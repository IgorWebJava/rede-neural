import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from autonomy.rl_agent import HomeostasisRLAgent
from autonomy.environment import HomeostasisEnvironment
from autonomy.monitor import NeuralPathologyMonitor
from autonomy.intervention import HomeostaticIntervention
from scripts.autonomy_logger import AutonomyLogger

def run_meta_optimization_loop(model, data_loader, epochs=10):
    """
    Loop de treinamento soberano com Meta-Otimização RL-Homeostasis.
    """
    # 1. Inicialização
    monitor = NeuralPathologyMonitor()
    intervention = HomeostaticIntervention()
    env = HomeostasisEnvironment(monitor)
    rl_agent = HomeostasisRLAgent(action_dim=len(env.actions))
    logger = AutonomyLogger(log_dir="./logs/meta_optimization")
    
    current_lr = 0.001
    
    print(f"Iniciando Treinamento com Meta-Otimização RL...")
    
    for epoch in range(epochs):
        # Estado Inicial
        state = env.get_state(current_lr)
        
        # Simulação de Passo de Treinamento
        # Em um cenário real, aqui ocorreria o forward/backward/optimizer.step()
        loss = np.random.random() * (1.0 / (epoch + 1)) # Simula convergência
        monitor.update_loss(loss)
        
        # 2. Decisão Autônoma (RL)
        action_idx = rl_agent.get_action(state)
        action_name = env.actions[action_idx]
        
        # 3. Execução da Intervenção
        if action_name == "REDUCE_LR":
            current_lr *= 0.9
        elif action_name == "CLIP_GRADIENTS":
            intervention.clip_gradients(model.parameters())
        elif action_name == "HEAL_LAYER":
            # Escolhe uma camada aleatória para simulação
            intervention.heal_layer(model)
            
        # 4. Observação e Recompensa
        next_state = env.get_state(current_lr)
        reward = env.calculate_reward(state, action_idx, next_state)
        
        # 5. Aprendizado do Agente RL
        rl_agent.update(state, action_idx, reward, next_state)
        
        # Log do Evento de Meta-Otimização
        logger.log_event("META_OPTIMIZATION_STEP", {
            "epoch": epoch,
            "action": action_name,
            "reward": reward,
            "current_lr": current_lr
        })
        
    print("Meta-Otimização concluída.")
    return rl_agent

if __name__ == "__main__":
    # Dummy model para teste
    from layers.linear import Linear
    model = Linear(10, 2)
    run_meta_optimization_loop(model, None, epochs=5)
