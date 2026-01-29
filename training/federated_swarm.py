import numpy as np
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from training.trainer import SovereignMultimodalTrainerV4
from security.wisdom_protocol import WisdomPacker
from fusion.swarm_governance import SwarmConsensus

class SovereignFederatedSwarm:
    """
    Simulador de Aprendizado Federado em Enxame (V5).
    Demonstra a colaboração soberana entre múltiplos agentes virtuais.
    """
    def __init__(self, num_agents=3):
        print(f"🌐 Inicializando Enxame Soberano com {num_agents} Agentes...")
        self.agents = [SovereignMultimodalTrainerV4() for _ in range(num_agents)]
        self.packer = WisdomPacker(agent_id="Swarm-Controller")
        self.consensus = SwarmConsensus()

    def run_federated_round(self):
        """Executa uma rodada de treinamento local seguido de consenso global."""
        swarm_packets = []
        
        # 1. Treinamento Local Independente
        for i, agent in enumerate(self.agents):
            print(f"\n🤖 Agente {i+1} iniciando treinamento local...")
            agent.run_epoch(steps=3)
            
            # Extrair pesos para exportação
            weights = {
                "classifier_w": agent.classifier.weight.data,
                "classifier_b": agent.classifier.bias.data if agent.classifier.bias else np.zeros(1)
            }
            
            # 2. Empacotamento Seguro (V5)
            packet = self.packer.pack(weights, insights={"loss": np.mean(agent.dashboard.history["loss"][-3:])})
            swarm_packets.append(packet)
            print(f"✅ Agente {i+1}: Sabedoria assinada e pronta para o enxame.")

        # 3. Governança e Consenso (V5)
        print("\n⚖️ Iniciando Governança de Enxame (Consenso de Pesos)...")
        for packet in swarm_packets:
            data = self.packer.unpack(packet)
            if data:
                # Trust score baseado na inversa da perda (simulação)
                trust = 1.0 / (data["insights"]["loss"] + 1e-5)
                self.consensus.add_contribution(data["weights"], trust_score=trust)
        
        global_weights = self.consensus.merge()
        print("🤝 Consenso Global atingido com sucesso.")

        # 4. Distribuição da Sabedoria (Atualizar agentes locais)
        print("📡 Distribuindo Sabedoria Global para o enxame...")
        for agent in self.agents:
            agent.classifier.weight.data = global_weights["classifier_w"]
            if agent.classifier.bias:
                agent.classifier.bias.data = global_weights["classifier_b"]
        
        print("\n✨ Rodada Federada Concluída: Enxame Sincronizado.")

if __name__ == "__main__":
    swarm = SovereignFederatedSwarm(num_agents=2)
    swarm.run_federated_round()
