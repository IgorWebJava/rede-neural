# Plataforma Desktop Soberana (V11)

Este documento descreve a nova interface unificada e o Chat AI Híbrido introduzidos na Versão 11.

## 1. Chat AI Híbrido Nativo
O Chat AI Híbrido (`chat/hybrid_ai.py`) é o coração da interação com o usuário:
- **Hibridismo de Modalidade**: Processa simultaneamente texto, visão e áudio em um único fluxo de conversa.
- **Explicabilidade Integrada**: Cada resposta é acompanhada por um relatório de raciocínio gerado pelo `SovereignExplainer`.
- **Soberania de Dados**: Toda a conversação e inferência ocorrem localmente no motor `EdgeInferenceEngine`.

## 2. Interface Desktop Moderna
Desenvolvida em Python nativo utilizando a biblioteca **CustomTkinter**:
- **Sidebar de Navegação**: Acesso rápido entre Chat, Treinamento e Governança.
- **Tema Dark Industrial**: UX otimizada para longas sessões de desenvolvimento e monitoramento.
- **Responsividade**: Layout adaptável para diferentes resoluções de tela.

## 3. Centro de Treinamento Visual
A página de treinamento (`ui/training_view.py`) oferece controle total sobre a evolução da rede:
- **Monitor de Recursos**: Visualização em tempo real de CPU, Memória e Temperatura via `SovereignResourceManager`.
- **Métricas Neurais**: Gráficos e labels dinâmicos de Perda (Loss) e Acurácia.
- **Controle Nativo**: Inicie, pause e monitore o treinamento diretamente pela interface gráfica.

## 4. Execução
Para iniciar a plataforma completa:
```bash
python3 ui/main_window.py
```
*Nota: Requer as dependências `customtkinter` e `pillow` instaladas.*
