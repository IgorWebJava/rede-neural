import numpy as np

class SovereignCompressor:
    """
    Compressor de Modelos Soberano (RULE 09).
    V8: Utiliza Decomposição em Valores Singulares (SVD) para reduzir rank de matrizes.
    Permite reduzir o tamanho do modelo em até 80% com perda mínima de precisão.
    """
    @staticmethod
    def compress_matrix(matrix, ratio=0.5):
        """
        Comprime uma matriz 2D mantendo apenas os top-K valores singulares.
        matrix = U * S * Vh
        """
        if matrix.ndim != 2:
            return matrix # Apenas 2D suportado no momento
            
        U, S, Vh = np.linalg.svd(matrix, full_matrices=False)
        
        # Determinar número de componentes para manter
        k = max(1, int(len(S) * ratio))
        
        # Reconstruir matriz aproximada de baixo rank
        compressed_S = S[:k]
        compressed_U = U[:, :k]
        compressed_Vh = Vh[:k, :]
        
        # Retornar componentes decompostas para economia real de armazenamento
        # Em vez de reconstruir, armazenamos (U_k, S_k, Vh_k)
        return {
            "U": compressed_U,
            "S": compressed_S,
            "Vh": compressed_Vh,
            "original_shape": matrix.shape
        }

    @staticmethod
    def decompress_matrix(comp_dict):
        """Reconstrói a matriz a partir das componentes comprimidas."""
        return (comp_dict["U"] * comp_dict["S"]) @ comp_dict["Vh"]

    def compress_model(self, weights_dict, ratio=0.4):
        """Aplica compressão em todo o dicionário de pesos."""
        compressed_model = {}
        original_size = 0
        compressed_size = 0
        
        for key, weight in weights_dict.items():
            original_size += weight.nbytes
            if weight.ndim == 2 and weight.shape[0] > 10 and weight.shape[1] > 10:
                comp = self.compress_matrix(weight, ratio=ratio)
                compressed_model[key] = comp
                compressed_size += comp["U"].nbytes + comp["S"].nbytes + comp["Vh"].nbytes
            else:
                compressed_model[key] = weight
                compressed_size += weight.nbytes
                
        reduction = (1 - compressed_size / original_size) * 100
        print(f"📉 Compressão V8: Redução de {reduction:.2f}% no tamanho do modelo.")
        return compressed_model
