# Exemplo de Kernel para Loss de Destilação de Política (KL Divergence)

import numpy as np
from numba import jit

# A Loss de Destilação é usada para treinar um Agente Aluno a imitar a política
# de um Agente Professor, acelerando o aprendizado.

@jit(nopython=True, cache=True)
def kl_divergence_kernel(p, q):
    """
    Calcula a Divergência de Kullback-Leibler (KL(P || Q)).
    P é a distribuição do Professor (Soft Targets).
    Q é a distribuição do Aluno (Softmax da Q-Table do Aluno).
    
    KL(P || Q) = sum(P * log(P / Q))
    """
    # Adiciona um pequeno epsilon para evitar log(0)
    epsilon = 1e-9
    q = np.maximum(q, epsilon)
    p = np.maximum(p, epsilon)
    
    return np.sum(p * np.log(p / q))

@jit(nopython=True, cache=True)
def softmax_with_temperature_kernel(q_values, temperature):
    """
    Calcula a Softmax com Temperatura (T) para gerar Soft Targets.
    """
    scaled_q = q_values / temperature
    exp_q = np.exp(scaled_q - np.max(scaled_q)) # Estabilidade numérica
    return exp_q / np.sum(exp_q)

def calculate_distillation_loss(teacher_q_values, student_q_values, temperature, alpha):
    """
    Calcula a Loss de Destilação Total.
    """
    # 1. Soft Targets do Professor
    teacher_policy = softmax_with_temperature_kernel(teacher_q_values, temperature)
    
    # 2. Política do Aluno
    student_policy = softmax_with_temperature_kernel(student_q_values, temperature)
    
    # 3. Loss de Destilação (KL Divergence)
    kl_loss = kl_divergence_kernel(teacher_policy, student_policy)
    
    # 4. Loss de Treinamento Normal (ex: MSE entre Q-values)
    # Placeholder para a Loss normal (deve ser calculada separadamente)
    normal_loss = np.mean((teacher_q_values - student_q_values)**2) 
    
    # 5. Loss Total
    total_loss = alpha * normal_loss + (1 - alpha) * kl_loss
    
    return total_loss, kl_loss

# ----------------------------------------------------------------------
# Diretriz Crítica:
# O Agente Aluno DEVE usar esta Loss para atualizar sua Q-Table,
# imitando a política do Professor.
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Exemplo de uso
    
    # Valores Q do Professor (política forte)
    teacher_q = np.array([0.1, 0.9, 0.0])
    
    # Valores Q do Aluno (política fraca)
    student_q = np.array([0.3, 0.3, 0.3])
    
    # Hiperparâmetros
    T = 2.0 # Temperatura de suavização
    alpha = 0.5 # Ponderação da Loss normal
    
    total_loss, kl_loss = calculate_distillation_loss(teacher_q, student_q, T, alpha)
    
    print(f"Loss de Destilação (KL): {kl_loss:.4f}")
    print(f"Loss Total (com alpha={alpha}): {total_loss:.4f}")
    
    # Se o aluno for treinado com esta Loss, seus Q-values se moverão
    # para imitar a política do professor (priorizar a Ação 1).
