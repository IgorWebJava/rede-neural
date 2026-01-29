# Exemplo de Kernel Otimizado com Numba JIT

import numpy as np
from numba import jit, prange

# ----------------------------------------------------------------------
# 1. Otimização de Multiplicação de Matrizes (Exemplo de Kernel)
#    A função jit(nopython=True) compila o código para código de máquina
#    nativo, removendo a sobrecarga do interpretador Python.
# ----------------------------------------------------------------------

@jit(nopython=True, cache=True)
def optimized_dot_product(A, B):
    """
    Multiplicação de matrizes otimizada para o Núcleo Neural.
    Assume que A e B são arrays numpy 2D.
    """
    return np.dot(A, B)

# ----------------------------------------------------------------------
# 2. Otimização de Loop Explícito com Paralelização (Exemplo de Ativação)
#    O uso de prange permite que o Numba paralelize o loop em múltiplos
#    núcleos de CPU, crucial para operações de elemento a elemento.
# ----------------------------------------------------------------------

@jit(nopython=True, parallel=True, cache=True)
def optimized_relu_activation(X):
    """
    Função de ativação ReLU otimizada e paralelizada.
    """
    out = np.empty_like(X)
    # prange é usado para paralelizar o loop
    for i in prange(X.shape[0]):
        for j in prange(X.shape[1]):
            out[i, j] = max(0.0, X[i, j])
    return out

# ----------------------------------------------------------------------
# 3. Exemplo de Otimização de Memória (Operação In-Place)
#    O Numba incentiva operações in-place para evitar alocação de memória.
# ----------------------------------------------------------------------

@jit(nopython=True, cache=True)
def optimized_add_in_place(A, B):
    """
    Adição de matrizes in-place (A += B).
    """
    A += B
    return A

# ----------------------------------------------------------------------
# Diretriz Crítica:
# O agente DEVE garantir que a lógica do Autograd (cálculo de gradientes)
# permaneça explícita em Python/Numpy, e apenas as operações de baixo
# nível (como as acima) sejam decoradas com @jit.
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Exemplo de uso e benchmark (o agente deve gerar um benchmark real)
    A = np.random.rand(100, 100)
    B = np.random.rand(100, 100)
    X = np.random.rand(500, 500)

    # Primeira chamada (compilação)
    _ = optimized_dot_product(A, B)
    _ = optimized_relu_activation(X)

    # Chamada otimizada
    result_dot = optimized_dot_product(A, B)
    result_relu = optimized_relu_activation(X)

    print("Otimização Numba JIT aplicada com sucesso.")
    print(f"Resultado da Multiplicação (Shape): {result_dot.shape}")
    print(f"Resultado da ReLU (Shape): {result_relu.shape}")
