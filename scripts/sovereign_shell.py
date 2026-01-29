import sys
import os
import numpy as np
import argparse

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from inference.engine import EdgeInferenceEngine
from persistence.manager import PersistenceManager

def main():
    parser = argparse.ArgumentParser(description="Sovereign Shell V6 - Interface de Comando Neural")
    parser.add_argument("--weights", type=str, help="Caminho para os pesos do modelo (.npz)")
    args = parser.parse_args()

    print("""
    =========================================
      🧠 SOVEREIGN SHELL V6 - ACTIVE
    =========================================
    Interface de Interação Direta com o Enxame
    """)

    # Carregar Pesos
    pm = PersistenceManager()
    weights_path = args.weights or "./persistence/weights/v4_industrial_checkpoint.npz"
    
    if not os.path.exists(weights_path):
        print(f"⚠️ Erro: Pesos não encontrados em {weights_path}")
        # Mock de pesos para demonstração se não existir
        weights = {
            'vision_w': np.random.randn(784, 32), 'vision_b': np.zeros((1, 32)),
            'text_w': np.random.randn(32, 32), 'text_b': np.zeros((1, 32)),
            'classifier_w': np.random.randn(64, 1), 'classifier_b': np.zeros((1, 1))
        }
    else:
        weights = pm.load_weights(weights_path)
        print(f"✅ Pesos carregados: {weights_path}")

    engine = EdgeInferenceEngine(weights)

    while True:
        try:
            print("\n--- Nova Inferência ---")
            cmd = input("sovereign> ").strip().lower()
            
            if cmd in ['exit', 'quit', 'q']:
                break
            elif cmd == 'status':
                print(f"📊 Performance: {engine.get_performance_report()}")
                continue
            
            # Simulação de entrada multimodal via shell
            print("📥 Processando Entrada Multimodal Simulada...")
            v_in = np.random.randn(1, 784)
            t_in = np.random.randn(1, 32)
            
            pred, lat = engine.run_inference(v_in, t_in)
            
            print(f"🔮 Predição: {'POSITIVA' if pred > 0.5 else 'NEGATIVA'} ({pred[0][0]:.4f})")
            print(f"⚡ Latência: {lat:.2f}ms")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Erro: {str(e)}")

    print("\nEncerrando Sovereign Shell. Soberania Preservada.")

if __name__ == "__main__":
    main()
