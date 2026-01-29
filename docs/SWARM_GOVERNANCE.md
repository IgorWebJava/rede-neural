# Governança de Enxame Soberano (V5)

Este documento descreve o protocolo de colaboração e inteligência coletiva implementado na Versão 5.

## 1. Protocolo de Sabedoria (Wisdom Protocol)
A colaboração entre agentes ocorre via pacotes de sabedoria assinados digitalmente:
- **Autenticidade**: Cada pacote é assinado via HMAC-SHA256 com uma chave de enxame (RULE 01).
- **Integridade**: Checksums SHA256 garantem que os pesos não foram corrompidos durante o trânsito (RULE 04).
- **Proveniência**: Metadados de timestamp e agent_id rastreiam a origem de cada contribuição.

## 2. Consenso Federado Soberano
O enxame atinge um modelo global através de um mecanismo de fusão ponderada:
- **Trust-Based Merging**: Agentes com melhor desempenho histórico (menor perda) têm maior peso no consenso.
- **Soberania Matemática**: A fusão é realizada em Python puro, sem dependência de servidores centrais proprietários (RULE 09).

## 3. Auto-Evolução (Self-Architect)
O sistema audita sua própria estrutura:
- **Auditoria Estrutural**: O `SelfArchitect` analisa tendências de perda e sugere expansões de camadas ou congelamento de backbones.
- **Ciclo de Feedback**: Permite que o modelo evolua de forma autônoma mantendo a estabilidade (RULE 12).

## 4. Segurança e Isolamento
Mesmo em um enxame, a **RULE 03** (Isolamento de Contexto) é preservada. Apenas pesos e insights abstratos são compartilhados, nunca dados brutos de treinamento ou segredos locais.
