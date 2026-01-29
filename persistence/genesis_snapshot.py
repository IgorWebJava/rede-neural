import os
import shutil
import hashlib
from datetime import datetime

class GenesisSnapshot:
    """
    Sistema de Backup de Estado Global (RULE 04).
    V10: Cria um snapshot completo de pesos, reputação e logs éticos.
    Garante a continuidade da inteligência soberana.
    """
    def __init__(self, backup_dir="./persistence/snapshots"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def create_snapshot(self, version_tag="V10_FINAL"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"genesis_{version_tag}_{timestamp}"
        snapshot_path = os.path.join(self.backup_dir, snapshot_name)
        
        os.makedirs(snapshot_path)
        
        # Arquivos críticos para o estado global
        critical_files = [
            "./persistence/weights/v4_industrial_checkpoint.npz",
            "./persistence/swarm_reputation.json",
            "./persistence/ethics_ledger.json",
            "./persistence/wisdom_wisdom.json"
        ]
        
        for f in critical_files:
            if os.path.exists(f):
                shutil.copy(f, snapshot_path)
                
        # Gerar manifesto de integridade do snapshot
        manifest = f"Snapshot: {snapshot_name}\n"
        manifest += f"Timestamp: {timestamp}\n"
        manifest += "Files included:\n"
        
        for f in os.listdir(snapshot_path):
            f_path = os.path.join(snapshot_path, f)
            with open(f_path, 'rb') as rb:
                f_hash = hashlib.sha256(rb.read()).hexdigest()
            manifest += f"- {f}: {f_hash}\n"
            
        with open(os.path.join(snapshot_path, "manifest.txt"), "w") as f:
            f.write(manifest)
            
        print(f"🌟 Genesis Snapshot criado: {snapshot_path}")
        return snapshot_path
