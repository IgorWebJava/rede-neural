import numpy as np
from engine.tensor import Tensor
from layers.base import Module

class CrossAttention(Module):
    """
    Mecanismo de Atenção Cruzada Soberana (RULE 09).
    Permite que uma modalidade (Query) atenda a outra (Key/Value).
    """
    def __init__(self, query_dim, key_dim, head_dim):
        self.head_dim = head_dim
        self.scale = np.sqrt(head_dim)
        
        # Projeções Lineares
        limit_q = np.sqrt(6 / (query_dim + head_dim))
        limit_k = np.sqrt(6 / (key_dim + head_dim))
        
        self.w_q = Tensor(np.random.uniform(-limit_q, limit_q, (query_dim, head_dim)), requires_grad=True)
        self.w_k = Tensor(np.random.uniform(-limit_k, limit_k, (key_dim, head_dim)), requires_grad=True)
        self.w_v = Tensor(np.random.uniform(-limit_k, limit_k, (key_dim, head_dim)), requires_grad=True)

    def forward(self, query, key_value):
        # 1. Projeções
        q = query.matmul(self.w_q)      # (N_q, head_dim)
        k = key_value.matmul(self.w_k)  # (N_kv, head_dim)
        v = key_value.matmul(self.w_v)  # (N_kv, head_dim)
        
        # 2. Cálculo de Scores: (Q @ K.T) / scale
        scores_data = np.dot(q.data, k.data.T) / self.scale
        
        # 3. Softmax Manual (Soberano)
        max_scores = np.max(scores_data, axis=-1, keepdims=True)
        exp_scores = np.exp(scores_data - max_scores)
        attn_weights_data = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        
        # Criar Tensor para Pesos de Atenção (para Autograd)
        attn_weights = Tensor(attn_weights_data, _children=(q, k), _op='Softmax', requires_grad=True)
        
        # 4. Saída: Weights @ V
        out_data = np.dot(attn_weights_data, v.data)
        out = Tensor(out_data, _children=(attn_weights, v), _op='AttentionOutput', requires_grad=True)
        
        # Definição manual do backward para a atenção (simplificado para o grafo)
        def _backward_attn():
            if attn_weights.requires_grad:
                # Gradiente em relação aos pesos
                attn_weights.grad += np.dot(out.grad, v.data.T)
            if v.requires_grad:
                # Gradiente em relação aos valores
                v.grad += np.dot(attn_weights_data.T, out.grad)
        
        out._backward = _backward_attn
        return out

    def parameters(self):
        return [self.w_q, self.w_k, self.w_v]
