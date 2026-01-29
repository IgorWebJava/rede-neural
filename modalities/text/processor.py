from layers.embeddings import Embedding
from layers.base import Module
from engine.tensor import Tensor
import numpy as np

class TextProcessor(Module):
    """
    Processador de Texto Soberano (RULE 06).
    Transforma tokens em vetores de características agregados.
    """
    def __init__(self, vocab_size, embed_dim):
        self.embedding = Embedding(vocab_size, embed_dim)

    def forward(self, tokens):
        # tokens: lista de índices ou Tensor de índices
        embeds = self.embedding(tokens)
        # Agregação simples por média para obter um vetor fixo da sequência
        # embeds shape: (seq_len, embed_dim)
        return embeds.sum(axis=0) * (1.0 / embeds.data.shape[0])

    def parameters(self):
        return self.embedding.parameters()
