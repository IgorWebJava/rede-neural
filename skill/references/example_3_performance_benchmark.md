# Exemplo 3: Benchmark de Performance Otimizada

## Objetivo

Demonstrar o ganho de performance obtido pela aplicação da **Fase 6: Otimização de Performance Industrial** (Integração Numba JIT) em uma operação crítica do Núcleo Neural.

## Prompt de Invocação

```
@neural-multimodal-sovereign execute a Fase 6 de Otimização no Núcleo Neural, focando na multiplicação de matrizes (np.dot) e gere um relatório de benchmark comparativo.
```

## Execução Esperada (Resumo do Processo)

1.  **Preparação**: O agente irá garantir que o Numba esteja instalado e que o template `templates/numba_optimized_kernel.py` seja usado como referência.
2.  **Implementação**: O agente criará um script de teste (`benchmark.py`) que define duas funções idênticas para multiplicação de matrizes: uma pura (`numpy.dot`) e outra otimizada (`@numba.jit(nopython=True)`).
3.  **Benchmark**: O agente executará o teste de tempo de execução para ambas as funções em um grande volume de dados (ex: matrizes 1000x1000) e calculará o fator de aceleração.
4.  **Relatório**: O agente gerará um relatório de benchmark, apresentando o tempo de execução e o ganho percentual.

## Saída Esperada (Relatório de Benchmark)

| Operação | Implementação | Tempo Médio (s) | Fator de Aceleração |
|:---|:---|:---|:---|
| Multiplicação de Matrizes (1000x1000) | Python Puro (`numpy.dot`) | 0.085 | 1.0x |
| Multiplicação de Matrizes (1000x1000) | Numba JIT (`@jit`) | 0.006 | **~14.1x** |

**Conclusão**: A integração do Numba JIT resultou em um ganho de performance de aproximadamente 14x, validando a abordagem de otimização soberana.

## Checkpoint de Validação

Este exemplo serve como o **Checkpoint de Validação** da Fase 6, onde o agente deve apresentar um relatório real com métricas de performance.
