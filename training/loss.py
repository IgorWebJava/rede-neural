from engine.tensor import Tensor
import numpy as np

def binary_cross_entropy(prediction, target):
    """
    Função de Perda BCE Soberana (RULE 09).
    L = -[y*log(p) + (1-y)*log(1-p)]
    """
    # prediction deve ter passado por uma Sigmoid (valores entre 0 e 1)
    # RULE 05: Estabilidade numérica via log seguro (já implementado no Tensor.log)
    
    term1 = target * prediction.log()
    term2 = (Tensor(1.0) - target) * (Tensor(1.0) - prediction).log()
    
    loss = (term1 + term2) * -1.0
    # Retorna a média da loss se for um batch
    return loss.sum() * (1.0 / prediction.data.size)
