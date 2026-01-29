import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.tensor import Tensor
from layers.attention import CrossAttention
import numpy as np

def test_cross_attention():
    print("🧪 Testando Mecanismo de Cross-Attention Soberano...")
    
    # Dimensões: Query(Text)=16, Key/Value(Vision)=32, Head=8
    attn = CrossAttention(16, 32, 8)
    
    # Entradas
    q = Tensor(np.random.randn(1, 16), requires_grad=True)
    kv = Tensor(np.random.randn(4, 32), requires_grad=True) # 4 "patches" de imagem
    
    # Forward
    out = attn(q, kv)
    
    # Backward
    out.backward()
    
    # Verificações
    assert out.data.shape == (1, 8), f"Shape de saída incorreto: {out.data.shape}"
    assert q.grad is not None, "Gradiente de Q não foi calculado"
    assert kv.grad is not None, "Gradiente de KV não foi calculado"
    
    print("✅ Cross-Attention Validado!")

if __name__ == "__main__":
    try:
        test_cross_attention()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
