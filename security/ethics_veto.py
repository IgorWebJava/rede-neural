import numpy as np
import hashlib
from datetime import datetime

class SovereignEthicsVeto:
    """
    Protocolo de Veto Ético Descentralizado (RULE 01 & 14).
    V9: Permite que o enxame bloqueie predições inseguras via consenso.
    """
    def __init__(self, swarm_size=3):
        self.swarm_size = swarm_size
        self.veto_log = []

    def request_clearance(self, agent_id, prediction_summary):
        """
        Simula um pedido de autorização ética ao enxame.
        """
        votes = []
        # Simulação de votação de outros agentes
        for i in range(self.swarm_size):
            # Lógica de decisão ética simulada
            # Em produção, cada agente rodaria sua própria auditoria local
            is_safe = np.random.rand() > 0.05 # 95% de chance de ser seguro
            votes.append(is_safe)
            
        consensus = sum(votes) > (self.swarm_size / 2)
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "prediction_hash": hashlib.sha256(str(prediction_summary).encode()).hexdigest(),
            "approved": consensus,
            "vote_count": f"{sum(votes)}/{self.swarm_size}"
        }
        self.veto_log.append(entry)
        
        if not consensus:
            print(f"🚨 VETO ÉTICO ATIVADO: Ação do agente {agent_id} bloqueada pelo enxame!")
            
        return consensus

    def get_ethics_report(self):
        total = len(self.veto_log)
        vetos = sum(1 for e in self.veto_log if not e["approved"])
        return {
            "total_requests": total,
            "vetos_active": vetos,
            "integrity_score": (1 - vetos/max(1, total)) * 100
        }
