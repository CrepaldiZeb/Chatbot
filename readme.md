# Chatbot

Este projeto é um chatbot que se integra com a API do Ollama para utilizar o modelo **llama3.1:8b**. O chatbot permite tanto iniciar um novo chat quanto retomar um chat existente (armazenado na base de dados SQLite). Além disso, oferece alguns comandos especiais para ajustar o comportamento e a busca de contexto.

---

## Requisitos

- **Python 3.10** (ou superior)
- **Ollama** rodando no backend com o modelo **llama3.1:8b** já realizado o pull.  
  *Para puxar o modelo, execute:*
  ```bash
  ollama pull llama3.1:8b
  ```
- **Base de dados SQLite** para armazenar os chats.

---

## Instalação

### Windows

1. **Criar e ativar um ambiente virtual (venv):**
   - Abra o Prompt de Comando ou PowerShell.
   - Crie o ambiente virtual:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente:
     - No PowerShell:
       ```bash
       .\venv\Scripts\Activate.ps1
       ```
     - No CMD:
       ```bash
       venv\Scripts\activate.bat
       ```

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Rodar o aplicativo:**
   ```bash
   python main.py
   ```

---

### Linux

1. **Criar e ativar um ambiente virtual (venv):**
   - Abra o Terminal.
   - Crie o ambiente virtual:
     ```bash
     python3 -m venv venv
     ```
   - Ative o ambiente virtual:
     ```bash
     source venv/bin/activate
     ```

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Rodar o aplicativo:**
   ```bash
   python main.py
   ```

---

## Uso do Chatbot

Ao iniciar o aplicativo (executando `main.py`), você será apresentado com as seguintes opções:

- **Criar novo chat:**
  - Se escolher essa opção, o programa solicitará que informe um nome para o chat.
- **Continuar chat existente:**
  - Permite retomar um chat já salvo na base de dados.

Dentro do chat, você pode utilizar os seguintes comandos especiais:

- `/behave`: Altera o comportamento do bot.
- `/search`: Faz com que o bot realize uma busca na web para obter contexto adicional à sua pergunta.
- `/bye`: Finaliza o chat.

Qualquer entrada que não seja um desses comandos será tratada como uma mensagem comum, e o bot responderá de acordo com o seu treinamento.

---

## Observações Adicionais

### Limitações do Modelo

O modelo **llama3.1:8b** é relativamente pequeno e pode, ocasionalmente, apresentar limitações. Em testes, foi observado que o comando `/behave` pode não funcionar como esperado em todos os cenários – especialmente para mudanças de idioma. Entretanto, quando solicitado para alterar o tom das respostas, o modelo respondeu de forma satisfatória.



