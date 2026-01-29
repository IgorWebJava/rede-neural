# 📜 Integração de RULES — Neural Multimodal Sovereign 2026

Este diretório contém a SKILL **Neural Multimodal Sovereign** devidamente adaptada para seguir as **14 RULES do Manus**.

## 🚀 Mudanças Realizadas

1.  **Autoridade Centralizada**: O arquivo `rules/RULES.md` foi integrado como a lei suprema do projeto.
2.  **Auditoria Automatizada**: O script `scripts/sovereign_auditor.py` foi totalmente refatorado para validar não apenas a soberania (No-PyTorch/TF), mas todas as 14 leis técnicas (Segurança, Performance, Erros, etc.).
3.  **Refatoração de Templates**:
    *   `templates/data_pipeline_template.py`: Removidos `time.sleep()` artificiais e adicionado tratamento de erro explícito conforme **RULE 02** e **RULE 08**.
    *   `templates/project_structure.md`: Atualizado para incluir o diretório `/rules` e mapear cada módulo para sua respectiva RULE.
4.  **Documentação**: `SKILL.md` agora referencia as RULES como autoridade máxima.

## 🛠️ Como Validar um Projeto

Para verificar se um projeto segue a SKILL e as RULES, execute:

```bash
python3 scripts/sovereign_auditor.py /caminho/do/seu/projeto
```

O auditor verificará:
- Ausência de frameworks proibidos (**RULE 09**).
- Tratamento de erros adequado (**RULE 08**).
- Ausência de bloqueios de performance (**RULE 02**).
- Estrutura de diretórios obrigatória (**RULE 06 & 11**).
- Isolamento de segredos (**RULE 01**).

---
**Status**: Fully Compliant | **Versão**: 2.8.0-SWARM-RULES
