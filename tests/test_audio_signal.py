import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modalities.audio.processor import AudioProcessor, SignalUtils
from engine.tensor import Tensor
import numpy as np

def test_audio_processing():
    print("🧪 Testando Núcleo de Áudio e Processamento de Sinais...")
    
    # 1. Setup do Processador de Áudio
    # Entrada: 1024 amostras, Hidden: 128, Output: 16
    ap = AudioProcessor(1024, 128, 16)
    
    # Simular sinal senoidal com ruído
    t = np.linspace(0, 1, 1024)
    signal = np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(1024)
    signal_tensor = Tensor(signal.reshape(1, -1), requires_grad=True)
    
    # Forward Pass
    audio_features = ap(signal_tensor)
    
    # Verificação de Dimensões
    assert audio_features.data.shape == (1, 16), f"Shape de áudio incorreto: {audio_features.data.shape}"
    print("✅ Extração de Características de Áudio Validada!")
    
    # 2. Testar Utilitários de Sinal (FFT)
    spectrum = SignalUtils.simple_fft(signal)
    assert spectrum.shape[0] == (1024 // 2) + 1, "Tamanho do espectro incorreto"
    print("✅ Análise Espectral Soberana Validada!")

if __name__ == "__main__":
    try:
        test_audio_processing()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
