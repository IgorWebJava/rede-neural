import numpy as np

class SovereignExplainer:
    """
    Camada de Explicabilidade Soberana (RULE 14).
    V10: Traduz ativações neurais e decisões do enxame em relatórios legíveis.
    """
    def __init__(self, model_params):
        self.params = model_params

    def explain_prediction(self, vision_feat, text_feat, prediction):
        """
        Analisa a contribuição de cada modalidade para a predição final.
        """
        # Cálculo simplificado de contribuição (Magnitude de Ativação)
        v_magnitude = np.mean(np.abs(vision_feat))
        t_magnitude = np.mean(np.abs(text_feat))
        
        total = v_magnitude + t_magnitude + 1e-8
        v_contrib = (v_magnitude / total) * 100
        t_contrib = (t_magnitude / total) * 100
        
        explanation = {
            "prediction": "POSITIVA" if prediction > 0.5 else "NEGATIVA",
            "confidence": f"{abs(prediction - 0.5) * 200:.2f}%",
            "modalities": {
                "vision": f"{v_contrib:.2f}% de influência",
                "text": f"{t_contrib:.2f}% de influência"
            },
            "reasoning": self._generate_reasoning(v_contrib, t_contrib)
        }
        return explanation

    def _generate_reasoning(self, v_contrib, t_contrib):
        if v_contrib > t_contrib:
            return "A decisão foi baseada predominantemente em padrões visuais detectados."
        else:
            return "A decisão foi baseada predominantemente no contexto textual analisado."

    def log_explanation(self, explanation):
        print("\n--- 🧠 EXPLICAÇÃO SOBERANA ---")
        print(f"Resultado: {explanation['prediction']} (Confiança: {explanation['confidence']})")
        print(f"Influência Visão: {explanation['modalities']['vision']}")
        print(f"Influência Texto: {explanation['modalities']['text']}")
        print(f"Raciocínio: {explanation['reasoning']}")
        print("------------------------------")
