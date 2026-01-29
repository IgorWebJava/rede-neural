import numpy as np
import pickle
import hashlib
import os
from datetime import datetime

class SovereignPacker:
    """
    Empacotador de Modelo Soberano Compacto (.sov).
    Formato binário otimizado para implantação em borda (RULE 04).
    """
    def __init__(self, model_name="SovereignModelV6"):
        self.model_name = model_name

    def pack_to_sov(self, weights_dict, metadata=None, output_path="./persistence/model.sov"):
        """
        Serializa os pesos e metadados em um arquivo .sov compacto.
        """
        data = {
            "header": {
                "name": self.model_name,
                "version": "V6-EDGE",
                "timestamp": datetime.now().isoformat(),
                "format": "SOV-BINARY-V1"
            },
            "weights": weights_dict,
            "metadata": metadata or {}
        }
        
        # Gerar Checksum de Integridade (RULE 04)
        serialized_data = pickle.dumps(data)
        checksum = hashlib.sha256(serialized_data).hexdigest()
        
        final_packet = {
            "checksum": checksum,
            "payload": serialized_data
        }
        
        with open(output_path, 'wb') as f:
            pickle.dump(final_packet, f)
            
        print(f"📦 Modelo empacotado com sucesso: {output_path} (Checksum: {checksum[:8]})")
        return output_path

    def unpack_from_sov(self, sov_path):
        """
        Lê e valida um arquivo .sov.
        """
        if not os.path.exists(sov_path):
            raise FileNotFoundError(f"⚠️ Arquivo .sov não encontrado: {sov_path}")
            
        with open(sov_path, 'rb') as f:
            packet = pickle.load(f)
            
        # Validar Integridade
        current_checksum = hashlib.sha256(packet["payload"]).hexdigest()
        if current_checksum != packet["checksum"]:
            raise ValueError("🚨 ERRO DE INTEGRIDADE: O modelo .sov foi alterado ou está corrompido!")
            
        data = pickle.loads(packet["payload"])
        print(f"✅ Modelo {data['header']['name']} {data['header']['version']} carregado com sucesso.")
        return data["weights"], data["metadata"]

if __name__ == "__main__":
    # Teste de Empacotamento
    packer = SovereignPacker()
    weights = {"test_w": np.random.randn(10, 10)}
    path = packer.pack_to_sov(weights)
    packer.unpack_from_sov(path)
