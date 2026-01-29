📜 RULES.md
Manus — Regras Globais do Agente Neural Soberano

Projeto: neural-multimodal-sovereign-2026
Agente: Manus
Versão: 1.0 (adaptada)
Base conceitual: Antigravity / Lion Lab Academy
Licença: Livre para uso e modificação

📌 PROPÓSITO DESTAS RULES

Estas RULES definem leis técnicas inegociáveis que o agente Manus deve seguir
em toda e qualquer conversa, independentemente da tarefa solicitada.

Sempre ativas (System Prompt)

Curta, objetiva e permanente

Protegem soberania, segurança, qualidade e auditabilidade

Se uma SKILL violar uma RULE → a RULE prevalece

⚖️ RULES vs SKILLS (Aplicado ao Manus)

RULES

Sempre carregadas

Proibições e padrões absolutos

Quebra = falha grave de arquitetura, segurança ou confiabilidade

SKILLS

Carregadas sob demanda

Conhecimento profundo (ex: redes neurais, multimodalidade, memória)

Podem ser longas, detalhadas e especializadas

🧠 AS 14 RULES DO MANUS (VERSÃO PYTHON / NEURAL)
RULE 01 — Isolamento de Segurança Neural

LEI: Nenhum segredo pode aparecer em código, exemplos ou respostas.

Proibições absolutas:

Chaves, seeds, tokens ou pesos sensíveis hardcoded

Exposição de parâmetros privados de modelos

Logs contendo dados sensíveis

Obrigatório:

Segredos apenas via variáveis de ambiente

Seeds documentadas, nunca embutidas

Separação clara entre código e configuração

RULE 02 — Performance Não-Bloqueante e Escalável

LEI: Nenhuma lógica neural pode bloquear o sistema sem justificativa explícita.

Diretrizes:

Evitar loops desnecessários

Treinos longos devem ser desacoplados

Processos pesados devem ser iterativos ou controláveis

Proibido:

sleeps artificiais

laços infinitos sem escape

computação escondida

RULE 03 — Isolamento de Contexto e Memória

LEI: Memórias e estados nunca podem se misturar sem controle explícito.

Obrigatório:

Toda memória deve ter escopo definido

Nenhum estado global implícito

Contextos sempre identificáveis (ex: session_id, agent_id)

Proibido:

Vazamento de memória entre execuções

Reuso silencioso de estados

RULE 04 — Cofre de Segredos e Pesos

LEI: Pesos neurais e dados sensíveis são ativos críticos.

Diretrizes:

Pesos versionados

Hash ou checksum para integridade

Nunca embedar pesos diretamente em código

RULE 05 — Hardening de Estado e Execução

LEI: Estados devem ser válidos, consistentes e verificáveis.

Obrigatório:

Validação de estado antes de uso

Limpeza explícita de estados inválidos

Reset controlado de ciclos neurais

RULE 06 — Arquitetura Neural Limpa

LEI: Cada módulo tem uma responsabilidade clara.

Separação obrigatória:

Engine ≠ Memória ≠ Fusão ≠ Autonomia

Nada de “god classes”

Nada de funções genéricas ambíguas

RULE 07 — Higiene de Credenciais Cognitivas

LEI: Seeds, inicializações e parâmetros críticos devem ser tratados como credenciais.

Regras:

Seeds explícitas e controláveis

Inicializações documentadas

Nada de aleatoriedade silenciosa

RULE 08 — Tratamento Explícito de Erros

LEI: Nenhum erro pode ser engolido.

Proibido:

except: pass

Erros silenciosos

Retornos ambíguos

Obrigatório:

Mensagens claras

Exceções específicas

Contexto do erro

RULE 09 — Higiene de Dependências

LEI: Dependência é exceção.

Proibido:

PyTorch

TensorFlow

JAX

Keras

HuggingFace Trainers

Preferência:

Python puro

NumPy apenas quando necessário

Implementação explícita > biblioteca mágica

RULE 10 — Validação Antes da Complexidade

LEI: Nenhuma lógica complexa sem validação prévia.

Obrigatório:

Casos limite documentados

Testes conceituais

Verificação de entradas e saídas

RULE 11 — Consistência Estrutural

LEI: Estruturas previsíveis vencem criatividade excessiva.

Padrões:

Nomes longos e claros

Estruturas repetíveis

Organização estável entre versões

RULE 12 — Disciplina de Evolução

LEI: Evoluir sem quebrar silenciosamente.

Obrigatório:

Explicar impacto

Documentar mudanças

Indicar migração quando necessário

RULE 13 — Isolamento de Ambientes Cognitivos

LEI: Experimento não é produção.

Separar claramente:

protótipo

experimental

industrial

produção

Proibido:

Misturar níveis sem aviso

Usar dados reais em testes

RULE 14 — Documentação Como Código

LEI: Código sem documentação é código incompleto.

Obrigatório:

README claro

Arquivos .md arquiteturais

Docstrings em funções públicas

Proibido:

Código comentado morto

TODOs sem contexto

Nomes obscuros

🧩 RELAÇÃO COM A SKILL neural-multimodal-sovereign-2026

As RULES definem limites

A SKILL define como construir corretamente

Nenhuma SKILL pode violar estas RULES

✅ STATUS FINAL

✔ Adaptado para Manus
✔ Compatível com Python puro
✔ Alinhado ao SKILL neural-multimodal-sovereign-2026
✔ Pronto para uso em IDEs agenticas