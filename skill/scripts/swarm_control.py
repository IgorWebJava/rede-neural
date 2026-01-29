import os
import sys
import json
import time

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autonomy.reputation import AgentReputationSystem

class SwarmControlDashboard:
    """
    Dashboard de Governança Global do Enxame (RULE 14).
    Visualização de reputação, créditos e saúde do enxame descentralizado.
    """
    def __init__(self):
        self.reputation_sys = AgentReputationSystem()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self):
        self.clear()
        db = self.reputation_sys.reputation_db
        
        print("=" * 60)
        print(" 🌐 SOVEREIGN SWARM CONTROL V7 - GOVERNANCE ACTIVE")
        print(f" Total Swarm Wisdom: {db.get('total_swarm_wisdom', 0)} samples")
        print("=" * 60)
        
        agents = db.get("agents", {})
        if not agents:
            print(" [!] Nenhum agente ativo detectado no enxame.")
        else:
            print(f"{'AGENT_ID':<15} | {'SCORE':<8} | {'CREDITS':<10} | {'VOTING_POWER':<12}")
            print("-" * 60)
            for aid, data in agents.items():
                v_power = self.reputation_sys.get_voting_power(aid)
                print(f"{aid:<15} | {data['score']:<8.4f} | {data['credits']:<10.2f} | {v_power:<12.4f}")
        
        print("\n" + "=" * 60)
        print(" [R]efresh | [B]oot Node | [C]onsensus Audit | [Q]uit")
        print("=" * 60)

if __name__ == "__main__":
    # Simulação de dados para visualização
    rep = AgentReputationSystem()
    rep.update_reputation("Agent-Alpha", 0.95, 1000)
    rep.update_reputation("Agent-Beta", 0.82, 500)
    
    dash = SwarmControlDashboard()
    dash.render()
