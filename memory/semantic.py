import numpy as np

class SemanticMemory:
    """
    Memória Semântica Vetorial Soberana (RULE 03).
    Implementa busca por similaridade de cosseno em Python puro.
    """
    def __init__(self, embedding_dim):
        self.embedding_dim = embedding_dim
        self.storage = [] # Lista de tuplas (vetor, metadados)

    def store(self, vector, metadata):
        """Armazena um vetor de conhecimento com metadados."""
        if isinstance(vector, np.ndarray):
            vec = vector.flatten()
        else:
            vec = np.array(vector).flatten()
            
        if vec.shape[0] != self.embedding_dim:
            raise ValueError(f"Dimensão do vetor ({vec.shape[0]}) incompatível com a memória ({self.embedding_dim})")
            
        self.storage.append((vec, metadata))

    def query(self, query_vector, top_k=3):
        """Busca os conhecimentos mais similares via similaridade de cosseno."""
        if not self.storage:
            return []
            
        q_vec = np.array(query_vector).flatten()
        results = []
        
        for vec, meta in self.storage:
            # Similaridade de Cosseno: (A . B) / (||A|| * ||B||)
            dot_product = np.dot(q_vec, vec)
            norm_q = np.linalg.norm(q_vec)
            norm_v = np.linalg.norm(vec)
            
            similarity = dot_product / (norm_q * norm_v + 1e-9)
            results.append((similarity, meta))
            
        # Ordenar por similaridade (descendente)
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]
