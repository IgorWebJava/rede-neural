import numpy as np
from typing import List, Dict

class ByzantineConsensus:
    """
    Protocolo de Consenso Bizantino Soberano (RULE 01, 04 & 06).
    Garante que o enxame ignore contribuições maliciosas ou ruidosas (Outliers).
    V7: Implementação de Trimmed Mean e Mediana Geométrica para fusão robusta.
    """
    def __init__(self, trim_factor=0.1):
        self.trim_factor = trim_factor # Porcentagem de outliers a remover de cada lado

    def robust_merge(self, contributions: List[Dict[str, np.ndarray]]):
        """
        Realiza a fusão de pesos utilizando a média aparada (Trimmed Mean)
        para mitigar ataques de envenenamento de modelo (Model Poisoning).
        """
        if not contributions:
            return None
            
        keys = contributions[0].keys()
        merged_weights = {}
        
        for key in keys:
            # Coletar todos os pesos para esta chave
            weights_stack = np.stack([c[key] for c in contributions], axis=0)
            
            # Ordenar ao longo do eixo dos agentes
            sorted_weights = np.sort(weights_stack, axis=0)
            
            # Calcular índices para o corte (trimming)
            n = len(contributions)
            low_idx = int(n * self.trim_factor)
            high_idx = n - low_idx
            
            if high_idx <= low_idx: # Fallback para mediana se o enxame for pequeno
                merged_weights[key] = np.median(weights_stack, axis=0)
            else:
                # Média dos valores centrais
                trimmed_weights = sorted_weights[low_idx:high_idx]
                merged_weights[key] = np.mean(trimmed_weights, axis=0)
                
        return merged_weights

    def validate_contribution(self, global_weights, local_weights, threshold=5.0):
        """
        Audita uma contribuição individual contra o consenso global.
        Retorna True se a contribuição for considerada 'saudável'.
        """
        divergence = 0
        count = 0
        for key in global_weights:
            # Distância Euclidiana entre pesos globais e locais
            dist = np.linalg.norm(global_weights[key] - local_weights[key])
            divergence += dist
            count += 1
            
        avg_divergence = divergence / count
        # Se a divergência for muito alta, o nó pode estar corrompido ou mal treinado
        return avg_divergence < threshold
