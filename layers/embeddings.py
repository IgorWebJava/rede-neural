from engine.tensor import Tensor
from layers.base import Module
import numpy as np

class Embedding(Module):
    """
    Camada de Embedding Soberana para Texto (RULE 09).
    Converte índices de tokens em vetores densos.
    """
    def __init__(self, vocab_size, embedding_dim):
        # Inicialização Normal para embeddings
        self.weight = Tensor(np.random.randn(vocab_size, embedding_dim) * 0.01, requires_grad=True)

    def forward(self, indices):
        # indices é uma lista ou array de inteiros
        # Extração manual de linhas (Slicing Soberano)
        data = self.weight.data[indices]
        out = Tensor(data, _children=(self.weight,), _op='Embedding', requires_grad=self.weight.requires_grad)

        def _backward():
            if self.weight.requires_grad:
                # O gradiente do embedding é esparso: acumulamos nas linhas acessadas
                for i, idx in enumerate(indices):
                    self.weight.grad[idx] += out.grad[i]
        out._backward = _backward
        return out

    def parameters(self):
        return [self.weight]
