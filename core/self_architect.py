import numpy as np
import os
import json

class SelfArchitect:
    """
    Sistema de Auto-Auditoria e Evolução de Arquitetura (RULE 06 & 12).
    Analisa o desempenho histórico e sugere ajustes estruturais.
    """
    def __init__(self, trainer):
        self.trainer = trainer
        self.audit_log = []

    def audit_performance(self, threshold_loss=0.1):
        """Analisa se a arquitetura atual está convergindo satisfatoriamente."""
        recent_losses = self.trainer.dashboard.history.get("loss", [])
        if len(recent_losses) < 10:
            return "INSUFFICIENT_DATA"
            
        avg_loss = np.mean(recent_losses[-10:])
        trend = recent_losses[-1] - recent_losses[-10]
        
        report = {
            "avg_loss": avg_loss,
            "trend": "IMPROVING" if trend < 0 else "STAGNATED",
            "efficiency": 1.0 / (avg_loss + 1e-9)
        }
        
        self.audit_log.append(report)
        
        if avg_loss > threshold_loss and trend >= 0:
            return "EXPANSION_RECOMMENDED"
        return "STABLE"

    def suggest_evolution(self):
        """Sugere modificações na arquitetura baseadas na auditoria."""
        status = self.audit_performance()
        
        suggestions = []
        if status == "EXPANSION_RECOMMENDED":
            suggestions.append({
                "action": "INCREASE_HIDDEN_DIM",
                "target": "fusion_layer",
                "reason": "Alta perda residual e estagnação de gradiente."
            })
            suggestions.append({
                "action": "ADD_CROSS_ATTENTION_HEADS",
                "target": "multimodal_fusion",
                "reason": "Necessidade de maior expressividade na fusão de modalidades."
            })
        elif status == "STABLE":
            suggestions.append({
                "action": "FREEZE_BACKBONE",
                "target": "vision_processor",
                "reason": "Características de baixo nível consolidadas."
            })
            
        return suggestions

    def save_audit_report(self, path="./docs/self_audit_report.json"):
        """Salva o relatório de auditoria estrutural."""
        with open(path, 'w') as f:
            json.dump(self.audit_log, f, indent=4)
        print(f"📑 Relatório de Auto-Arquitetura salvo em {path}")
