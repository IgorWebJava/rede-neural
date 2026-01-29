from layers.attention import CrossAttention
from layers.base import Module, Linear
from engine.tensor import Tensor
import numpy as np

class SovereignCrossModalFusion(Module):
    """
    Fusão Multimodal Avançada via Cross-Attention (RULE 06).
    Texto atua como Query para extrair informações relevantes da Visão.
    """
    def __init__(self, text_dim, vision_dim, internal_dim):
        self.attention = CrossAttention(text_dim, vision_dim, internal_dim)
        self.output_projection = Linear(internal_dim, internal_dim)

    def forward(self, text_features, vision_features):
        """
        text_features: (N_tokens, text_dim)
        vision_features: (N_patches, vision_dim)
        """
        # Atenção Cruzada: O que no texto é relevante na imagem?
        context_vector = self.attention(text_features, vision_features)
        
        # Agregação final e projeção
        # Usamos a média do contexto se houver múltiplos tokens
        if context_vector.data.ndim > 2:
            agg_data = context_vector.data.mean(axis=0, keepdims=True)
            context_vector = Tensor(agg_data, requires_grad=True)
            
        return self.output_projection(context_vector)

    def parameters(self):
        return self.attention.parameters() + self.output_projection.parameters()
