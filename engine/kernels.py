import numpy as np
from numba import jit

@jit(nopython=True, cache=True)
def optimized_matmul(A, B):
    """Multiplicação de matrizes otimizada via Numba."""
    return np.dot(A, B)

@jit(nopython=True, cache=True)
def optimized_add(A, B):
    """Adição de tensores otimizada."""
    return A + B

@jit(nopython=True, cache=True)
def optimized_mul(A, B):
    """Multiplicação elemento a elemento otimizada."""
    return A * B

@jit(nopython=True, cache=True)
def optimized_relu(X):
    """ReLU de alta performance."""
    # np.maximum é bem otimizado pelo Numba
    return np.maximum(0.0, X)

@jit(nopython=True, cache=True)
def optimized_relu_backward(X, grad_out):
    """Backward da ReLU otimizado."""
    return np.where(X > 0, grad_out, 0.0)
