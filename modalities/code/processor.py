from layers.base import Module, Linear, ReLU
from engine.tensor import Tensor
import numpy as np

class CodeProcessor(Module):
    """
    Processador de Código e Lógica Soberano (RULE 06 & 09).
    V4: Especializado em extrair padrões estruturais e frequência de keywords.
    """
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        # 1. Embeddings de Código (Tokens)
        self.embedding = Tensor(np.random.randn(vocab_size, embedding_dim) * 0.01, requires_grad=True)
        
        # 2. Keywords de Controle (Análise Estrutural)
        self.keywords = ["def", "class", "import", "from", "return", "if", "for", "while", "try", "except"]
        self.fc_structural = Linear(len(self.keywords) + 1, hidden_dim) # +1 para comprimento
        
        self.fc_logic = Linear(embedding_dim + hidden_dim, hidden_dim)
        self.relu = ReLU()
        self.output_layer = Linear(hidden_dim, embedding_dim)

    def forward(self, token_indices, code_string=""):
        """
        Processamento Híbrido: Tokens + Análise Estrutural.
        """
        # 1. Embedding de Tokens
        embedded = Tensor(self.embedding.data[token_indices], _children=(self.embedding,), _op='CodeEmbedding', requires_grad=True)
        sequence_mean = Tensor(embedded.data.mean(axis=0, keepdims=True), requires_grad=True)
        
        # 2. Análise Estrutural (V4)
        if not code_string and token_indices:
            code_string = " ".join([str(t) for t in token_indices])
            
        features = []
        for kw in self.keywords:
            features.append(code_string.count(kw))
        features.append(len(code_string) / 1000.0)
        
        struct_x = Tensor([features], requires_grad=True)
        struct_feat = self.relu(self.fc_structural(struct_x))
        
        # 3. Fusão Híbrida (Tokens + Estrutura)
        combined = Tensor(np.concatenate([sequence_mean.data, struct_feat.data], axis=-1), requires_grad=True)
        
        logic_state = self.relu(self.fc_logic(combined))
        return self.output_layer(logic_state)

    def parameters(self):
        return ([self.embedding] + 
                self.fc_structural.parameters() + 
                self.fc_logic.parameters() + 
                self.output_layer.parameters())

class LogicValidator:
    """
    Utilitário para validar consistência lógica de saídas de código.
    """
    @staticmethod
    def verify_syntax(code_string):
        """Verifica sintaxe Python básica sem executar (RULE 01)."""
        try:
            compile(code_string, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
