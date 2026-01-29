import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from security.communication import SovereignProtocol, SecurityError
import json

def test_secure_communication():
    print("🧪 Testando Comunicação Segura entre Agentes...")
    
    # 1. Setup de Agentes
    key = b"super_secret_swarm_key_2026"
    agent_a = SovereignProtocol(agent_id="AGENT_ALPHA", secret_key=key)
    agent_b = SovereignProtocol(agent_id="AGENT_BETA", secret_key=key)
    
    # 2. Transmissão de Sabedoria
    wisdom_data = {"weights_hash": "abc123def", "status": "stable", "consensus_vote": True}
    encoded_msg = agent_a.pack_wisdom(wisdom_data)
    
    print(f"📡 Mensagem Codificada: {encoded_msg[:60]}...")
    
    # 3. Recepção e Validação
    decoded_data = agent_b.unpack_wisdom(encoded_msg)
    
    assert decoded_data == wisdom_data, "Dados decodificados divergem do original"
    print("✅ Integridade e Autenticidade Validadas!")
    
    # 4. Testar Ataque de Interceptação (Modificação de Dados)
    tampered_msg = json.loads(encoded_msg)
    tampered_msg["payload"] = "bWFsZmljaW91cy1kYXRh" # "malficious-data" em base64
    tampered_json = json.dumps(tampered_msg)
    
    print("🧪 Simulando ataque de modificação de payload...")
    result = agent_b.unpack_wisdom(tampered_json)
    
    assert result is None, "O sistema deveria ter bloqueado a mensagem adulterada"
    print("✅ Bloqueio de Mensagem Adulterada Validado!")

if __name__ == "__main__":
    try:
        test_secure_communication()
    except Exception as e:
        print(f"❌ Falha no Teste: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
