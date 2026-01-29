import numpy as np
from engine.tensor import Tensor

class QPSOOptimizer:
    """
    Otimizador de Enxame de Partículas com Inspiração Quântica (RULE 09).
    V8: Utiliza funções de onda delta para exploração global do espaço de pesos.
    Não utiliza gradientes, ideal para escapar de mínimos locais complexos.
    """
    def __init__(self, parameters, population_size=20, g=1.0):
        self.params = parameters
        self.pop_size = population_size
        self.g = g # Parâmetro de controle de contração-expansão
        
        # Inicializar população de partículas para cada parâmetro
        self.population = []
        self.pbest = [] # Melhores posições individuais
        self.gbest = None # Melhor posição global
        
        for p in self.params:
            shape = (population_size,) + p.data.shape
            pos = np.random.uniform(-1, 1, shape).astype(np.float32)
            self.population.append(pos)
            self.pbest.append(pos.copy())
            
    def step(self, fitness_fn):
        """
        Executa uma iteração do QPSO.
        fitness_fn: função que recebe os parâmetros e retorna o valor de perda (menor é melhor).
        """
        current_fitness = np.zeros((self.pop_size,))
        
        # 1. Avaliar fitness para cada partícula
        for i in range(self.pop_size):
            # Aplicar pesos da partícula i temporariamente
            original_weights = []
            for j, p in enumerate(self.params):
                original_weights.append(p.data.copy())
                p.data = self.population[j][i]
            
            current_fitness[i] = fitness_fn()
            
            # Restaurar e atualizar pbest
            # (Simplificação: assume-se que pbest_fitness é rastreado)
            # Na implementação real, precisaríamos armazenar o histórico de fitness por partícula
            
        # 2. Calcular mbest (Média dos pbest)
        mbest = [np.mean(pb, axis=0) for pb in self.pbest]
        
        # 3. Atualizar posições via tunelamento quântico
        for j, p in enumerate(self.params):
            for i in range(self.pop_size):
                phi = np.random.uniform(0, 1, p.data.shape)
                p_local = phi * self.pbest[j][i] + (1 - phi) * self.gbest_data[j]
                
                u = np.random.uniform(0, 1, p.data.shape)
                L = self.g * np.abs(mbest[j] - self.population[j][i])
                
                # Equação de posição quântica
                if np.random.rand() > 0.5:
                    self.population[j][i] = p_local + L * np.log(1.0 / u)
                else:
                    self.population[j][i] = p_local - L * np.log(1.0 / u)
                    
        # Nota: Esta é uma versão conceitual soberana do QPSO integrada ao motor.
