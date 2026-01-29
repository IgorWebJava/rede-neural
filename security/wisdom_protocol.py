import numpy as np
import json
import hashlib
import hmac
import os
import base64
from datetime import datetime

class WisdomPacker:
    """
    Empacotador de Sabedoria Soberana (RULE 01, 04 & 06).
    Garante que pesos e insights sejam exportados com assinatura digital e metadados de proveniência.
    """
    def __init__(self, agent_id, secret_key=None):
        self.agent_id = agent_id
        # RULE 01: Segredos via variáveis de ambiente
        self.secret_key = secret_key or os.getenv("SOVEREIGN_SWARM_KEY", "swarm_secret_2026").encode()

    def _sign(self, payload):
        """Gera assinatura HMAC-SHA256 para o payload."""
        return hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()

    def pack(self, weights_dict, insights=None):
        """
        Empacota pesos e insights em um formato serializável e assinado.
        """
        # Converter arrays numpy para listas para JSON
        serializable_weights = {k: v.tolist() if isinstance(v, np.ndarray) else v 
                               for k, v in weights_dict.items()}
        
        data = {
            "version": "V5-SWARM",
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "weights": serializable_weights,
            "insights": insights or {},
            "checksum": hashlib.sha256(json.dumps(serializable_weights).encode()).hexdigest()
        }
        
        payload = json.dumps(data).encode()
        signature = self._sign(payload)
        
        packet = {
            "payload": base64.b64encode(payload).decode(),
            "signature": signature
        }
        return json.dumps(packet)

    def unpack(self, json_packet):
        """
        Desempacota e valida a integridade e autenticidade do pacote de sabedoria.
        """
        try:
            packet = json.loads(json_packet)
            payload_bytes = base64.b64decode(packet["payload"])
            signature = packet["signature"]
            
            # Validar assinatura (RULE 04)
            if not hmac.compare_digest(signature, self._sign(payload_bytes)):
                raise SecurityError("🚨 Falha de Autenticidade: Assinatura do Enxame Inválida!")
                
            data = json.loads(payload_bytes)
            
            # Validar integridade dos dados (Checksum)
            current_checksum = hashlib.sha256(json.dumps(data["weights"]).encode()).hexdigest()
            if current_checksum != data["checksum"]:
                raise SecurityError("🚨 Falha de Integridade: Checksum dos pesos corrompido!")
                
            return data
        except Exception as e:
            print(f"⚠️ Erro no Protocolo de Sabedoria: {str(e)}")
            return None

class SecurityError(Exception):
    pass
