# Exemplo de Kernel para Monitor de Patologias Neurais (Detecção de Explosão de Gradientes)

import numpy as np
from numba import jit, prange

# O uso de Numba JIT é aplicado para otimizar o cálculo da norma dos gradientes.

@jit(nopython=True, cache=True)
def calculate_global_norm(gradients):
    """
    Calcula a norma L2 global de todos os gradientes em uma lista de arrays numpy.
    Esta é a métrica primária para detectar explosão de gradientes.
    """
    global_norm_sq = 0.0
    for grad_array in gradients:
        # A norma L2 de um array é a raiz quadrada da soma dos quadrados de seus elementos.
        # Para evitar underflow/overflow, somamos os quadrados e tiramos a raiz no final.
        global_norm_sq += np.sum(grad_array**2)
        
    return np.sqrt(global_norm_sq)

def monitor_gradient_explosion(gradients, threshold=10.0):
    """
    Monitora a explosão de gradientes e retorna um alerta de patologia.
    
    gradients: Lista de arrays numpy (gradientes de cada camada).
    threshold: Limite máximo aceitável para a norma global.
    """
    global_norm = calculate_global_norm(gradients)
    
    patologia = {
        "nome": "Explosão de Gradientes",
        "detectado": False,
        "norma_atual": global_norm,
        "limite": threshold,
        "intervencao_sugerida": None
    }
    
    if global_norm > threshold:
        patologia["detectado"] = True
        patologia["intervencao_sugerida"] = "Gradient Clipping Dinâmico"
        
    return patologia

# ----------------------------------------------------------------------
# Diretriz Crítica:
# O agente DEVE integrar este monitor ao loop de treinamento,
# acionando o Mecanismo de Decisão Autônoma quando uma patologia é detectada.
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Exemplo de uso
    np.random.seed(42)
    
    # Simulação de gradientes normais
    grads_normal = [np.random.randn(10, 10) * 0.1, np.random.randn(5, 5) * 0.1]
    patologia_normal = monitor_gradient_explosion(grads_normal)
    
    print("--- Teste 1: Gradientes Normais ---")
    print(f"Norma Global: {patologia_normal['norma_atual']:.4f}")
    print(f"Patologia Detectada: {patologia_normal['detectado']}")
    
    # Simulação de explosão de gradientes
    grads_explosion = [np.random.randn(10, 10) * 5.0, np.random.randn(5, 5) * 5.0]
    patologia_explosion = monitor_gradient_explosion(grads_explosion)
    
    print("\n--- Teste 2: Explosão de Gradientes ---")
    print(f"Norma Global: {patologia_explosion['norma_atual']:.4f}")
    print(f"Patologia Detectada: {patologia_explosion['detectado']}")
    print(f"Intervenção: {patologia_explosion['intervencao_sugerida']}")
