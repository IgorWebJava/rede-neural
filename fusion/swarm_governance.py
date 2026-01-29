import numpy as np
from engine.kernels import optimized_add, optimized_mul
from engine.tensor import Tensor

class SwarmConsensus:
    """
    Mecanismo de Governança de Enxame (RULE 06 & 11).
    Realiza a fusão soberana de modelos provenientes de diferentes agentes.
    """
    def __init__(self):
        self.participants = []

    def add_contribution(self, weights_dict, trust_score=1.0):
        """Adiciona uma contribuição de um agente ao pool de consenso."""
        # V5: Garantir que os pesos sejam arrays numpy para operações matemáticas
        sanitized_weights = {k: np.array(v) if not isinstance(v, np.ndarray) else v 
                            for k, v in weights_dict.items()}
        self.participants.append({
            "weights": sanitized_weights,
            "trust": trust_score
        })

    def merge(self):
        """
        Realiza a fusão ponderada (Consenso Federado) de todos os modelos.
        Retorna um novo dicionário de pesos unificado.
        """
        if not self.participants:
            return None
            
        total_trust = sum(p["trust"] for p in self.participants)
        if total_trust == 0:
            return self.participants[0]["weights"] # Fallback
            
        # Pegar as chaves do primeiro participante como referência
        keys = self.participants[0]["weights"].keys()
        merged_weights = {}
        
        for key in keys:
            # Inicializar acumulador com zeros da mesma forma que o peso original
            first_weight = self.participants[0]["weights"][key]
            acc_data = np.zeros_like(first_weight, dtype=np.float32)
            
            for p in self.participants:
                norm_trust = p["trust"] / total_trust
                # W_merged = sum(W_i * trust_i)
                acc_data += p["weights"][key] * norm_trust
            
            merged_weights[key] = acc_data
            
        return merged_weights

class ModelDistiller:
    """
    Utilitário para destilação de conhecimento (Teacher-Student).
    Permite que um modelo menor (Student) aprenda com o consenso (Teacher).
    """
    @staticmethod
    def calculate_soft_targets(logits, temperature=2.0):
        """Aplica Softmax com Temperatura para suavizar a política (RULE 09)."""
        exp_logits = np.exp(logits / temperature)
        return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
