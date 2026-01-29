import numpy as np
from numba import jit, prange

# ----------------------------------------------------------------------
# 1. Swarm Trust-Weighting Kernel
# ----------------------------------------------------------------------

@jit(nopython=True, parallel=True)
def calculate_trust_scores(stability_history, performance_metrics, uptime_data):
    """
    Calcula o score de confiança de cada agente no enxame.
    - stability_history: Histórico de auto-correções (0.0 a 1.0)
    - performance_metrics: Precisão em tarefas de validação (0.0 a 1.0)
    - uptime_data: Maturidade operacional (normalizado)
    """
    num_agents = stability_history.shape[0]
    trust_scores = np.zeros(num_agents)
    
    for i in prange(num_agents):
        # Ponderação: 40% Estabilidade, 40% Performance, 20% Uptime
        score = (stability_history[i] * 0.4) + \
                (performance_metrics[i] * 0.4) + \
                (uptime_data[i] * 0.2)
        trust_scores[i] = score
        
    # Normalização Softmax para pesos de fusão
    max_score = np.max(trust_scores)
    exp_scores = np.exp(trust_scores - max_score)
    return exp_scores / np.sum(exp_scores)

@jit(nopython=True, parallel=True)
def sovereign_policy_fusion(policies, trust_weights):
    """
    Realiza a fusão ponderada de políticas (Q-Tables) de múltiplos agentes.
    - policies: Tensor (Agentes, Estados, Ações)
    - trust_weights: Vetor de pesos de confiança por agente
    """
    num_agents, num_states, num_actions = policies.shape
    global_policy = np.zeros((num_states, num_actions))
    
    for i in range(num_agents):
        weight = trust_weights[i]
        for s in prange(num_states):
            for a in range(num_actions):
                global_policy[s, a] += policies[i, s, a] * weight
                
    return global_policy

# ----------------------------------------------------------------------
# 2. Monitor de Governança (RULE 11)
# ----------------------------------------------------------------------

class SwarmGovernance:
    """
    Gerenciador de Governança do Enxame Soberano.
    Garante que apenas agentes confiáveis influenciem o modelo global.
    """
    def __init__(self, threshold=0.1):
        self.threshold = threshold # Peso mínimo para participar da fusão

    def audit_swarm(self, agents_data):
        """
        Audita o enxame e gera pesos de fusão.
        """
        # Simulação de extração de métricas (em prod viria do persistence/logs)
        stability = np.array([d['stability'] for d in agents_data])
        performance = np.array([d['performance'] for d in agents_data])
        uptime = np.array([d['uptime'] for d in agents_data])
        
        weights = calculate_trust_scores(stability, performance, uptime)
        
        # RULE 05: Hardening de Estado - Filtrar agentes abaixo do threshold
        weights[weights < self.threshold] = 0.0
        # Re-normalizar
        if np.sum(weights) > 0:
            weights = weights / np.sum(weights)
            
        return weights

if __name__ == '__main__':
    # Exemplo de Governança em Enxame de 3 Agentes
    agents = [
        {'name': 'Agent_A', 'stability': 0.95, 'performance': 0.92, 'uptime': 1.0},
        {'name': 'Agent_B', 'stability': 0.40, 'performance': 0.50, 'uptime': 0.2}, # Instável
        {'name': 'Agent_C', 'stability': 0.88, 'performance': 0.85, 'uptime': 0.8}
    ]
    
    gov = SwarmGovernance(threshold=0.15)
    weights = gov.audit_swarm(agents)
    
    print("📊 Pesos de Confiança do Enxame:")
    for i, a in enumerate(agents):
        print(f"  - {a['name']}: {weights[i]:.4f}")
    
    if weights[1] == 0:
        print("\n🛡️ RULE 05: Agent_B foi isolado por baixa estabilidade.")
