import streamlit as st
import ollama
# streamlit run 03.Chatbot/3.streamlit_chatbot_template.py 

# Configuración de la página
st.set_page_config(
    page_title="Mi Template en Streamlit", 
    layout="wide")

# Título de la aplicación
st.title("🚀 Alba's Chatbot")
st.subheader("Bienvenido a la aplicación")

# Lista de modelos disponibles en Ollama
available_models = ["llama3.2:3b", "mistral", "gemma:2b", "codellama", "phi3"]

# Inicializar variables en session_state si no existen
if "messages" not in st.session_state:
    st.session_state["messages"] = []
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
        st.rerun()  # Recargar la app para aplicar cambios

# Botón para borrar historial de chat
if st.session_state["chat_active"]:
    if st.button("🗑️ Borrar Chat"):
        st.session_state["messages"] = []  # Reiniciar historial
        st.session_state["chat_active"] = False  # Desactivar el chat
        st.success("✅ Chat borrado correctamente.")  # Mensaje de confirmación
        st.rerun()  # Refrescar la app para aplicar cambios

# Función para obtener respuesta de Ollama con streaming y manejo de errores
def stream_ollama_response(messages,model):
    try:
        response_stream = ollama.chat(model=model, messages=messages, stream=True)
        for chunk in response_stream:
            yield chunk["message"]["content"]
    except Exception as e:
        st.error(f"❌ Error al generar respuesta: {str(e)}")
        return


# Solo mostrar chat si el usuario ha iniciado la conversación
if st.session_state["chat_active"]:
    # Display previous chat messages from session history
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

        # Obtener el modelo seleccionado
        selected_model = st.session_state["selected_model"]

        # Crear espacio para la respuesta en streaming
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            # Generar respuesta en streaming
            for chunk in stream_ollama_response(st.session_state["messages"],selected_model):
                full_response += chunk
                response_container.markdown(full_response)  # Actualiza el mensaje en pantalla

        # Store assistant response in session history
        st.session_state["messages"].append({'role': 'assistant', 'content': full_response})  

   
