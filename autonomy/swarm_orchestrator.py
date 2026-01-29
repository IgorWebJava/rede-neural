import os
import subprocess
import sys
import shutil

class SwarmOrchestrator:
    """
    Orquestrador de Enxame Autônomo (RULE 01 & 12).
    Facilita a expansão do enxame através de auto-replicação de nós de treinamento.
    """
    def __init__(self, swarm_root="./swarm_nodes"):
        self.swarm_root = swarm_root
        os.makedirs(swarm_root, exist_ok=True)

    def spawn_node(self, node_id):
        """
        Cria um novo nó de enxame independente (Isolamento de Contexto - RULE 03).
        """
        node_path = os.path.join(self.swarm_root, f"node_{node_id}")
        if os.path.exists(node_path):
            print(f"⚠️ Nó {node_id} já existe. Ignorando spawn.")
            return False
            
        print(f"🧬 Clonando estrutura soberana para o Nó {node_id}...")
        
        # Copiar apenas os diretórios necessários para execução (Core & Engine)
        dirs_to_copy = ['engine', 'layers', 'modalities', 'fusion', 'training', 'persistence', 'security', 'autograd', 'autonomy']
        os.makedirs(node_path)
        
        for d in dirs_to_copy:
            src = os.path.join("./", d)
            dst = os.path.join(node_path, d)
            if os.path.exists(src):
                shutil.copytree(src, dst)
        
        # Criar script de inicialização do nó
        init_script = f"""
import sys
import os
sys.path.append(os.getcwd())
from training.trainer import SovereignMultimodalTrainerV4
print('🤖 Nó {node_id} ONLINE e pronto para o Enxame.')
trainer = SovereignMultimodalTrainerV4()
trainer.run_epoch(steps=5)
"""
        with open(os.path.join(node_path, "start_node.py"), "w") as f:
            f.write(init_script)
            
        print(f"✅ Nó {node_id} orquestrado com sucesso em {node_path}")
        return True

    def health_check_all(self):
        """Verifica a integridade de todos os nós ativos no enxame."""
        nodes = [d for d in os.listdir(self.swarm_root) if d.startswith("node_")]
        print(f"🔍 Auditoria de Enxame: {len(nodes)} nós detectados.")
        return nodes
