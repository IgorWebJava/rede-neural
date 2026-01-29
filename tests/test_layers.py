import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.tensor import Tensor
from layers.base import Linear, ReLU
from autograd.engine import Autograd
import numpy as np

def test_mlp_flow():
    print("🧪 Testando Fluxo de Camadas Neurais (MLP)...")
    
    # 1. Definir Modelo Simples
    layer1 = Linear(2, 4)
    relu = ReLU()
    layer2 = Linear(4, 1)
    
    params = layer1.parameters() + layer2.parameters()
    
    # 2. Dados de Entrada
    x = Tensor([[0.5, -0.2]])
    target = Tensor([[1.0]])
    
    # 3. Forward Pass
    h1 = relu(layer1(x))
    output = layer2(h1)
    
    # 4. Cálculo de Loss (MSE Simples: (out - target)^2)
    diff = output + (target * -1.0)
    # Implementação manual de square para o teste
    loss = Tensor(diff.data**2, _children=(diff,), _op='MSE', requires_grad=True)
    def _backward():
        diff.grad += 2.0 * diff.data * loss.grad
    loss._backward = _backward
    
    # 5. Backward Pass
    Autograd.zero_grad(params)
    loss.backward()
    
    # 6. Optimizer Step
    old_weight = layer1.weight.data.copy()
    Autograd.step(params, lr=0.1)
    
    # 7. Verificação (RULE 10)
    assert not np.allclose(old_weight, layer1.weight.data), "Os pesos deveriam ter mudado após o step."
    print("✅ Camadas Neurais e Fluxo de Treino Validados!")

if __name__ == "__main__":
    try:
        test_mlp_flow()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
