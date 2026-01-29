import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.tensor import Tensor
from autograd.engine import Autograd
import numpy as np

def test_neural_core():
    print("🧪 Testando Núcleo Neural Soberano...")
    
    # 1. Setup de Tensores
    x = Tensor([[1.0, 2.0]], requires_grad=True)
    w = Tensor([[3.0], [4.0]], requires_grad=True)
    b = Tensor([[1.0]], requires_grad=True) # Garantir 2D para consistência
    
    # 2. Forward Pass (Linear: y = xW + b)
    y = x.matmul(w) + b
    
    # 3. Backward Pass
    y.backward()
    
    # 4. Verificação de Gradientes (RULE 10)
    # y = x1*w1 + x2*w2 + b
    # dy/dx1 = w1 = 3.0
    # dy/dx2 = w2 = 4.0
    expected_grad_x = np.array([[3.0, 4.0]])
    
    # dy/dw1 = x1 = 1.0
    # dy/dw2 = x2 = 2.0
    expected_grad_w = np.array([[1.0], [2.0]])
    
    # dy/db = 1.0
    expected_grad_b = np.array([[1.0]])
    
    assert np.allclose(x.grad, expected_grad_x), f"Grad X incorreto: {x.grad}"
    assert np.allclose(w.grad, expected_grad_w), f"Grad W incorreto: {w.grad}"
    assert np.allclose(b.grad, expected_grad_b), f"Grad B incorreto: {b.grad}"
    
    print("✅ Núcleo Neural Validado com Sucesso!")

if __name__ == "__main__":
    try:
        test_neural_core()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
