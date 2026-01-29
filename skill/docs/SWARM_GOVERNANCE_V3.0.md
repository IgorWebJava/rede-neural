# 🌐 Governança de Enxame (Swarm Governance) V3.0

Este documento descreve o sistema de controle descentralizado para a inteligência coletiva do projeto **Neural Multimodal Sovereign**.

## 1. O Problema da Descentralização

Em sistemas de inteligência coletiva (Swarm), o risco de "Envenenamento de Política" (Policy Poisoning) é real. Um agente malicioso ou com falhas técnicas (patologias neurais) pode degradar o modelo global durante a fusão.

## 2. A Solução: Trust-Weighted Consensus

A Governança de Enxame V3.0 implementa uma camada de auditoria matemática entre a exportação de sabedoria e a fusão global.

### 2.1. Métricas de Confiança (Trust Metrics)

O score de cada agente é calculado dinamicamente com base em:

1.  **Estabilidade (40%)**: Frequência e sucesso de intervenções homeostáticas (RULE 05).
2.  **Performance (40%)**: Resultados em benchmarks de validação compartilhados (RULE 10).
3.  **Maturidade (20%)**: Tempo de operação contínua sem falhas críticas.

### 2.2. Isolamento Autônomo (RULE 05 & 13)

Agentes que caem abaixo de um **Threshold de Confiança** são automaticamente isolados. Seus pesos são zerados no kernel de fusão, garantindo que o "ruído" ou a "patologia" de um indivíduo não contamine o coletivo.

## 3. Fluxo de Fusão Soberana

1.  **Auditoria**: O `SwarmGovernance` lê os logs de performance e estabilidade dos pares.
2.  **Ponderação**: O kernel `calculate_trust_scores` gera os pesos de influência.
3.  **Fusão**: O kernel `sovereign_policy_fusion` realiza a média ponderada das Q-Tables.
4.  **Distribuição**: O novo modelo global (mais robusto) é distribuído para o enxame.

---
**Arquivo de Referência**: `templates/swarm_governance_kernel.py`
