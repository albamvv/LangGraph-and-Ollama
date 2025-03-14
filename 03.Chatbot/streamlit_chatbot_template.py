import streamlit as st
import ollama
# streamlit run 07.Streamlit/streamlit_chatbot_template.py 

# Configuración de la página
st.set_page_config(
    page_title="Mi Template en Streamlit", 
    layout="wide")

# Título de la aplicación
st.title("🚀 Alba's Chatbot")

st.subheader("Bienvenido a la aplicación")
#st.write("Esta es una plantilla básica de Streamlit.")
#st.image("https://source.unsplash.com/random/800x400", caption="Imagen aleatoria")

# Función para obtener respuesta de Ollama con streaming
def stream_ollama_response(messages):
    response_stream = ollama.chat(model="llama3.2:3b", messages=messages, stream=True)
    for chunk in response_stream:
        yield chunk["message"]["content"]

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar historial de mensajes
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Input field for user messages
prompt = st.chat_input("Enter your question")
if prompt:
    # Agregar mensaje del usuario al historial
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt) # Display user message

   # Crear espacio para la respuesta en streaming
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        # Generar respuesta en streaming
        for chunk in stream_ollama_response(st.session_state["messages"]):
            full_response += chunk
            response_container.markdown(full_response)  # Actualiza el mensaje en pantalla
 

    # Store assistant response in session history
    st.session_state["messages"].append({'role': 'assistant', 'content': full_response})  

   
