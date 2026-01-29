from layers.base import Module, Linear, ReLU
from engine.tensor import Tensor
import numpy as np

class AudioProcessor(Module):
    """
    Processador de Áudio e Sinais Soberano (RULE 06 & 09).
    V4: Especializado em extrair características espectrais via FFT.
    """
    def __init__(self, input_bins, hidden_dim, output_dim):
        # input_bins: número de bins de frequência esperados
        self.fc_signal = Linear(input_bins, hidden_dim)
        self.relu = ReLU()
        self.fc_features = Linear(hidden_dim, output_dim)

    def forward(self, waveform):
        """
        waveform: Array contendo a amplitude do sinal no tempo.
        Transforma em domínio de frequência antes do processamento neural.
        """
        # 1. Pré-processamento Soberano: FFT e Normalização
        if isinstance(waveform, Tensor):
            waveform = waveform.data
        
        # FFT Real (RULE 09)
        fft_data = np.abs(np.fft.rfft(waveform))
        
        # Ajuste de bins para o tamanho da camada linear
        n_bins = self.fc_signal.weight.data.shape[0]
        if len(fft_data) > n_bins:
            fft_data = fft_data[:n_bins]
        elif len(fft_data) < n_bins:
            fft_data = np.pad(fft_data, (0, n_bins - len(fft_data)))
            
        # Normalização Z-score soberana
        fft_norm = (fft_data - np.mean(fft_data)) / (np.std(fft_data) + 1e-9)
        
        x = Tensor([fft_norm], requires_grad=True)
        
        # 2. Extração de Características Neurais
        h = self.relu(self.fc_signal(x))
        return self.fc_features(h)

    def parameters(self):
        return self.fc_signal.parameters() + self.fc_features.parameters()

class SignalUtils:
    """
    Utilitários soberanos para processamento de sinais digitais.
    """
    @staticmethod
    def simple_fft(signal):
        """Implementação simplificada de magnitude espectral (RULE 09)."""
        return np.abs(np.fft.rfft(signal))
