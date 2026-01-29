# Exemplo 1: Classificação de Imagens Soberana

## Objetivo

Criar um sistema de classificação de imagens de ponta a ponta, utilizando o Núcleo Neural Soberano e o módulo de Visão, sem depender de frameworks externos.

## Prompt de Invocação

```
@neural-multimodal-sovereign crie uma rede neural para classificação de imagens com as seguintes características:
- Entrada: imagens 224x224 RGB
- Saída: 1000 classes (ImageNet)
- Arquitetura: CNN + Vision Transformer híbrido
- Treinamento: CPU e GPU
- Precisão: float32
```

## Execução Esperada (Resumo do Processo)

1.  **Fase 1 (Planejamento):** O agente irá gerar a estrutura de diretórios e o `config.yaml` com as modalidades `vision` e `code` (para testes/scripts) ativadas.
2.  **Fase 2 (Núcleo Neural):** O agente implementará as classes `Tensor`, `Autograd`, `Linear`, `Conv2D` e `Attention manual` em Python puro, usando `numpy` para as operações de array.
3.  **Fase 3 (Multimodal):** O agente implementará o `CNN + Vision Transformer híbrido` (Encoder Visual) e o `Encoder de Código` (para scripts de treino).
4.  **Fase 4 (Memória):** O agente implementará o sistema de memória para armazenar pesos e logs de treino.
5.  **Fase 5 (Produção):** O agente gerará os scripts de treino (`train.py`), inferência (`infer.py`) e o script de deploy.

## Saída Esperada

- Arquivo `config.yaml` com `modalities.vision.enabled: true`
- Diretório `src/engine/` contendo `tensor.py`, `autograd.py`, `layers.py`
- Diretório `src/models/` contendo a implementação do modelo híbrido
- Arquivo `scripts/train.py` utilizando o `Runtime` do Núcleo Neural
- Documentação técnica detalhada do modelo
