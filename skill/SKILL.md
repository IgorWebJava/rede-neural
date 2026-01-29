---
name: neural-multimodal-sovereign
description: "Projeta, constrói e opera uma rede neural multimodal soberana com interface desktop e persistência robusta em Banco de Dados Local."
---

# 🧠 Neural Multimodal Sovereign 2026 - V12 (DATABASE EDITION)

Este guia capacita o agente a integrar uma camada de persistência industrial utilizando um motor de Banco de Dados Local (SQLite3) ao ecossistema soberano. A V12 substitui arquivos JSON/NPZ por um CRUD completo, garantindo integridade de dados, portabilidade e soberania absoluta.

## ⚖️ Autoridade Máxima: RULES.md

**ATENÇÃO**: Este projeto é regido pelas **14 RULES do Manus**. As RULES definem leis técnicas inegociáveis. Se houver conflito entre este guia e as RULES, as **RULES prevalecem**.

## 📋 Quick Reference (V12 Database)

| Aspecto | Detalhe |
| :--- | :--- |
| **Objetivo** | CRUD completo com DB Local para Pesos, Logs, Reputação e Chat. |
| **Persistência** | Migração de Flat-Files para Banco de Dados Relacional Local. |
| **Segurança** | Sanitização de queries e integridade referencial soberana. |
| **Soberania** | Independência total de servidores de rede externos ou drivers complexos. |

## ⚙️ The Process: V12 Database Integration

### 1️⃣ Modelagem de Dados Soberana
Definir o esquema do banco de dados focado em:
- **`models`**: Armazenamento de pesos e versões de arquitetura.
- **`swarm_reputation`**: Créditos e scores de agentes do enxame.
- **`ethics_ledger`**: Logs imutáveis de decisões e vetos com Hash-Chaining.
- **`chat_history`**: Mensagens multimodais e metadados de XAI.

### 2️⃣ Implementação do CRUD Core
Desenvolver o `SovereignDB`, uma camada de abstração que:
- Utiliza o motor SQLite3 nativo do Python para garantir portabilidade (RULE 09).
- Implementa operações de Create, Read, Update e Delete com validação de integridade.
- Garante que a lógica neural permaneça isolada da complexidade do SQL.

### 3️⃣ Sincronização e Auditoria
Utilizar o Banco de Dados como ponto central de verdade, permitindo auditorias rápidas e recuperação de estado (Genesis Snapshot) de forma atômica e segura.

## 🛑 Exit Criteria

- Banco de Dados Local modelado e operacional.
- Todo o estado do sistema (Pesos, Logs, Chat) migrado para o CRUD.
- Interface Desktop V11 consumindo dados diretamente do DB.
- Auditoria das **14 RULES** concluída via `sovereign_auditor.py`.

---
**Status**: Database-Integrated | **Versão**: 12.0.0-DATABASE
