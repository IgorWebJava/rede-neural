import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from layers.attention import CrossAttention
from modalities.code.processor import CodeProcessor
from modalities.audio.processor import AudioProcessor
from security.communication import SovereignProtocol

def test_v2_expansion_harmony():
    print("🧪 Testando Harmonia da Expansão V2.0 (Fase 8)...")
    
    # 1. Validar Atenção Cruzada
    from engine.tensor import Tensor
    attn = CrossAttention(16, 16, 8)
    q = Tensor(np.random.randn(1, 16))
    kv = Tensor(np.random.randn(2, 16))
    out_attn = attn(q, kv)
    print(f"  - Cross-Attention: OK (Shape {out_attn.data.shape})")
    
    # 2. Validar Núcleo de Código
    cp = CodeProcessor(10, 8, 16)
    out_code = cp([1, 2, 3])
    print(f"  - Code Processor: OK (Shape {out_code.data.shape})")
    
    # 3. Validar Núcleo de Áudio
    ap = AudioProcessor(128, 32, 8)
    out_audio = ap(np.random.randn(1, 128))
    print(f"  - Audio Processor: OK (Shape {out_audio.data.shape})")
    
    # 4. Validar Segurança
    sp = SovereignProtocol(agent_id="VALIDATOR")
    msg = sp.pack_wisdom({"status": "certified"})
    assert sp.unpack_wisdom(msg)["status"] == "certified"
    print("  - Sovereign Security: OK")

    print("\n✅ Expansão V2.0 validada com sucesso em todos os núcleos!")

if __name__ == "__main__":
    try:
        test_v2_expansion_harmony()
    except Exception as e:
        print(f"❌ Falha na Integração V2: {str(e)}")
        sys.exit(1)
