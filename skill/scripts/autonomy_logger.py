import time
import json
import os
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        return super(NumpyEncoder, self).default(obj)

class AutonomyLogger:
    """
    Logger de Autonomia Soberano.
    Registra todas as decisões e intervenções autônomas para auditoria futura.
    """
    def __init__(self, log_dir="./logs/autonomy"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = os.path.join(log_dir, f"autonomy_{int(time.time())}.jsonl")

    def log_event(self, event_type, details):
        """
        Registra um evento de autonomia em formato JSONL.
        """
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "unix_time": time.time(),
            "event": event_type,
            "details": details
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry, cls=NumpyEncoder) + "\n")
            
        print(f"[AUTONOMY] {event_type}: {details}")

    def get_summary(self):
        """Retorna um resumo das intervenções registradas."""
        # Implementação futura de análise de logs
        pass
