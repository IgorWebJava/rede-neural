# Autonomia de Enxame e Governança Descentralizada (V7)

Este documento detalha os mecanismos de auto-governança e orquestração autônoma da Versão 7.

## 1. Consenso Bizantino Soberano
Para garantir a integridade do modelo global em um ambiente descentralizado, a V7 utiliza um protocolo de **Consenso Bizantino**:
- **Robustez a Outliers**: Utiliza a média aparada (*Trimmed Mean*) para ignorar contribuições de nós que divergem drasticamente do consenso, protegendo contra envenenamento de modelo.
- **Validação Cruzada**: Cada contribuição é auditada contra o estado global antes de ser integrada.

## 2. Economia de Sabedoria e Reputação
O enxame opera sob uma meritocracia neural gerenciada pelo `AgentReputationSystem`:
- **Score de Reputação**: Baseado na qualidade histórica das contribuições (estabilidade e perda).
- **Créditos de Utilidade**: Agentes acumulam créditos ao processar amostras reais, que aumentam seu **Poder de Voto** no consenso.
- **Votação Ponderada**: O peso de cada agente na fusão final é proporcional à sua reputação e créditos acumulados.

## 3. Orquestração e Auto-Replicação
O `SwarmOrchestrator` permite que o sistema se expanda organicamente:
- **Spawn de Nós**: Capacidade de criar novos nós de treinamento independentes com isolamento de contexto total (RULE 03).
- **Auto-Cura do Enxame**: Nós inativos ou corrompidos podem ser detectados e reinicializados pelo orquestrador.

## 4. Dashboard de Controle (Swarm-Control)
A governança é transparente e auditável via `scripts/swarm_control.py`, permitindo visualizar em tempo real a hierarquia de reputação e a saúde coletiva do enxame.
