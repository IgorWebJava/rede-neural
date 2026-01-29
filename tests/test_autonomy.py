import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.tensor import Tensor
from persistence.manager import PersistenceManager
from autonomy.homeostasis import PathologyMonitor, HomeostasisAgent
import numpy as np

def test_self_healing():
    print("🧪 Testando Autonomia e Self-Healing...")
    
    # 1. Setup
    pm = PersistenceManager(base_path="./tests/tmp_autonomy")
    monitor = PathologyMonitor(threshold_grad=10.0)
    agent = HomeostasisAgent(pm)
    
    p = Tensor([1.0, 2.0], requires_grad=True)
    params = [p]
    
    # Salvar estado inicial estável
    agent.record_stable_state(params, "stable.npz")
    
    # 2. Simular Explosão de Gradiente
    p.grad = np.array([100.0, 100.0]) # Acima do threshold 10.0
    status = monitor.check_health(params, loss_value=0.5)
    
    assert status["healthy"] == False, "O monitor deveria detectar gradiente explodido."
    
    # 3. Intervenção
    current_lr = 0.1
    new_lr, action = agent.intervene(status, params, current_lr)
    
    assert new_lr < current_lr, "O LR deveria ter sido reduzido."
    assert action == "LR_REDUCTION", f"Ação inesperada: {action}"
    print("✅ Self-Healing (Redução de LR) Validado!")
    
    # 4. Simular Falha Catastrófica (NaN)
    status_nan = {"healthy": False, "issues": ["CATASTROPHIC_LOSS_FAILURE"]}
    p.data.fill(np.nan)
    
    new_lr, action = agent.intervene(status_nan, params, new_lr)
    assert action == "STATE_RESTORATION", f"Deveria ter restaurado o estado. Ação: {action}"
    assert not np.isnan(p.data).any(), "Os dados ainda contêm NaNs após restauração."
    
    print("✅ Self-Healing (Restauração de Estado) Validado!")

if __name__ == "__main__":
    try:
        test_self_healing()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        import shutil
        if os.path.exists("./tests/tmp_autonomy"):
            shutil.rmtree("./tests/tmp_autonomy")
