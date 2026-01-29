import os
import time
import psutil
import numpy as np

class SovereignResourceManager:
    """
    Gerenciador de Recursos e Energia (RULE 02 & 05).
    Monitora CPU, Memória e Temperatura para ajustar a carga de treinamento.
    V8: Implementação de 'Thermal Throttling' soberano.
    """
    def __init__(self, cpu_threshold=80.0, mem_threshold=85.0):
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold
        self.history = []

    def get_system_load(self):
        """Coleta métricas reais do hardware."""
        cpu_usage = psutil.cpu_percent(interval=0.1)
        mem_usage = psutil.virtual_memory().percent
        
        # Simulação de temperatura (psutil.sensors_temperatures() pode não estar disponível em todos os OS)
        temp = 45.0 + (cpu_usage * 0.3) 
        
        return {
            "cpu": cpu_usage,
            "mem": mem_usage,
            "temp": temp,
            "timestamp": time.time()
        }

    def get_training_multiplier(self):
        """
        Calcula um multiplicador de intensidade para o treinamento.
        Retorna um valor entre 0.1 (mínimo) e 1.0 (máximo).
        """
        load = self.get_system_load()
        self.history.append(load)
        
        multiplier = 1.0
        
        # Reduzir intensidade se a CPU estiver sobrecarregada
        if load["cpu"] > self.cpu_threshold:
            multiplier *= 0.7
            
        # Reduzir drasticamente se a memória estiver no limite (RULE 05)
        if load["mem"] > self.mem_threshold:
            multiplier *= 0.5
            
        # Thermal Throttling
        if load["temp"] > 75.0:
            multiplier *= 0.3
            print(f"⚠️ Alerta Térmico: Reduzindo intensidade para {multiplier:.2f}")
            
        return max(0.1, multiplier)

    def optimize_batch_size(self, base_batch_size):
        """Sugere um tamanho de batch otimizado para os recursos atuais."""
        mult = self.get_training_multiplier()
        return max(1, int(base_batch_size * mult))
