import matplotlib.pyplot as plt
import numpy as np

def plot_neural_health(history):
    """
    Gera visualização da saúde do motor neural (Loss, Gradientes, Entropia).
    'history' deve ser um dicionário com listas de métricas.
    """
    epochs = range(1, len(history['loss']) + 1)
    
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Loss
    plt.subplot(2, 2, 1)
    plt.plot(epochs, history['loss'], 'b-', label='Loss')
    plt.title('Estabilidade da Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Valor')
    plt.grid(True)
    
    # Subplot 2: Grad Norm (Detecção de Explosão)
    plt.subplot(2, 2, 2)
    plt.plot(epochs, history['grad_norm'], 'r-', label='Grad Norm')
    plt.axhline(y=1.0, color='k', linestyle='--', label='Threshold de Clipping')
    plt.title('Norma dos Gradientes (Sanidade)')
    plt.xlabel('Epoch')
    plt.grid(True)
    
    # Subplot 3: Entropia de Ativação
    plt.subplot(2, 2, 3)
    plt.plot(epochs, history['entropy'], 'g-', label='Entropy')
    plt.title('Entropia de Ativação (Capacidade)')
    plt.xlabel('Epoch')
    plt.grid(True)
    
    # Subplot 4: Learning Rate Dinâmico
    plt.subplot(2, 2, 4)
    plt.step(epochs, history['lr'], 'm-', label='LR')
    plt.title('Learning Rate (Auto-Ajuste)')
    plt.xlabel('Epoch')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('neural_health_report.png')
    print("📊 Relatório 'neural_health_report.png' gerado com sucesso.")

# Exemplo de uso:
# history = {'loss': [0.9, 0.7, 0.5], 'grad_norm': [0.1, 0.2, 0.15], 'entropy': [2.1, 2.0, 1.9], 'lr': [0.01, 0.01, 0.005]}
# plot_neural_health(history)
