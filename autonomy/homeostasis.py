import numpy as np
import time
import os

class PathologyMonitor:
    """
    Monitor de Patologias Neurais (RULE 05).
    Detecta instabilidades como NaNs, explosão de gradientes e estagnação.
    """
    def __init__(self, threshold_grad=100.0):
        self.threshold_grad = threshold_grad
        self.history = []

    def check_health(self, parameters, loss_value):
        """Avalia a saúde dos parâmetros e da loss."""
        status = {"healthy": True, "issues": []}
        
        # 1. Verificar NaNs na Loss
        if np.isnan(loss_value) or np.isinf(loss_value):
            status["healthy"] = False
            status["issues"].append("CATASTROPHIC_LOSS_FAILURE")
            
        # 2. Verificar Gradientes (RULE 05)
        for i, p in enumerate(parameters):
            if p.grad is not None:
                grad_norm = np.linalg.norm(p.grad)
                if np.isnan(grad_norm) or grad_norm > self.threshold_grad:
                    status["healthy"] = False
                    status["issues"].append(f"GRADIENT_EXPLOSION_PARAM_{i}")
        
        return status

class HomeostasisAgent:
    """
    Agente de Intervenção Homeostática (Self-Healing).
    Executa ações corretivas baseadas no diagnóstico do monitor.
    """
    def __init__(self, persistence_manager):
        self.pm = persistence_manager
        self.last_stable_checkpoint = None

    def intervene(self, status, parameters, current_lr):
        """Aplica intervenções para restaurar a estabilidade."""
        new_lr = current_lr
        action_taken = "NONE"
        
        if not status["healthy"]:
            print(f"🚨 Intervenção Homeostática Necessária: {status['issues']}")
            
            # Ação 1: Reduzir drasticamente o Learning Rate
            new_lr = current_lr * 0.1
            action_taken = "LR_REDUCTION"
            
            # Ação 2: Se houver NaNs, tentar restaurar último estado estável
            if any("CATASTROPHIC" in issue for issue in status["issues"]):
                if self.last_stable_checkpoint:
                    self.pm.load_weights(parameters, self.last_stable_checkpoint)
                    action_taken = "STATE_RESTORATION"
                else:
                    # Se não houver checkpoint, reinicializar gradientes
                    for p in parameters:
                        if p.grad is not None:
                            p.grad.fill(0)
                    action_taken = "GRADIENT_RESET"
                    
        return new_lr, action_taken

    def record_stable_state(self, parameters, filename):
        """Salva um checkpoint quando o sistema está saudável."""
        self.pm.save_weights(parameters, filename)
        self.last_stable_checkpoint = filename
