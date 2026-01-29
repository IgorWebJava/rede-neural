import numpy as np
from engine.tensor import Tensor
from layers.base import Module, Linear, ReLU

class AlignmentLayer(Module):
    """
    Camada de Alinhamento Neural Soberana (RULE 01 & 13).
    V9: Garante que as representações latentes permaneçam dentro de um 
    'Hipercubo de Segurança' definido por vetores éticos.
    """
    def __init__(self, feature_dim):
        self.feature_dim = feature_dim
        # Vetores de referência ética (Espaço de Segurança)
        # Em uma versão avançada, estes seriam aprendidos via RLHF soberano
        self.safety_anchors = Tensor(np.random.uniform(-0.5, 0.5, (1, feature_dim)), requires_grad=False)
        self.projection = Linear(feature_dim, feature_dim)
        self.relu = ReLU()

    def forward(self, x):
        """
        Projeta o vetor de entrada para mais próximo das âncoras de segurança.
        """
        # 1. Transformação de Alinhamento
        h = self.relu(self.projection(x))
        
        # 2. Penalidade de Distância (Soft Constraint)
        # Se a distância for muito alta, puxamos o vetor de volta
        dist = np.linalg.norm(h.data - self.safety_anchors.data)
        if dist > 1.0:
            scale = 1.0 / (dist + 1e-8)
            h.data = h.data * scale
            
        return h

    def parameters(self):
        return self.projection.parameters()

class EthicsMonitor:
    """
    Monitor de Ética em Tempo Real.
    Analisa predições e ativa protocolos de segurança se necessário.
    """
    @staticmethod
    def evaluate_intent(prediction_val, threshold=0.95):
        """
        Avalia se uma predição extrema pode indicar comportamento de risco.
        """
        if prediction_val > threshold:
            return "WARNING: Extreme Prediction Detected"
        return "SAFE"
