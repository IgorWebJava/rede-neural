import numpy as np
import json
import os
import hashlib
from datetime import datetime

class FeatureCache:
    """
    Cache de Features Multimodais (RULE 02 & 03).
    Evita reprocessamento de dados idênticos e economiza CPU.
    """
    def __init__(self, cache_dir="./persistence/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.memory_cache = {}

    def _generate_hash(self, data):
        """Gera um hash único para os dados de entrada."""
        if isinstance(data, np.ndarray):
            return hashlib.sha256(data.tobytes()).hexdigest()
        return hashlib.sha256(str(data).encode()).hexdigest()

    def get(self, data):
        h = self._generate_hash(data)
        return self.memory_cache.get(h)

    def set(self, data, features):
        h = self._generate_hash(data)
        self.memory_cache[h] = features
        # Limitar tamanho do cache em memória (LRU simples pode ser implementado)
        if len(self.memory_cache) > 1000:
            self.memory_cache.pop(next(iter(self.memory_cache)))

class LongTermMemory:
    """
    Memória de Longo Prazo Persistente (RULE 04).
    Armazena 'Wisdom' (conhecimento consolidado) em disco com integridade.
    """
    def __init__(self, db_path="./persistence/long_term_memory.json"):
        self.db_path = db_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {"entries": [], "version": "V4"}

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def commit_wisdom(self, vector, concept, importance=1.0):
        """Consolida um vetor de conhecimento na memória permanente."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "concept": concept,
            "vector": vector.tolist() if isinstance(vector, np.ndarray) else vector,
            "importance": importance
        }
        self.data["entries"].append(entry)
        self._save()
        print(f"🧠 Sabedoria Consolidada: {concept} (Importância: {importance})")

    def retrieve_by_concept(self, concept_query):
        """Busca simples por palavra-chave nos conceitos."""
        return [e for e in self.data["entries"] if concept_query.lower() in e["concept"].lower()]
