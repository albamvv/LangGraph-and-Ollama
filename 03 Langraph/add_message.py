from typing import Annotated, TypedDict
from datetime import datetime

# Dummy function to process messages
def add_messages(messages_list, new_messages):
    #print("messages_list-> ",messages_list) # Output: ['Hello', 'How can I help you?'
    return messages_list + new_messages

class State(TypedDict): # TypedDict nos permite definir un diccionario con una estructura fija, donde cada clave tiene un tipo específico.
    messages: Annotated[list, add_messages]  # Extra metadata for processing 
    # State es un diccionario que debe contener una clave llamada messages, que almacena una lista.
    user_name: str  # Nombre del usuario
    chatbot_name: str  # Nombre del chatbot
    conversation_id: int  # ID único de la conversación
    timestamp: str  # Última actualización del estado

# Initial state
state1: State = {"messages": ["Hello", "How can I help you?"]}
#print("state messages-> ", state["messages"]) # ouput-> state messages->  ['Hello', 'How can I help you?']

state2: State = {
    "messages": ["Hola", "¿Cómo puedo ayudarte?"],
    "user_name": "Carlos",
    "chatbot_name": "ChatGPT",
    "conversation_id": 12345,
    "timestamp": datetime.now().isoformat()  # Formato de fecha ISO 8601
}


new_messages = ["Quiero saber el clima", "¿Puedes ayudarme?"]

processed_messages = add_messages(state1["messages"],new_messages)
print('processed_messages: ',processed_messages)
# Output: ["Hello", "How can I help you?", "New message processed!"]


state2["messages"] = add_messages(state2["messages"], new_messages)
state2["timestamp"] = datetime.now().isoformat()  # Actualizamos la fecha
print("Messages-> ",state2["messages"])
print("User-> ",state2["user_name"])
#print(state2)
