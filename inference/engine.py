import numpy as np
import time
from engine.kernels import optimized_matmul, optimized_add, optimized_relu

class EdgeInferenceEngine:
    """
    Motor de Inferência Otimizado para Borda (RULE 02 & 09).
    Focado em baixa latência e consumo mínimo de memória, removendo overhead de autograd.
    """
    def __init__(self, model_params):
        # model_params: dicionário de arrays numpy (pesos consolidados)
        self.params = model_params
        self.stats = {"latency_ms": [], "throughput": 0}

    def _forward_linear(self, x, weight, bias=None):
        """Execução linear otimizada sem rastreamento de gradiente."""
        out = optimized_matmul(x, weight)
        if bias is not None:
            out = optimized_add(out, bias)
        return out

    def run_inference(self, vision_data, text_data):
        """
        Executa uma passagem de inferência multimodal completa.
        """
        start_time = time.time()
        
        # 1. Processamento de Visão (Simplificado para Inferência)
        # Assume-se que vision_data já está normalizado
        v_h = optimized_relu(self._forward_linear(vision_data, self.params['vision_w'], self.params['vision_b']))
        
        # 2. Processamento de Texto (Simplificado)
        t_h = optimized_relu(self._forward_linear(text_data, self.params['text_w'], self.params['text_b']))
        
        # 3. Fusão de Borda (Concatenação Simples para velocidade na V6)
        fused = np.concatenate([v_h, t_h], axis=-1)
        
        # 4. Classificação Final
        logits = self._forward_linear(fused, self.params['classifier_w'], self.params['classifier_b'])
        prediction = 1.0 / (1.0 + np.exp(-logits)) # Sigmoid manual
        
        latency = (time.time() - start_time) * 1000
        self.stats["latency_ms"].append(latency)
        
        return prediction, latency

    def get_performance_report(self):
        avg_latency = np.mean(self.stats["latency_ms"]) if self.stats["latency_ms"] else 0
        return {
            "avg_latency_ms": avg_latency,
            "p95_latency_ms": np.percentile(self.stats["latency_ms"], 95) if self.stats["latency_ms"] else 0,
            "status": "OPTIMIZED" if avg_latency < 10 else "HEAVY"
        }
