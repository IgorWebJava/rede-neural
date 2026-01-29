from engine.tensor import Tensor

class Autograd:
    """
    Controlador do Grafo Computacional Soberano (RULE 06).
    """
    @staticmethod
    def zero_grad(parameters):
        """Limpa os gradientes acumulados (RULE 05)."""
        for p in parameters:
            if p.grad is not None:
                p.grad.fill(0)

    @staticmethod
    def step(parameters, lr=0.01):
        """Atualização de pesos via SGD manual (RULE 09)."""
        for p in parameters:
            if p.requires_grad and p.grad is not None:
                p.data -= lr * p.grad
