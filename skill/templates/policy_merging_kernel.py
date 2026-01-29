import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True)
def sovereign_policy_merging(q_tables, weights):
    """
    Kernel de Fusão de Políticas Soberano.
    Realiza a média ponderada de múltiplas Q-Tables (políticas de RL)
    para gerar um modelo de consenso global.
    
    q_tables: Array 4D (num_agentes, estados, acoes, features)
    weights: Array 1D (num_agentes) - Pesos de confiança
    """
    num_agentes, num_states, num_actions, num_features = q_tables.shape
    
    # Normalizar pesos
    total_weight = np.sum(weights)
    norm_weights = weights / total_weight
    
    # Q-Table de Consenso
    consensus_q = np.zeros((num_states, num_actions, num_features))
    
    for a in range(num_agentes):
        w = norm_weights[a]
        for s in prange(num_states):
            for act in range(num_actions):
                for f in range(num_features):
                    consensus_q[s, act, f] += q_tables[a, s, act, f] * w
                    
    return consensus_q

@jit(nopython=True)
def calculate_trust_score(stability_score, performance_score, uptime_score):
    """
    Calcula o score de confiança de um agente para ponderação no consenso.
    """
    # Pesos fixos de importância industrial
    w_stability = 0.4
    w_performance = 0.4
    w_uptime = 0.2
    
    return (stability_score * w_stability) + \
           (performance_score * w_performance) + \
           (uptime_score * w_uptime)
