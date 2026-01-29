import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.tensor import Tensor
from layers.embeddings import Embedding
from modalities.vision.processor import VisionProcessor
import numpy as np

def test_multimodal_integration():
    print("🧪 Testando Integração Multimodal (Texto + Visão)...")
    
    # 1. Texto: Embedding de 10 palavras para dim 8
    text_emb = Embedding(10, 8)
    text_input = [1, 3, 5] # Tokens
    text_features = text_emb(text_input)
    
    # 2. Visão: Imagem 28x28 (784) para dim 8
    vision_proc = VisionProcessor(784, 64, 8)
    image_input = Tensor(np.random.randn(1, 784))
    vision_features = vision_proc(image_input)
    
    # 3. Fusão Simples (Média das features)
    # Reduzir texto para (1, 8) via média
    text_mean_data = text_features.data.mean(axis=0, keepdims=True)
    text_features_agg = Tensor(text_mean_data, requires_grad=True)
    
    combined = text_features_agg + vision_features
    
    # 4. Verificação de Dimensões
    assert combined.data.shape == (1, 8), f"Shape de fusão incorreto: {combined.data.shape}"
    print("✅ Integração Multimodal Validada!")

if __name__ == "__main__":
    try:
        test_multimodal_integration()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
