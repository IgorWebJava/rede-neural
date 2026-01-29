import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.tensor import Tensor
from persistence.manager import PersistenceManager
from memory.semantic import SemanticMemory
import numpy as np

def test_persistence_and_memory():
    print("🧪 Testando Persistência e Memória Semântica...")
    
    # 1. Testar Persistência
    pm = PersistenceManager(base_path="./tests/tmp_weights")
    p1 = Tensor([1.0, 2.0, 3.0], requires_grad=True)
    p2 = Tensor([[0.5, 0.1], [0.2, 0.8]], requires_grad=True)
    
    params = [p1, p2]
    pm.save_weights(params, "test_model.npz")
    
    # Modificar e Recarregar
    p1.data.fill(0.0)
    pm.load_weights(params, "test_model.npz")
    assert np.allclose(p1.data, [1.0, 2.0, 3.0]), "Falha ao recarregar pesos."
    print("✅ Persistência Validada!")
    
    # 2. Testar Memória Semântica
    mem = SemanticMemory(embedding_dim=4)
    mem.store([1, 0, 0, 0], {"info": "Conceito A"})
    mem.store([0, 1, 0, 0], {"info": "Conceito B"})
    
    # Query idêntica ao Conceito A
    results = mem.query([1, 0, 0, 0], top_k=1)
    print(f"DEBUG: Top result: {results[0][1]['info']} (Score: {results[0][0]:.4f})")
    assert results[0][1]['info'] == "Conceito A", f"Falha na busca semântica: esperado 'Conceito A', obtido '{results[0][1]['info']}'"
    print("✅ Memória Semântica Validada!")

if __name__ == "__main__":
    try:
        test_persistence_and_memory()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Limpeza
        import shutil
        if os.path.exists("./tests/tmp_weights"):
            shutil.rmtree("./tests/tmp_weights")
