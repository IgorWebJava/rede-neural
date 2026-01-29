# Exemplo de Kernel para Buffer de Replay de Experiência Priorizada (PER) Soberano

import numpy as np
from numba import jit

# O PER é crucial para o Lifelong-RL, pois armazena e amostra experiências
# de forma a mitigar o esquecimento catastrófico, priorizando transições raras ou críticas.

class PrioritizedReplayBufferSovereign:
    """
    Buffer de Replay Priorizado (PER) implementado com Numpy e Numba.
    Utiliza uma estrutura de Soma de Árvore (SumTree) simplificada para amostragem eficiente.
    """
    
    def __init__(self, capacity, alpha=0.6, epsilon=0.01):
        self.capacity = capacity
        self.alpha = alpha  # Exponente de prioridade (0.0 a 1.0)
        self.epsilon = epsilon # Pequeno valor para garantir que nenhuma transição tenha prioridade zero
        self.buffer = []
        self.priorities = np.zeros((capacity,), dtype=np.float32)
        self.next_idx = 0
        self.current_size = 0

    def add(self, experience, priority):
        """
        Adiciona uma nova experiência e sua prioridade ao buffer.
        """
        if self.current_size < self.capacity:
            self.buffer.append(experience)
            self.current_size += 1
        else:
            self.buffer[self.next_idx] = experience
            
        self.priorities[self.next_idx] = priority ** self.alpha
        self.next_idx = (self.next_idx + 1) % self.capacity

    @jit(nopython=True, cache=True)
    def _sample_indices_kernel(self, batch_size, priorities, total_priority):
        """
        Kernel otimizado para amostragem de índices com base na prioridade.
        """
        indices = np.zeros(batch_size, dtype=np.int32)
        segment = total_priority / batch_size
        
        for i in range(batch_size):
            a = segment * i
            b = segment * (i + 1)
            
            # Amostragem uniforme dentro de cada segmento
            s = np.random.uniform(a, b)
            
            # Busca linear simplificada (para manter a soberania e evitar estruturas complexas)
            current_sum = 0.0
            for j in range(len(priorities)):
                current_sum += priorities[j]
                if current_sum >= s:
                    indices[i] = j
                    break
        return indices

    def sample(self, batch_size, beta=0.4):
        """
        Amostra um batch de experiências com base na prioridade.
        """
        if self.current_size == 0:
            return [], [], []

        # Normaliza as prioridades para obter a probabilidade
        total_priority = self.priorities[:self.current_size].sum()
        
        # Amostragem otimizada
        indices = self._sample_indices_kernel(batch_size, self.priorities[:self.current_size], total_priority)
        
        # Cálculo dos pesos de importância (IS weights)
        probabilities = self.priorities[indices] / total_priority
        max_prob = self.priorities[:self.current_size].max() / total_priority
        weights = (max_prob * probabilities) ** (-beta)
        weights /= weights.max() # Normaliza os pesos
        
        experiences = [self.buffer[i] for i in indices]
        
        return experiences, indices, weights

    def update_priorities(self, indices, td_errors):
        """
        Atualiza as prioridades com base nos novos erros TD (Temporal Difference).
        """
        for idx, error in zip(indices, td_errors):
            self.priorities[idx] = (np.abs(error) + self.epsilon) ** self.alpha

# ----------------------------------------------------------------------
# Diretriz Crítica:
# O Agente RL-Homeostasis DEVE usar este buffer para armazenar e amostrar
# transições, priorizando aquelas com maior erro TD (maior surpresa/desvio).
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Exemplo de uso
    buffer = PrioritizedReplayBufferSovereign(capacity=10)
    
    # Adiciona experiências com prioridades variadas (erros TD)
    buffer.add("Exp 1 (Baixo Erro)", 0.1)
    buffer.add("Exp 2 (Médio Erro)", 0.5)
    buffer.add("Exp 3 (Alto Erro)", 2.0)
    
    # Amostra um batch (deve priorizar a Exp 3)
    experiences, indices, weights = buffer.sample(batch_size=2)
    
    print(f"Experiências Amostradas: {experiences}")
    print(f"Índices Amostrados: {indices}")
    print(f"Pesos de Importância (IS Weights): {weights}")
    
    # Simula novos erros TD e atualiza prioridades
    buffer.update_priorities(indices, [0.05, 3.0])
    print("\nPrioridades Atualizadas.")
