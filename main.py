import os
import sqlite3
from datetime import datetime

os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"

from langchain_ollama import OllamaLLM
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_community.document_loaders import WebBaseLoader
import googlesearch

# Configuração do banco de dados
def setup_database():
    os.makedirs('db', exist_ok=True)  # Garante que a pasta exista
    conn = sqlite3.connect(os.path.join('db', 'chats.db'))
    c = conn.cursor()
    
    # Tabela para os chats (removido o campo created_at)
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT)''')
    
    # Tabela para as mensagens (removido o campo created_at)
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  chat_id INTEGER,
                  type TEXT,
                  content TEXT,
                  FOREIGN KEY (chat_id) REFERENCES chats (id))''')
    
    conn.commit()
    return conn

def save_message(conn, chat_id, message_type, content):
    c = conn.cursor()
    # Corrigido para ter apenas 3 placeholders
    c.execute('''INSERT INTO messages (chat_id, type, content)
                 VALUES (?, ?, ?)''', (chat_id, message_type, content))
    conn.commit()

def load_chat_history(conn, chat_id):
    c = conn.cursor()
    # Alterado ORDER BY para 'id', já que não há mais 'created_at'
    c.execute('SELECT type, content FROM messages WHERE chat_id = ? ORDER BY id', (chat_id,))
    messages = []
    for msg_type, content in c.fetchall():
        if msg_type == 'system':
            messages.append(SystemMessage(content=content))
        elif msg_type == 'human':
            messages.append(HumanMessage(content=content))
        elif msg_type == 'ai':
            messages.append(AIMessage(content=content))
    return messages

def list_chats(conn):
    c = conn.cursor()
    # Removido o campo created_at da seleção e ordenação
    c.execute('SELECT id, name FROM chats')
    return c.fetchall()

def create_new_chat(conn, name):
    c = conn.cursor()
    # Removido o campo created_at do INSERT
    c.execute('INSERT INTO chats (name) VALUES (?)', (name,))
    conn.commit()
    return c.lastrowid

def web_search_and_scrape(query, num_results=3):
    try:
        # Realizar busca no Google usando googlesearch
        search_results = list(googlesearch.search(query, num_results=num_results))
        print(f"\nSearching: {search_results}\n")
        
        # Carregar conteúdo das páginas
        loader = WebBaseLoader(search_results)
        documents = loader.load()
        
        # Preparar o resumo dos resultados
        summary = "\nInformações encontradas:\n\n"
        for i, doc in enumerate(documents, 1):
            summary += f"Fonte {i} ({doc.metadata['source']}):\n"
            summary += f"{doc.page_content[:1000]}...\n\n"
        
        return summary
    
    except Exception as e:
        return f"Erro durante a busca: {str(e)}"

model = OllamaLLM(model="llama3.1:8b")

def send_message(user_input, conn, chat_id, chat_history):  
    chat_history.append(HumanMessage(content=user_input))
    save_message(conn, chat_id, 'human', user_input)
    
    result = model.invoke(chat_history)
    
    chat_history.append(AIMessage(content=result))
    save_message(conn, chat_id, 'ai', result)
    
    print(f"\nAI: {result}\n")

def main():
    conn = setup_database()
    chat_history = []
    
    print("\n=====x========x========x=================x========x========x======")
    print("=====x========x========x==== CHAT_BOT ===x========x========x======")
    print("=====x========x========x=================x========x========x======")
    
    print("\n1. Criar novo chat")
    print("2. Continuar chat existente")
    choice = input("Escolha uma opção: ")
    
    if choice == '1':
        name = input("Digite um nome para o chat: ")
        chat_id = create_new_chat(conn, name)
        chat_history.clear()
        # Inicializar com a mensagem do sistema
        initial_system_message = "Você é um chatbot. Você obedece as ordens do sistema, ele molda e define seu comportamento."
        chat_history.append(SystemMessage(content=initial_system_message))
        save_message(conn, chat_id, 'system', initial_system_message)
    else:
        print("\nChats existentes:")
        chats = list_chats(conn)
        for chat in chats:
            print(f"ID: {chat[0]}, Nome: {chat[1]}")
        
        chat_id = int(input("\nDigite o ID do chat que deseja continuar: "))
        chat_history.clear()
        chat_history.extend(load_chat_history(conn, chat_id))

    print("\nInstruções: Digite '/bye' para finalizar.")
    print("Instruções: Digite '/behave' para mudar o contexto.")
    print("Instruções: Digite '/search' para fazer uma busca na web.\n")

    sair = False
    while not sair:
        user_input = input("Você: ")
        if user_input == "/bye":
            sair = True
        elif user_input == "/behave":
            context = input("Escolha o comportamento do chatbot: ")
            system_message = "O sistema ordena: " + context
            chat_history.append(SystemMessage(content=system_message))
            save_message(conn, chat_id, 'system', system_message)
            print("Comportamento alterado.")
        elif user_input == "/search":
            search_query = input("O que você quer pesquisar? ")
            print("\nRealizando busca na web...")
            search_results = web_search_and_scrape(search_query)
            
            context_message = f"Com base na pesquisa sobre '{search_query}', aqui estão as informações mais recentes: {search_results}"
            chat_history.append(SystemMessage(content=context_message))
            save_message(conn, chat_id, 'system', context_message)
            send_message(search_query, conn, chat_id, chat_history)  
        else:
            send_message(user_input, conn, chat_id, chat_history)  

    conn.close()

if __name__ == "__main__":
    main()
