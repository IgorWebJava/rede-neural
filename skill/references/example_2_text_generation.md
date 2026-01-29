# Exemplo 2: Geração de Texto Soberana com Transformer

## Objetivo

Construir um modelo de linguagem autoregressivo (Transformer) do zero, utilizando o Núcleo Neural Soberano, para geração de texto em múltiplos idiomas.

## Prompt de Invocação

```
@neural-multimodal-sovereign crie um modelo de linguagem autoregressivo com as seguintes especificações:
- Arquitetura: Transformer (12 camadas, 768 dimensões)
- Tokenizador: Customizado, suportando múltiplos idiomas
- Treinamento: Autoregressivo
- Memória: Ativar Memória Semântica para contexto de longo prazo
```

## Execução Esperada (Resumo do Processo)

1.  **Fase 1 (Planejamento):** O agente irá gerar a estrutura de diretórios e o `config.yaml` com as modalidades `text` e `memory` ativadas.
2.  **Fase 2 (Núcleo Neural):** O agente garantirá que as camadas `Attention manual`, `LayerNorm` e `Embeddings` estejam implementadas no Núcleo Neural.
3.  **Fase 3 (Multimodal):** O agente implementará o `Transformer próprio` (Encoder/Decoder de Texto) e o `Tokenizador customizado`.
4.  **Fase 4 (Memória):** O agente implementará a `Memória Semântica Vetorial` com indexação própria e similaridade cosine para enriquecer o contexto de geração.
5.  **Fase 5 (Produção):** O agente gerará os scripts de pré-processamento de texto, treino e o script de inferência para geração de texto.

## Saída Esperada

- Arquivo `config.yaml` com `modalities.text.enabled: true` e `memory.semantic.enabled: true`
- Diretório `src/text/` contendo `tokenizer.py` e `transformer.py`
- Implementação do grafo computacional para o Transformer no `autograd.py`
- Arquivo `scripts/generate.py` para inferência de texto
- Documentação técnica sobre o modelo de linguagem e o tokenizador
