import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True)
def sovereign_fused_linear_relu(x, w, b):
    """
    Kernel Industrial Fundido: Linear + ReLU.
    Reduz overhead de memória e melhora localidade de cache ao processar
    a ativação imediatamente após a multiplicação de matrizes.
    """
    m, n = x.shape
    n_out = w.shape[1]
    
    # Alocação de saída
    out = np.zeros((m, n_out))
    
    for i in prange(m):
        for j in range(n_out):
            dot = 0.0
            for k in range(n):
                dot += x[i, k] * w[k, j]
            
            # Adicionar Bias
            val = dot + b[j]
            
            # ReLU In-Place (Fusão)
            if val < 0:
                out[i, j] = 0.0
            else:
                out[i, j] = val
                
    return out

@jit(nopython=True, parallel=True)
def sovereign_fused_backward(grad_out, x, w, out_forward):
    """
    Backward fundido para Linear + ReLU.
    Calcula gradientes de pesos e entrada em um único passo.
    """
    m, n = x.shape
    n_out = w.shape[1]
    
    grad_w = np.zeros((n, n_out))
    grad_x = np.zeros((m, n))
    grad_b = np.zeros(n_out)
    
    # 1. Aplicar derivada da ReLU ao grad_out
    # 2. Calcular gradientes
    for i in prange(m):
        for j in range(n_out):
            # Derivada da ReLU
            if out_forward[i, j] <= 0:
                g = 0.0
            else:
                g = grad_out[i, j]
            
            grad_b[j] += g
            
            for k in range(n):
                grad_w[k, j] += x[i, k] * g
                grad_x[i, k] += w[k, j] * g
                
    return grad_x, grad_w, grad_b
