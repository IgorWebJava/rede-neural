import sys
import os
import numpy as np

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from persistence.db_manager import SovereignDBManager

def test_crud():
    print("🧪 Iniciando Teste de CRUD MySQL Soberano...")
    db = SovereignDBManager()
    
    # 1. Teste de Modelos
    test_weights = {"param_0": np.random.randn(5, 5)}
    db.save_model("V12_TEST", test_weights)
    loaded_weights = db.load_latest_model()
    assert np.allclose(test_weights["param_0"], loaded_weights["param_0"])
    print("✅ CRUD de Modelos: OK")
    
    # 2. Teste de Chat
    db.add_chat_entry("Oi", "Olá", "text", {"reason": "test"}, 0.99)
    history = db.get_chat_history(limit=1)
    assert len(history) > 0
    assert history[0]['user_input'] == "Oi"
    print("✅ CRUD de Chat: OK")
    
    # 3. Teste de Reputação
    db.upsert_reputation("Agent-Test", 0.9, 100.0, 50)
    print("✅ CRUD de Reputação: OK")
    
    print("\n🌟 Todos os testes de CRUD MySQL passaram!")

if __name__ == "__main__":
    try:
        test_crud()
    except Exception as e:
        print(f"❌ Falha no teste: {e}")
        sys.exit(1)
