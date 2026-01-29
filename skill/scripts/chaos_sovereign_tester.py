import os
import sys
import numpy as np
import time

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from training.trainer import SovereignMultimodalTrainerV3

class SovereignChaosTesterV3:
    """
    Framework de Certificação V3 (RULE 05 & 08).
    Valida resiliência, conformidade e self-healing.
    """
    def __init__(self):
        self.trainer = SovereignMultimodalTrainerV3()
        self.report = []

    def test_gradient_explosion_recovery(self):
        """Simula explosão de gradiente e verifica se o HomeostasisAgent intervém."""
        print("🧪 Testando recuperação de explosão de gradiente...")
        
        # Forçar gradientes gigantes em um parâmetro
        for p in self.trainer.params:
            if p.requires_grad:
                p.grad = np.random.randn(*p.data.shape) * 1e6
        
        # Tentar um passo de treino
        health = self.trainer.monitor.check_health(self.trainer.params, 0.5)
        new_lr, action = self.trainer.agent.intervene(health, self.trainer.params, self.trainer.lr)
        
        if action == "LR_REDUCTION" or action == "GRADIENT_RESET":
            self.report.append(f"✅ Auto-Healing: Intervenção '{action}' detectada com sucesso.")
            return True
        else:
            self.report.append("❌ Auto-Healing: Falha ao detectar instabilidade nos gradientes.")
            return False

    def test_auditor_compliance(self):
        """Valida se o Auditor ainda passa após as mudanças."""
        print("🧪 Validando conformidade com o Auditor Soberano...")
        # Simulação interna do teste de auditoria
        from skill.scripts.sovereign_auditor import audit_rules, audit_project_structure
        violations = audit_rules(".")
        missing = audit_project_structure(".")
        
        if not violations and not missing:
            self.report.append("✅ Auditoria: Sistema 100% em conformidade com as RULES.")
            return True
        else:
            self.report.append(f"❌ Auditoria: Violações detectadas: {violations + missing}")
            return False

    def run_certification(self):
        print("\n--- 🛡️ Iniciando Certificação Sovereign V3 ---\n")
        self.test_gradient_explosion_recovery()
        self.test_auditor_compliance()
        
        print("\n--- 📜 Relatório Final de Certificação V3 ---")
        for line in self.report:
            print(line)
        
        all_passed = all("✅" in line for line in self.report)
        if all_passed:
            print("\nStatus: SISTEMA V3 CERTIFICADO - SOBERANIA PRESERVADA")
        else:
            print("\nStatus: FALHA NA CERTIFICAÇÃO")
            sys.exit(1)

if __name__ == "__main__":
    tester = SovereignChaosTesterV3()
    tester.run_certification()
