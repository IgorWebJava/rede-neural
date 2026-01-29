# Otimização Quântica e Consciência de Recurso (V8)

Este documento detalha as inovações em eficiência e otimização avançada introduzidas na Versão 8.

## 1. Otimizador QPSO (Quantum-inspired)
Diferente dos otimizadores baseados em gradiente (como Adam/SGD), o **QPSO** utiliza princípios de mecânica quântica para exploração do espaço de parâmetros:
- **Tunelamento Quântico**: Permite que as partículas "atravessem" barreiras de potencial, escapando de mínimos locais onde gradientes tradicionais falhariam.
- **Convergência Global**: Focado em encontrar o ótimo global através de uma nuvem de partículas regida por funções de onda delta.

## 2. Gestão Energética (Power-Aware)
O `SovereignResourceManager` garante que o enxame opere dentro dos limites físicos do hardware:
- **Thermal Throttling**: Ajusta dinamicamente a intensidade do treinamento baseado na temperatura da CPU.
- **Resource Balancing**: Redimensiona o tamanho dos batches e a frequência de sincronização para evitar estouro de memória (RULE 05).

## 3. Compressão Soberana (SVD Pruning)
Para otimizar a comunicação no enxame e o armazenamento em dispositivos de borda:
- **Decomposição de Baixo Rank**: Utiliza SVD para decompor matrizes de pesos grandes em componentes menores, mantendo apenas os valores singulares mais significativos.
- **Redução de Payload**: Capaz de reduzir o tamanho do modelo em até 80% mantendo a precisão funcional.

## 4. Kernels de Alta Performance
Novos kernels em `engine/kernels_v8.py` implementam operações de álgebra linear de baixo nível paralelizadas via Numba, otimizando o uso de instruções SIMD da CPU de forma soberana (RULE 09).
