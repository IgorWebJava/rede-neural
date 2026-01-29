# Exemplo de Kernel para Aprendizado Contraste Multimodal (InfoNCE)

import numpy as np
from numba import jit, prange

# O uso de Numba JIT é crucial aqui para otimizar as operações de matrizes
# e o cálculo da exponencial, que são intensivos em Loss de Contraste.

@jit(nopython=True, cache=True)
def cosine_similarity(a, b):
    """Calcula a similaridade de cosseno entre dois vetores."""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

@jit(nopython=True, cache=True)
def info_nce_loss_kernel(embeddings_a, embeddings_b, temperature=0.07):
    """
    Calcula a Loss InfoNCE (Normalized Temperature-scaled Cross-Entropy)
    para um batch de embeddings pareados (ex: Texto e Imagem).

    embeddings_a: Matriz de embeddings da Modalidade A (N x D)
    embeddings_b: Matriz de embeddings da Modalidade B (N x D)
    N: Tamanho do batch
    D: Dimensão do embedding
    """
    N = embeddings_a.shape[0]
    
    # 1. Calcular a matriz de similaridade (N x N)
    # A matriz S[i, j] é a similaridade entre A[i] e B[j]
    similarity_matrix = np.dot(embeddings_a, embeddings_b.T)
    
    # 2. Aplicar a temperatura
    similarity_matrix /= temperature
    
    # 3. Calcular a exponencial (numerador e denominador)
    exp_similarity = np.exp(similarity_matrix)
    
    # 4. Calcular o denominador (soma das exponenciais em cada linha/coluna)
    # Denominador para A -> B (soma nas colunas)
    denominator_a = np.sum(exp_similarity, axis=1)
    
    # Denominador para B -> A (soma nas linhas)
    denominator_b = np.sum(exp_similarity, axis=0)
    
    # 5. Calcular a Loss (Cross-Entropy)
    
    # Loss A -> B (Target é a diagonal)
    log_prob_a = similarity_matrix.diagonal() - np.log(denominator_a)
    loss_a = -np.mean(log_prob_a)
    
    # Loss B -> A (Target é a diagonal)
    log_prob_b = similarity_matrix.diagonal() - np.log(denominator_b)
    loss_b = -np.mean(log_prob_b)
    
    # Loss total (média das duas direções)
    total_loss = (loss_a + loss_b) / 2
    
    return total_loss

# ----------------------------------------------------------------------
# Diretriz Crítica:
# O agente DEVE implementar a função de backpropagation (gradientes)
# para esta Loss manualmente, utilizando o Autograd Soberano.
# Este kernel apenas fornece o cálculo eficiente do valor da Loss.
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Exemplo de uso
    np.random.seed(42)
    D = 128  # Dimensão do embedding
    N = 32   # Tamanho do batch
    
    # Embeddings normalizados
    E_text = np.random.randn(N, D).astype(np.float32)
    E_image = np.random.randn(N, D).astype(np.float32)
    
    # Normalização (crucial para InfoNCE)
    E_text /= np.linalg.norm(E_text, axis=1, keepdims=True)
    E_image /= np.linalg.norm(E_image, axis=1, keepdims=True)
    
    # Primeira chamada (compilação JIT)
    _ = info_nce_loss_kernel(E_text, E_image)
    
    # Chamada otimizada
    loss_value = info_nce_loss_kernel(E_text, E_image)
    
    print("Kernel InfoNCE otimizado com Numba JIT aplicado com sucesso.")
    print(f"Loss InfoNCE calculada: {loss_value:.4f}")
