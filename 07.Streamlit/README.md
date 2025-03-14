# Chat message memory

## Overview



## Usage

```sh
   python chat_message_memory.py
```

## Guide

- Here's an minimal example of how to use st.chat_message to display a welcome message: 

```python
import streamlit as st
with st.chat_message("user"):
    st.write("Hello 👋")
```
**Output:**

 ![Alt text](assets/chat-message-hello.png)


## Implementation

- Mostrar mensaje del usuario en el chat
```python
    with st.chat_message("user"):
        st.write(prompt)
```

-  Agregar mensaje del usuario al historial
```python
    st.session_state["messages"].append({"role": "user", "content": prompt})
```

- Generar respuesta con Ollama
```python
response = ollama.chat(model="llama3.2:3b", messages=st.session_state["messages"]) bot_reply = response["message"]["content"]
```

- Agregar respuesta del bot al historial
```python
st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
```

- Mostrar respuesta en el chat
```python
with st.chat_message("assistant"): st.write(bot_reply)
```

