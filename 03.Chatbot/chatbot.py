from imports import *  # Importar módulos necesarios
import sqlite3
# streamlit run 03.Chatbot/chatbot.py 

# Configuración de la página
st.set_page_config(page_title="🚀 Alba's Chatbot", layout="wide")
st.title("🚀 Alba's Chatbot")
st.subheader("Bienvenido a la aplicación")

# Lista de modelos disponibles en Ollama
available_models = ["llama3.2:3b", "mistral", "gemma:2b", "codellama", "phi3"]

# Base de datos para almacenar el historial de chat
db_url = "sqlite:///chat_history.db"
user_id = "Alba Vadillo"

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, db_url)

# Inicializar variables en session_state si no existen
if "chat_active" not in st.session_state:
    st.session_state["chat_active"] = False  # Estado del chat
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = available_models[0]  # Modelo por defecto

# Selector de modelo antes de iniciar el chat
if not st.session_state["chat_active"]:
    st.session_state["selected_model"] = st.selectbox("🧠 Selecciona un modelo:", available_models)

# Botón para iniciar la conversación
if not st.session_state["chat_active"]:
    if st.button("🟢 Iniciar Chat"):
        st.session_state["chat_active"] = True
        st.rerun()

# Botón para borrar historial de chat
def clear_chat():
    history = get_session_history(user_id)
    history.clear()
    st.session_state["chat_active"] = False
    st.success("✅ Chat borrado correctamente.")
    st.rerun()

if st.session_state["chat_active"]:
    if st.button("🗑️ Borrar Chat"):
        clear_chat()

# Configuración del LLM
base_url = "http://localhost:11434"
selected_model = st.session_state["selected_model"]
llm = ChatOllama(base_url=base_url, model=selected_model)
system = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")
human = HumanMessagePromptTemplate.from_template("{input}")
messages = [system, MessagesPlaceholder(variable_name='history'), human]
prompt = ChatPromptTemplate(messages=messages)

# Cadena de procesamiento del chatbot
chain = prompt | llm | StrOutputParser()
runnable_with_history = RunnableWithMessageHistory(
    chain, get_session_history, 
    input_messages_key='input', 
    history_messages_key='history'
)

# Mostrar historial de chat desde la base de datos
history = get_session_history(user_id)
stored_messages = history.messages

for message in stored_messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

# Input de usuario
user_prompt = st.chat_input("Escribe tu mensaje...")

if user_prompt:
    history.add_user_message(user_prompt)  # Guardar mensaje en la base de datos
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        
        for chunk in runnable_with_history.stream({'input': user_prompt}, config={'configurable': {'session_id': user_id}}):
            full_response += chunk
            response_container.markdown(full_response)  # Mostrar en pantalla
    
    history.add_ai_message(full_response)  # Guardar respuesta en la base de datos
