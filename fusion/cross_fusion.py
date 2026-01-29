from layers.attention import CrossAttention
from layers.base import Module, Linear, ReLU
from engine.tensor import Tensor

class CrossFusion(Module):
    """
    Módulo de Fusão Multimodal Avançada (RULE 06).
    Utiliza Cross-Attention para fundir duas modalidades.
    """
    def __init__(self, mod1_dim, mod2_dim, fusion_dim):
        self.attention = CrossAttention(mod1_dim, mod2_dim, fusion_dim)
        self.post_fusion = Linear(fusion_dim, fusion_dim)
        self.relu = ReLU()

    def forward(self, x1, x2):
        """
        x1: Modalidade 1 (Query)
        x2: Modalidade 2 (Key/Value)
        """
        # x1 e x2 devem ter forma (N, dim)
        # CrossAttention espera query (Nq, dim) e key_value (Nkv, dim)
        fused = self.attention(x1, x2)
        return self.relu(self.post_fusion(fused))

    def parameters(self):
        return self.attention.parameters() + self.post_fusion.parameters()
