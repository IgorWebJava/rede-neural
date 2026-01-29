from engine.tensor import Tensor
from engine.kernels import optimized_relu, optimized_relu_backward
import numpy as np

class Module:
    """
    Classe base para todos os módulos neurais (RULE 06).
    """
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

    def forward(self, *args, **kwargs):
        raise NotImplementedError

    def parameters(self):
        """Retorna a lista de tensores de parâmetros do módulo."""
        return []

class Linear(Module):
    """
    Camada Linear (Fully Connected) Soberana.
    """
    def __init__(self, in_features, out_features, bias=True):
        # Inicialização Xavier/Glorot (RULE 07)
        limit = np.sqrt(6 / (in_features + out_features))
        self.weight = Tensor(np.random.uniform(-limit, limit, (in_features, out_features)), requires_grad=True)
        self.bias = Tensor(np.zeros((1, out_features)), requires_grad=True) if bias else None

    def forward(self, x):
        out = x.matmul(self.weight)
        if self.bias:
            out = out + self.bias
        return out

    def parameters(self):
        params = [self.weight]
        if self.bias:
            params.append(self.bias)
        return params

class ReLU(Module):
    """
    Função de Ativação ReLU Soberana Otimizada (V4).
    """
    def forward(self, x):
        # V4: Uso de kernel ReLU otimizado
        out_data = optimized_relu(x.data)
        out = Tensor(out_data, _children=(x,), _op='ReLU', requires_grad=x.requires_grad)

        def _backward():
            if x.requires_grad:
                # V4: Uso de kernel ReLU backward otimizado
                x.grad += optimized_relu_backward(x.data, out.grad)
        out._backward = _backward
        return out

class Sigmoid(Module):
    """
    Função de Ativação Sigmoid Soberana.
    """
    def forward(self, x):
        return (Tensor(1.0) + (-x).exp()).pow(-1)

class Tanh(Module):
    """
    Função de Ativação Tanh Soberana.
    """
    def forward(self, x):
        e_x = x.exp()
        e_nx = (-x).exp()
        return (e_x - e_nx) * (e_x + e_nx).pow(-1)

class Softmax(Module):
    """
    Função de Ativação Softmax Soberana.
    """
    def forward(self, x):
        max_val = np.max(x.data, axis=-1, keepdims=True)
        x_stable = x - Tensor(max_val)
        exp_x = x_stable.exp()
        sum_exp = exp_x.sum(axis=-1, keepdims=True)
        return exp_x * sum_exp.pow(-1)
