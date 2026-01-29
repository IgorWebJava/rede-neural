import numpy as np
import sys
import os
from persistence.db_manager import SovereignDBManager

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from inference.engine import EdgeInferenceEngine
from inference.explainability import SovereignExplainer
from modalities.text.processor import TextProcessor
from modalities.vision.processor import VisionProcessor

class HybridAIChat:
    """
    Chat AI Híbrido Soberano (RULE 01 & 09).
    V12: Integra CRUD completo com MySQL para histórico e persistência de contexto.
    """
    def __init__(self, model_params):
        self.engine = EdgeInferenceEngine(model_params)
        self.explainer = SovereignExplainer(model_params)
        self.text_proc = TextProcessor()
        self.vision_proc = VisionProcessor()
        self.db = SovereignDBManager()

    def process_message(self, user_input, modality="text", data=None):
        """
        Processa uma mensagem do usuário e persiste no MySQL (V12).
        """
        # 1. Processar entrada
        if modality == "text":
            text_features = self.text_proc.process(user_input)
            vision_features = np.zeros_like(text_features)
        elif modality == "image":
            vision_features = self.vision_proc.process(data)
            text_features = self.text_proc.process(user_input or "")
        else:
            text_features = np.random.randn(1, 32)
            vision_features = np.random.randn(1, 32)
        
        # 2. Executar inferência
        prediction, latency = self.engine.run_inference(vision_features, text_features)
        
        # 3. Gerar explicação
        explanation = self.explainer.explain_prediction(vision_features, text_features, prediction)
        
        # 4. Formular resposta
        response = self._generate_response(user_input, explanation, prediction)
        
        # 5. Persistir no MySQL (V12 CRUD)
        self.db.add_chat_entry(
            user_input=user_input,
            response=response,
            modality=modality,
            explanation=explanation,
            prediction=float(prediction[0][0])
        )
        
        return response, explanation

    def _generate_response(self, user_input, explanation, prediction):
        decision = explanation["prediction"]
        confidence = explanation["confidence"]
        reasoning = explanation["reasoning"]
        
        response = f"Análise Concluída:\n"
        response += f"- Resultado: {decision}\n"
        response += f"- Confiança: {confidence}\n"
        response += f"- Raciocínio: {reasoning}\n"
        
        return response

    def get_history(self, limit=50):
        """Recupera histórico do MySQL (V12)."""
        return self.db.get_chat_history(limit)
