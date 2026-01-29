from layers.base import Module, Linear, ReLU
from engine.tensor import Tensor
import numpy as np

class VisionProcessor(Module):
    """
    Processador de Visão Soberano (RULE 06).
    Simplificado para processar imagens como vetores flat.
    """
    def __init__(self, input_dim, hidden_dim, output_dim):
        self.fc1 = Linear(input_dim, hidden_dim)
        self.relu = ReLU()
        self.fc2 = Linear(hidden_dim, output_dim)

    def forward(self, x):
        # x shape: (batch, channels, height, width) -> flatten
        if x.data.ndim > 2:
            batch_size = x.data.shape[0]
            flat_data = x.data.reshape(batch_size, -1)
            x = Tensor(flat_data, requires_grad=x.requires_grad)
        
        h = self.relu(self.fc1(x))
        return self.fc2(h)

    def parameters(self):
        return self.fc1.parameters() + self.fc2.parameters()
