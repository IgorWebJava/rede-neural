import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True)
def sovereign_cross_attention(q, k, v, mask=None):
    """
    Kernel de Atenção Cross-Modal Soberano otimizado com Numba JIT.
    Permite que uma modalidade (ex: Texto) atue como Query e outra (ex: Imagem) como Key/Value.
    """
    n_q, d_k = q.shape
    n_k, d_v = v.shape
    
    # 1. MatMul Q @ K.T / sqrt(d_k)
    scores = np.zeros((n_q, n_k))
    scale = np.sqrt(d_k)
    
    for i in prange(n_q):
        for j in range(n_k):
            dot = 0.0
            for l in range(d_k):
                dot += q[i, l] * k[j, l]
            scores[i, j] = dot / scale
            
    # 2. Aplicar Máscara (se houver)
    if mask is not None:
        scores += mask
        
    # 3. Softmax Manual
    for i in prange(n_q):
        max_val = np.max(scores[i, :])
        exp_sum = 0.0
        for j in range(n_k):
            scores[i, j] = np.exp(scores[i, j] - max_val)
            exp_sum += scores[i, j]
        for j in range(n_k):
            scores[i, j] /= exp_sum
            
    # 4. MatMul Scores @ V
    output = np.zeros((n_q, d_v))
    for i in prange(n_q):
        for j in range(d_v):
            val = 0.0
            for l in range(n_k):
                val += scores[i, l] * v[l, j]
            output[i, j] = val
            
    return output
