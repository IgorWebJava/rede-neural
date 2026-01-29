# 📖 Exemplo: Como usar esta SKILL (Guia para o Agente)

Este exemplo demonstra como um usuário deve invocar a skill e como o agente Manus deve utilizar a pasta `references/` para obter conhecimentos especializados sem sobrecarregar o contexto inicial.

## 💬 Prompt do Usuário

> "@neural-multimodal-sovereign, preciso implementar o **Sistema de Memória Semântica** para o meu projeto de IA soberana. 
> 
> Por favor:
> 1. Consulte as diretrizes detalhadas em `references/memory_system.md`.
> 2. Utilize o template `templates/project_structure.md` para garantir que os diretórios de persistência estejam corretos.
> 3. Implemente a lógica de indexação vetorial em Python puro, seguindo os princípios de soberania."

## 🤖 Comportamento Esperado do Manus

Ao receber este prompt, o agente Manus seguirá este fluxo lógico:

1.  **Ativação**: O Manus lê o `SKILL.md` (que é pequeno e eficiente) para entender o processo geral.
2.  **Busca de Conhecimento**: Em vez de tentar "adivinhar" a arquitetura, ele acessa especificamente `references/memory_system.md` para entender como a memória hierárquica (Curto Prazo vs. Semântica) deve ser implementada.
3.  **Uso de Templates**: Ele lê `templates/project_structure.md` para criar a pasta `data/vectors/` e outros diretórios necessários.
4.  **Execução**: Ele escreve o código Python garantindo que não está usando bibliotecas proibidas (como FAISS ou PyTorch), conforme as restrições lidas no `SKILL.md`.

## 💡 Por que isso é uma Referência?

*   **Eficiência de Tokens**: O agente só carrega o arquivo de "Memória" quando precisa dele.
*   **Precisão**: O uso de referências externas evita que o agente use padrões genéricos de IA e siga exatamente a arquitetura "Sovereign".
*   **Modularidade**: Se a arquitetura de memória mudar, apenas o arquivo em `references/` precisa ser atualizado, sem alterar a lógica principal da SKILL.
