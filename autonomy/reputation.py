import json
import os
from datetime import datetime

class AgentReputationSystem:
    """
    Sistema de Reputação e Créditos de Utilidade (RULE 05 & 06).
    Gerencia a confiança e o 'poder de voto' de cada agente no enxame.
    """
    def __init__(self, storage_path="./persistence/swarm_reputation.json"):
        self.storage_path = storage_path
        self.reputation_db = self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"agents": {}, "total_swarm_wisdom": 0}

    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.reputation_db, f, indent=4)

    def update_reputation(self, agent_id, quality_score, samples_processed):
        """
        Atualiza a reputação com base na qualidade da contribuição (V7).
        """
        if agent_id not in self.reputation_db["agents"]:
            self.reputation_db["agents"][agent_id] = {
                "score": 1.0,
                "credits": 10.0,
                "total_contributions": 0,
                "last_seen": ""
            }
            
        agent = self.reputation_db["agents"][agent_id]
        
        # Fórmula de Reputação: Média móvel ponderada
        alpha = 0.2
        agent["score"] = (1 - alpha) * agent["score"] + alpha * quality_score
        
        # Ganho de créditos baseado em utilidade real
        agent["credits"] += samples_processed * 0.1 * quality_score
        agent["total_contributions"] += 1
        agent["last_seen"] = datetime.now().isoformat()
        
        self.reputation_db["total_swarm_wisdom"] += samples_processed
        self._save()

    def get_voting_power(self, agent_id):
        """Retorna o peso do voto de um agente baseado em sua reputação."""
        agent = self.reputation_db["agents"].get(agent_id)
        if not agent:
            return 0.1 # Nós novos têm poder mínimo
        return max(0.1, agent["score"] * (1 + (agent["credits"] / 1000.0)))
