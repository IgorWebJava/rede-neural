import numpy as np

class SovereignBiasAuditor:
    """
    Auditor de Viés e Estereótipos (RULE 13).
    V9: Analisa a distribuição de predições entre diferentes grupos latentes.
    """
    def __init__(self):
        self.stats = {}

    def audit_prediction(self, features, prediction, group_id):
        """
        Registra estatísticas de predição para auditoria de disparidade.
        """
        if group_id not in self.stats:
            self.stats[group_id] = {"preds": [], "count": 0}
            
        self.stats[group_id]["preds"].append(float(prediction))
        self.stats[group_id]["count"] += 1

    def calculate_disparity(self):
        """
        Calcula a disparidade estatística entre grupos.
        """
        if len(self.stats) < 2:
            return 0.0
            
        means = [np.mean(g["preds"]) for g in self.stats.values()]
        # Disparidade = Max Diff entre as médias de predição
        disparity = max(means) - min(means)
        
        return disparity

    def suggest_mitigation(self):
        disparity = self.calculate_disparity()
        if disparity > 0.2:
            return {
                "action": "ADJUST_ALIGNMENT_LAYER",
                "severity": "HIGH",
                "reason": f"Disparidade detectada: {disparity:.4f}"
            }
        return {"action": "NONE", "severity": "LOW"}
