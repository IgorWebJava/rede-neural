import os
import pickle
import time

def save_sovereign_checkpoint(model_state, epoch, loss, path="checkpoints/"):
    """
    Salva um checkpoint binário soberano com metadados de integridade.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        
    timestamp = int(time.time())
    filename = f"sovereign_v1_epoch{epoch}_loss{loss:.4f}_{timestamp}.skpt"
    full_path = os.path.join(path, filename)
    
    checkpoint = {
        "version": "2.6.0-ULTIMATE",
        "epoch": epoch,
        "loss": loss,
        "weights": model_state,
        "timestamp": timestamp
    }
    
    with open(full_path, "wb") as f:
        pickle.dump(checkpoint, f)
        
    print(f"💾 Checkpoint Soberano salvo: {full_path}")
    return full_path

def list_checkpoints(path="checkpoints/"):
    if not os.path.exists(path):
        print("📭 Nenhum checkpoint encontrado.")
        return []
    
    files = [f for f in os.listdir(path) if f.endswith(".skpt")]
    print(f"📂 Encontrados {len(files)} checkpoints soberanos.")
    for f in sorted(files):
        print(f"  - {f}")
    return files

if __name__ == "__main__":
    # Exemplo de teste
    dummy_state = {"layer1": [0.1, 0.2], "layer2": [0.5, 0.6]}
    save_sovereign_checkpoint(dummy_state, 10, 0.4567)
    list_checkpoints()
