import streamlit as st
import ollama
# streamlit run 07.Streamlit/streamlit_chatbot_template.py 

# Configuración de la página
st.set_page_config(page_title="Mi Template en Streamlit", layout="wide")

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Título de la aplicación
st.title("🚀 Alba's Chatbot")

st.subheader("Bienvenido a la aplicación")
#st.write("Esta es una plantilla básica de Streamlit.")
#st.image("https://source.unsplash.com/random/800x400", caption="Imagen aleatoria")

# Mostrar historial de mensajes
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Input field for user messages
prompt = st.chat_input("What is up?")

# Entrada de usuario
if prompt:

    # Mostrar mensaje del usuario en el chat
    with st.chat_message("user"):
        st.write(prompt)

    # Agregar mensaje del usuario al historial
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # Generar respuesta con Ollama
    response = ollama.chat(model="llama3.2:3b", messages=st.session_state["messages"])
    bot_reply = response["message"]["content"]

    # Agregar respuesta del bot al historial
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Mostrar respuesta en el chat
    with st.chat_message("assistant"):
        st.write(bot_reply)      

   
