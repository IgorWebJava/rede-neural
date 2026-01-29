import numpy as np
import sys

def test_tensor_math():
    print("🧪 Iniciando Teste de Sanidade Matemática...")
    
    try:
        # Simular uma operação básica que o motor soberano deve suportar
        a = np.random.randn(10, 10)
        b = np.random.randn(10, 10)
        
        # Teste de MatMul (Soberania exige que o agente saiba implementar isso)
        res = np.dot(a, b)
        
        if res.shape == (10, 10):
            print("✅ Operações básicas de Array (Numpy) estão operacionais.")
            return True
    except Exception as e:
        print(f"❌ Falha no teste de sanidade: {e}")
        return False

if __name__ == "__main__":
    if test_tensor_math():
        sys.exit(0)
    else:
        sys.exit(1)
