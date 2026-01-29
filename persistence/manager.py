import numpy as np
import os
import json
import hashlib
import pickle
from persistence.db_manager import SovereignDBManager

class PersistenceManager:
    """
    Gerenciador de Persistência Soberano (RULE 04).
    V12: Híbrido MySQL + Flat-Files para redundância e integridade industrial.
    """
    def __init__(self, base_path="./persistence/weights"):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.db = SovereignDBManager()

    def save_weights(self, parameters, filename="model_weights.npz"):
        """Salva uma lista de tensores em formato binário e no MySQL."""
        path = os.path.join(self.base_path, filename)
        weights_dict = {f"param_{i}": p.data for i, p in enumerate(parameters)}
        
        # 1. Salvar em arquivo (NPZ)
        np.savez(path, **weights_dict)
        
        # Gerar Checksum para integridade (RULE 04)
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        checksum = sha256_hash.hexdigest()
        with open(path + ".sha256", "w") as f:
            f.write(checksum)
            
        # 2. Salvar no MySQL (V12 CRUD)
        self.db.save_model(filename, weights_dict)
            
        print(f"💾 Pesos salvos em {path} e MySQL (Checksum: {checksum[:8]}...)")
        return checksum

    def load_weights(self, parameters, filename="model_weights.npz"):
        """Tenta carregar do MySQL, fallback para arquivo se falhar."""
        # Tentar MySQL primeiro (V12)
        db_weights = self.db.load_latest_model()
        if db_weights:
            for i, p in enumerate(parameters):
                key = f"param_{i}"
                if key in db_weights:
                    p.data = db_weights[key].copy()
            print("✅ Pesos carregados com sucesso do MySQL.")
            return

        # Fallback para arquivo
        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Arquivo de pesos não encontrado: {path}")
            
        data = np.load(path)
        for i, p in enumerate(parameters):
            key = f"param_{i}"
            if key in data:
                p.data = data[key].copy()
        print(f"✅ Fallback: Pesos carregados de {path}")

    def update_agent_reputation(self, agent_id, score, credits, contributions):
        """Atualiza reputação no MySQL (V12)."""
        self.db.upsert_reputation(agent_id, score, credits, contributions)
