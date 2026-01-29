import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True, cache=True)
def fast_hadamard_product(A, B):
    """Produto de Hadamard (elemento a elemento) ultra-otimizado."""
    out = np.empty_like(A)
    for i in prange(A.shape[0]):
        for j in prange(A.shape[1]):
            out[i, j] = A[i, j] * B[i, j]
    return out

@jit(nopython=True, parallel=True, cache=True)
def fast_matrix_add_scaled(A, B, alpha):
    """Adição de matrizes escalonada: A + alpha * B."""
    out = np.empty_like(A)
    for i in prange(A.shape[0]):
        for j in prange(A.shape[1]):
            out[i, j] = A[i, j] + alpha * B[i, j]
    return out

@jit(nopython=True, cache=True)
def low_level_norm(A):
    """Cálculo de norma de Frobenius otimizado."""
    return np.sqrt(np.sum(A**2))
