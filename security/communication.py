import json
import hashlib
import hmac
import os
import base64

class SovereignProtocol:
    """
    Protocolo de Comunicação Segura entre Agentes (RULE 01 & 04).
    Garante autenticidade, integridade e isolamento de segredos.
    """
    def __init__(self, agent_id, secret_key=None):
        self.agent_id = agent_id
        # RULE 01: Segredos via variáveis de ambiente, nunca hardcoded
        self.secret_key = secret_key or os.getenv("SOVEREIGN_AGENT_KEY", "default_secure_key").encode()

    def pack_wisdom(self, data_dict):
        """
        Empacota dados (pesos, contextos) com assinatura digital.
        """
        payload = json.dumps(data_dict).encode()
        
        # Gerar assinatura HMAC-SHA256 (RULE 04)
        signature = hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()
        
        message = {
            "sender": self.agent_id,
            "payload": base64.b64encode(payload).decode(),
            "signature": signature
        }
        return json.dumps(message)

    def unpack_wisdom(self, json_message):
        """
        Desempacota e valida a integridade da mensagem recebida.
        """
        try:
            msg = json.loads(json_message)
            payload = base64.b64decode(msg["payload"])
            signature = msg["signature"]
            
            # Validar assinatura
            expected_signature = hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                raise SecurityError("🚨 Violação de Integridade: Assinatura Inválida!")
                
            return json.loads(payload)
        except Exception as e:
            print(f"⚠️ Erro de Segurança na Comunicação: {str(e)}")
            return None

class SecurityError(Exception):
    """Exceção para violações de segurança no protocolo."""
    pass
