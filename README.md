
# UploadFilePythonContentOracle

UploadFilePythonContentOracle é uma aplicação desktop desenvolvida em Python com interface gráfica (PySimpleGUI) para facilitar o upload de arquivos e pastas para o Oracle Content Management Cloud, utilizando autenticação via token OAuth2.

---

## Visão Geral

Esta ferramenta foi criada para automatizar e simplificar o processo de envio de múltiplos arquivos ou pastas inteiras para o Oracle Content, com acompanhamento visual do progresso, logs de operação e gerenciamento de token de autenticação.

---

## Funcionalidades

- **Upload de Arquivos**: Permite selecionar múltiplos arquivos locais e enviá-los para o Oracle Content, criando automaticamente a pasta de destino.
- **Upload de Pastas**: Permite selecionar uma pasta local e enviar todos os arquivos contidos nela para o Oracle Content, com criação automática da pasta correspondente.
- **Gestão de Token**: Interface para inserir, salvar, buscar e excluir o token de autenticação necessário para o upload.
- **Barra de Progresso**: Acompanhamento visual do progresso de upload.
- **Logs**: Registro de erros e operações em arquivo de log (`app.log`).
- **Interface Gráfica Intuitiva**: Navegação por abas para separar uploads de arquivos, uploads de pastas e configurações.

---

## Pré-requisitos

- Python 3.7+
- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)
- [requests](https://docs.python-requests.org/en/latest/)

Instale as dependências com:

```bash
pip install PySimpleGUI requests
```

---

## Instalação e Execução

1. Clone este repositório:
  ```bash
  git clone https://github.com/luccassantos4/UploadFilePythonContentOracle.git
  ```
2. Acesse a pasta do projeto:
  ```bash
  cd UploadFilePythonContentOracle
  ```
3. Execute a aplicação:
  ```bash
  python main.pyw
  ```
  Ou gere um executável com PyInstaller:
  ```bash
  pyinstaller main.pyw --icon=upload-file.ico --onefile
  ```

---

## Como Usar

1. **Configuração do Token**:
  - Acesse a aba "Config".
  - Insira seu token OAuth2 e clique em "Salvar Token".
  - Se necessário, utilize "Buscar Token" para abrir a página de obtenção do token.
  - Para remover o token, clique em "Excluir Token".

2. **Upload de Arquivos**:
  - Acesse a aba "Upload Arquivos".
  - Clique em "Escolher arquivos" e selecione os arquivos desejados.
  - Clique em "Enviar Arquivos" para iniciar o upload.

3. **Upload de Pastas**:
  - Acesse a aba "Upload Pasta".
  - Clique em "Escolher Pasta" e selecione a pasta desejada.
  - Clique em "Enviar Pasta" para iniciar o upload de todos os arquivos da pasta.

Durante o upload, acompanhe o progresso pela barra e consulte o log para detalhes ou erros.

---

## Estrutura do Projeto

```
├── conexao.py         # Configuração das conexões e endpoints do Oracle Content
├── controller.py      # Funções de upload, criação de pastas e lógica principal
├── main.pyw           # Interface gráfica e controle de eventos
├── upload-file.ico    # Ícone do aplicativo
├── README.md          # Documentação
├── LICENSE            # Licença
```

---

## Detalhes Técnicos

- **Integração com Oracle Content**: Utiliza endpoints REST para upload de arquivos e criação de pastas.
- **Autenticação**: Necessário fornecer um token OAuth2 válido para autenticação nas requisições.
- **Threads**: O upload é realizado em threads para não travar a interface gráfica.
- **Logs**: Todos os erros e operações relevantes são registrados em `app.log`.

---

## Screenshots

<div align="center">
  <h4>Página 1 Preview</h4>
  <img src="https://user-images.githubusercontent.com/62127980/191640895-78d36bef-8d10-49b5-a777-b62bebabf7d4.jpg">
</div>
<div align="center">
  <h4>Página 2 Preview</h4>
  <img src="https://user-images.githubusercontent.com/62127980/191640893-4a31f3fd-a01d-4c22-94dc-25fce5aef35d.jpg">
</div>
<div align="center">
  <h4>Página 3 Preview</h4>
  <img src="https://user-images.githubusercontent.com/62127980/191640892-00a43ad9-a3ee-4e98-887b-c916441550ae.jpg">
</div>
