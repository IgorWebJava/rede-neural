import sys
import os
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Adicionar raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from inference.engine import EdgeInferenceEngine
from persistence.manager import PersistenceManager

app = FastAPI(title="Sovereign Neural API V6", version="1.0.0")

# Inicializar Motor de Inferência
pm = PersistenceManager()
weights_path = "./persistence/weights/v4_industrial_checkpoint.npz"

# Mock de pesos para demonstração
weights = {
    'vision_w': np.random.randn(784, 32).astype(np.float32),
    'vision_b': np.zeros((1, 32), dtype=np.float32),
    'text_w': np.random.randn(32, 32).astype(np.float32),
    'text_b': np.zeros((1, 32), dtype=np.float32),
    'classifier_w': np.random.randn(64, 1).astype(np.float32),
    'classifier_b': np.zeros((1, 1), dtype=np.float32)
}

engine = EdgeInferenceEngine(weights)

class InferenceRequest(BaseModel):
    vision_input: list
    text_input: list

class InferenceResponse(BaseModel):
    prediction: float
    confidence: float
    latency_ms: float
    decision: str

@app.get("/health")
def health_check():
    """Verificação de saúde do sistema."""
    return {
        "status": "HEALTHY",
        "version": "V6-EDGE",
        "performance": engine.get_performance_report()
    }

@app.post("/infer", response_model=InferenceResponse)
def run_inference(req: InferenceRequest):
    """Executa uma inferência multimodal."""
    try:
        v_in = np.array(req.vision_input, dtype=np.float32).reshape(1, -1)
        t_in = np.array(req.text_input, dtype=np.float32).reshape(1, -1)
        
        pred, lat = engine.run_inference(v_in, t_in)
        
        pred_val = float(pred[0][0])
        confidence = abs(pred_val - 0.5) * 2  # Confiança baseada na distância de 0.5
        
        return InferenceResponse(
            prediction=pred_val,
            confidence=confidence,
            latency_ms=lat,
            decision="POSITIVO" if pred_val > 0.5 else "NEGATIVO"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stats")
def get_statistics():
    """Retorna estatísticas de performance."""
    return engine.get_performance_report()

@app.get("/")
def root():
    """Endpoint raiz com informações da API."""
    return {
        "name": "Sovereign Neural API V6",
        "version": "1.0.0",
        "endpoints": [
            "/health - Verificação de saúde",
            "/infer - Executar inferência",
            "/stats - Estatísticas de performance"
        ]
    }

if __name__ == "__main__":
    print("🚀 Iniciando Sovereign Neural API V6...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
