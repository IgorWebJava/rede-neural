import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from training.trainer import SovereignMultimodalTrainer
from engine.tensor import Tensor

def run_demo():
    print("🧠 Iniciando Demonstração de Inferência Soberana...")
    
    # 1. Carregar Modelo (Instanciar e carregar pesos se existirem)
    model = SovereignMultimodalTrainer()
    
    # Simular entrada multimodal
    print("📥 Recebendo Dados Multimodais...")
    tokens = [2, 4, 7] # Ex: "O agente Manus"
    img = np.random.randn(1, 784) # Ex: Imagem de um sensor
    
    # 2. Forward Pass de Inferência
    text_feat = model.text_enc(tokens)
    text_agg = Tensor(text_feat.data.mean(axis=0, keepdims=True))
    vision_feat = model.vision_enc(Tensor(img))
    
    combined = text_agg + vision_feat
    prediction = model.head(combined)
    
    print(f"🔮 Resultado da Inferência: {prediction.data[0,0]:.4f}")
    print("✅ Demonstração Concluída.")

if __name__ == "__main__":
    run_demo()
