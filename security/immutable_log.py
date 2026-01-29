import json
import hashlib
import os
from datetime import datetime

class ImmutableEthicsLog:
    """
    Log de Governança Ética Imutável (RULE 04 & 14).
    V9: Utiliza encadeamento de hashes (Hash-Chaining) para garantir que o 
    histórico de decisões éticas não possa ser alterado.
    """
    def __init__(self, log_path="./persistence/ethics_ledger.json"):
        self.log_path = log_path
        self.ledger = self._load()

    def _load(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as f:
                return json.load(f)
        return {"entries": [], "last_hash": "SOVEREIGN_GENESIS"}

    def add_entry(self, event_type, details):
        """
        Adiciona uma entrada ao ledger com encadeamento de hash.
        """
        timestamp = datetime.now().isoformat()
        prev_hash = self.ledger["last_hash"]
        
        entry_data = {
            "timestamp": timestamp,
            "event": event_type,
            "details": details,
            "prev_hash": prev_hash
        }
        
        # Calcular hash da entrada atual
        entry_json = json.dumps(entry_data, sort_keys=True).encode()
        current_hash = hashlib.sha256(entry_json).hexdigest()
        
        entry_data["hash"] = current_hash
        self.ledger["entries"].append(entry_data)
        self.ledger["last_hash"] = current_hash
        
        self._save()
        return current_hash

    def _save(self):
        with open(self.log_path, 'w') as f:
            json.dump(self.ledger, f, indent=4)

    def verify_integrity(self):
        """
        Verifica se a corrente de hashes foi quebrada.
        """
        prev_hash = "SOVEREIGN_GENESIS"
        for entry in self.ledger["entries"]:
            # Verificar se o prev_hash bate
            if entry["prev_hash"] != prev_hash:
                return False, f"🚨 Corrente quebrada no timestamp {entry['timestamp']}"
            
            # Recalcular hash para validar imutabilidade
            check_data = {k: v for k, v in entry.items() if k != "hash"}
            check_json = json.dumps(check_data, sort_keys=True).encode()
            if hashlib.sha256(check_json).hexdigest() != entry["hash"]:
                return False, f"🚨 Conteúdo alterado no timestamp {entry['timestamp']}"
                
            prev_hash = entry["hash"]
            
        return True, "✅ Integridade do Ledger Ético Confirmada."
