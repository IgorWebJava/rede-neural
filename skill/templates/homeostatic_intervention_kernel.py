# Exemplo de Kernel para Intervenção Homeostática (Gradient Clipping Dinâmico)

import numpy as np
from numba import jit, prange
from templates.pathology_monitor_kernel import calculate_global_norm

@jit(nopython=True, cache=True)
def apply_gradient_clipping(gradients, clip_norm):
    """
    Aplica o Gradient Clipping dinâmico em-place.
    
    gradients: Lista de arrays numpy (gradientes de cada camada).
    clip_norm: O limite máximo para a norma global.
    """
    
    # 1. Calcular a norma global atual
    global_norm = calculate_global_norm(gradients)
    
    # 2. Calcular o fator de clipping
    # Se a norma for maior que o limite, o fator será menor que 1.0
    clipping_factor = clip_norm / global_norm
    
    # 3. Aplicar o clipping apenas se a norma exceder o limite
    if global_norm > clip_norm:
        # O fator de clipping é aplicado a todos os gradientes
        for i in prange(len(gradients)):
            gradients[i] *= clipping_factor
        
        return True, global_norm * clipping_factor # Retorna a nova norma
    
    return False, global_norm # Retorna a norma original

# ----------------------------------------------------------------------
# Diretriz Crítica:
# Este kernel DEVE ser chamado pelo Adaptador de Hiperparâmetros e Intervenção Homeostática
# após o Monitor de Patologias detectar uma explosão de gradientes.
# A intervenção é feita em-place (in-place), otimizada com Numba.
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Exemplo de uso
    np.random.seed(42)
    clip_limite = 1.0
    
    # Simulação de explosão de gradientes
    grads_explosion = [np.random.randn(10, 10) * 5.0, np.random.randn(5, 5) * 5.0]
    
    norma_original = calculate_global_norm(grads_explosion)
    
    print(f"Norma Original: {norma_original:.4f}")
    print(f"Limite de Clipping: {clip_limite}")
    
    # Aplica o clipping
    clipped, nova_norma = apply_gradient_clipping(grads_explosion, clip_limite)
    
    if clipped:
        print(f"\nClipping Aplicado: Sim")
        print(f"Nova Norma Global: {nova_norma:.4f}")
    else:
        print("\nClipping Aplicado: Não (Norma já estava abaixo do limite)")
