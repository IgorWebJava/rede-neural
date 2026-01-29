# Estrutura Oficial do Projeto (RULES-Compliant)
Neural Multimodal Sovereign 2026

## Objetivo

Este documento define a **estrutura obrigatória de pastas e arquivos**, integrada às **14 RULES do Manus**.

## ⚖️ Conformidade com as RULES

| Pasta | RULE Relacionada | Descrição |
| :--- | :--- | :--- |
| `/core` | RULE 06 | Fundamentos e tipos base. |
| `/engine` | RULE 09 | Motor neural soberano (Python/Numpy). |
| `/autograd` | RULE 09 | Diferenciação automática manual. |
| `/security` | RULE 01, 13 | Sandbox e isolamento de segredos. |
| `/persistence` | RULE 04, 05 | Gerenciamento de pesos e estados. |
| `/docs` | RULE 14 | Documentação técnica arquitetural. |
| `/rules` | Global | Cópia local das RULES para auditoria offline. |

## Estrutura Raiz Obrigatória

```text
neural-multimodal-sovereign/
│
├── rules/             <-- RULE: Leis inegociáveis
├── core/              <-- RULE 06: Arquitetura Limpa
├── engine/            <-- RULE 09: Soberania (No PyTorch/TF)
├── autograd/          <-- RULE 09: Autograd Manual
├── layers/            <-- RULE 06: Modularidade
├── modalities/        <-- RULE 06: Especialização
├── fusion/            <-- RULE 06: Fusão Explícita
├── memory/            <-- RULE 03: Isolamento de Memória
├── autonomy/          <-- RULE 02, 12: Autonomia Controlada
├── training/          <-- RULE 02, 10: Treino Não-Bloqueante
├── inference/         <-- RULE 02: Performance
├── evaluation/        <-- RULE 10: Validação
├── security/          <-- RULE 01, 13: Hardening e Sandbox
├── persistence/       <-- RULE 04, 05: Cofre de Pesos
├── configs/           <-- RULE 01: Separação Código/Config
├── logs/              <-- RULE 01, 08: Auditoria e Erros
├── checkpoints/       <-- RULE 04: Versionamento de Pesos
├── scripts/           <-- Operacional
├── tests/             <-- RULE 10: Testes Conceituais
└── docs/              <-- RULE 14: Documentação como Código
```

## Regras de Implementação
1. **RULE 08**: Cada arquivo `.py` deve ter tratamento de erro explícito.
2. **RULE 14**: Cada diretório principal deve conter um `README.md` ou arquivo `.md` explicativo em `/docs`.
3. **RULE 09**: É proibido importar `torch`, `tensorflow` ou similares em qualquer arquivo desta estrutura.
