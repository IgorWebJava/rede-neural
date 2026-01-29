import numpy as np
from engine.kernels import optimized_matmul, optimized_add, optimized_mul

class Tensor:
    """
    Implementação Soberana de Tensor N-D (RULE 09).
    V4: Integrado com Kernels Numba JIT para performance industrial.
    """
    def __init__(self, data, requires_grad=False, _children=(), _op=''):
        # Garantir que data seja sempre um array numpy
        if isinstance(data, (int, float, list)):
            data = np.array(data, dtype=np.float32)
        elif isinstance(data, np.ndarray):
            data = data.astype(np.float32)
            
        self.data = data
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data) if requires_grad else None
        
        # Internals para Autograd (RULE 06)
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        return f"SovereignTensor(shape={self.data.shape}, op={self._op})"

    def _handle_broadcasting(self, target_tensor, grad):
        """Ajusta o gradiente para corresponder à forma do tensor original após broadcasting."""
        if not target_tensor.requires_grad:
            return
        
        # Converter grad para array se for escalar (proteção V4)
        if np.isscalar(grad):
            grad = np.array(grad, dtype=np.float32)
        
        # 1. Reduzir dimensões extras à esquerda
        while grad.ndim > target_tensor.data.ndim:
            grad = grad.sum(axis=0)
            
        # 2. Reduzir dimensões onde o original tinha tamanho 1
        for i, dim in enumerate(target_tensor.data.shape):
            if dim == 1:
                grad = grad.sum(axis=i, keepdims=True)
                
        target_tensor.grad += grad

    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out_data = optimized_add(self.data, other.data)
        out = Tensor(out_data, 
                    requires_grad=(self.requires_grad or other.requires_grad),
                    _children=(self, other), 
                    _op='+')

        def _backward():
            if self.requires_grad:
                self._handle_broadcasting(self, out.grad)
            if other.requires_grad:
                self._handle_broadcasting(other, out.grad)
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out_data = optimized_mul(self.data, other.data)
        out = Tensor(out_data, 
                    requires_grad=(self.requires_grad or other.requires_grad),
                    _children=(self, other), 
                    _op='*')

        def _backward():
            if self.requires_grad:
                self._handle_broadcasting(self, optimized_mul(other.data, out.grad))
            if other.requires_grad:
                self._handle_broadcasting(other, optimized_mul(self.data, out.grad))
        out._backward = _backward
        return out

    def pow(self, other):
        return self.__pow__(other)

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "Soberania: Apenas potências numéricas suportadas no momento."
        out = Tensor(self.data**other, requires_grad=self.requires_grad, _children=(self,), _op=f'**{other}')

        def _backward():
            if self.requires_grad:
                self.grad += (other * self.data**(other - 1)) * out.grad
        out._backward = _backward
        return out

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def matmul(self, other):
        """Multiplicação de matrizes soberana otimizada (V4)."""
        other = other if isinstance(other, Tensor) else Tensor(other)
        out_data = optimized_matmul(self.data, other.data)
        out = Tensor(out_data, 
                    requires_grad=(self.requires_grad or other.requires_grad),
                    _children=(self, other), 
                    _op='matmul')

        def _backward():
            if self.requires_grad:
                self.grad += optimized_matmul(out.grad, other.data.T)
            if other.requires_grad:
                other.grad += optimized_matmul(self.data.T, out.grad)
        out._backward = _backward
        return out

    def exp(self):
        out = Tensor(np.exp(self.data), requires_grad=self.requires_grad, _children=(self,), _op='exp')

        def _backward():
            if self.requires_grad:
                self.grad += out.data * out.grad
        out._backward = _backward
        return out

    def log(self):
        out = Tensor(np.log(self.data + 1e-8), requires_grad=self.requires_grad, _children=(self,), _op='log')

        def _backward():
            if self.requires_grad:
                self.grad += (1.0 / (self.data + 1e-8)) * out.grad
        out._backward = _backward
        return out

    def sum(self, axis=None, keepdims=False):
        out = Tensor(np.sum(self.data, axis=axis, keepdims=keepdims), 
                    requires_grad=self.requires_grad, _children=(self,), _op='sum')

        def _backward():
            if self.requires_grad:
                grad = out.grad
                if axis is not None and not keepdims:
                    if isinstance(axis, int):
                        grad = np.expand_dims(grad, axis=axis)
                    else:
                        for a in sorted(axis):
                            grad = np.expand_dims(grad, axis=a)
                self.grad += np.ones_like(self.data) * grad
        out._backward = _backward
        return out

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        if self.grad is None:
            self.grad = np.ones_like(self.data)
        else:
            self.grad.fill(1.0)
        
        for node in reversed(topo):
            node._backward()
