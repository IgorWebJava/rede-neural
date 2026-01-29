import numpy as np
from numba import jit, prange, vectorize, float32

# ----------------------------------------------------------------------
# 1. Kernel Vetorizado (SIMD)
# ----------------------------------------------------------------------

@vectorize([float32(float32, float32)], target='parallel')
def sovereign_simd_add(a, b):
    """
    Soma de elementos vetorizada (SIMD) usando Numba.
    O target='parallel' permite que o compilador use instruções SIMD e multi-threading.
    """
    return a + b

@jit(nopython=True, parallel=True, fastmath=True)
def sovereign_simd_matmul(A, B):
    """
    Multiplicação de Matrizes (MatMul) com otimização SIMD e Paralelismo.
    - nopython=True: Garante que o código seja compilado para código de máquina puro.
    - parallel=True: Ativa o paralelismo automático (prange).
    - fastmath=True: Permite otimizações matemáticas agressivas (ex: reordenação de operações).
    """
    M, N = A.shape
    N, P = B.shape
    C = np.zeros((M, P), dtype=np.float32)
    
    # Otimização de Tiling (Blocagem) para localidade de cache
    BLOCK_SIZE = 32
    
    for i_block in prange(0, M, BLOCK_SIZE):
        for k_block in range(0, N, BLOCK_SIZE):
            for j_block in range(0, P, BLOCK_SIZE):
                
                # Processamento do Bloco
                for i in range(i_block, min(i_block + BLOCK_SIZE, M)):
                    for k in range(k_block, min(k_block + BLOCK_SIZE, N)):
                        temp = A[i, k]
                        for j in range(j_block, min(j_block + BLOCK_SIZE, P)):
                            C[i, j] += temp * B[k, j]
    return C

# ----------------------------------------------------------------------
# 2. Benchmark de Performance (RULE 02 & 10)
# ----------------------------------------------------------------------

def run_benchmark():
    import time
    
    # Matrizes de teste (1024x1024)
    size = 1024
    A = np.random.rand(size, size).astype(np.float32)
    B = np.random.rand(size, size).astype(np.float32)
    
    print(f"🚀 Iniciando Benchmark SIMD (Matriz {size}x{size})...")
    
    # 1. Warm-up (Compilação JIT)
    _ = sovereign_simd_matmul(A[:10, :10], B[:10, :10])
    
    # 2. Teste Otimizado
    start = time.time()
    C_simd = sovereign_simd_matmul(A, B)
    end = time.time()
    simd_time = end - start
    print(f"✅ SIMD MatMul: {simd_time:.4f}s")
    
    # 3. Teste Numpy (Referência)
    start = time.time()
    C_np = np.dot(A, B)
    end = time.time()
    np_time = end - start
    print(f"✅ Numpy dot: {np_time:.4f}s")
    
    print(f"\n📊 Fator de Aceleração: {np_time / simd_time:.2f}x")
    
    # Validação de Integridade (RULE 05)
    diff = np.max(np.abs(C_simd - C_np))
    if diff < 1e-4:
        print("💎 Precisão Numérica: Validada (Erro < 1e-4)")
    else:
        print(f"⚠️ Alerta de Precisão: Diferença de {diff:.2e}")

if __name__ == '__main__':
    run_benchmark()
