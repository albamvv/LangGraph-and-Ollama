from imports import*
#-------------------- Configuration -------------------
base_url = "http://localhost:11434"
model = 'llama3.2:3b' # Specify the model to be used (Llama 3.2 with 3 billion parameters)
llm = ChatOllama(base_url=base_url, model=model) # Initialize the ChatOllama model with the base URL and model


#-------------------- Simple chain -------------------
template = ChatPromptTemplate.from_template("{prompt}") # Create a chat prompt template that accepts a variable input as "prompt"
chain = template | llm | StrOutputParser() # Create a processing chain: the template is passed to the LLM, and the response is parsed into a string using StrOutputParser

about = "My name is Alba Vadillo. I work for KGP Talkie."
response1=chain.invoke({'prompt': about})
#print("response1-> ",response1)
#------------------------
prompt = "What is my name?"
response2=chain.invoke({'prompt': prompt})
#print("response2-> ",response2)

#------------------ Runnable With Message History ---------------
# Function to retrieve the chat history for a given session ID
def get_session_history(session_id):
    # Uses SQLChatMessageHistory to store and retrieve chat history from an SQLite database
    return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

runnable_with_history = RunnableWithMessageHistory(chain, get_session_history) # Wrap the main chain with message history functionality
user_id = 'Alba Vadillo' # Define a unique user ID (session ID) for maintaining conversation history
history = get_session_history(user_id) # Retrieve the chat history for the specified user session
history.get_messages() # Fetch and display previous messages from the chat history
history.clear() # Clear the chat history (removes all stored messages for this session)

# Invoke the chain with the user input while maintaining session history
runnable1=runnable_with_history.invoke(
    [HumanMessage(content=about)], 
    config={'configurable': {'session_id': user_id}}
)
print("runnable1-> ",runnable1)

# Invoke the chain again with a follow-up question, expecting the model to remember context
runnable2=runnable_with_history.invoke(
    [HumanMessage(content="whats my name?")], 
    config={'configurable': {'session_id': user_id}}
)
print("runnable2-> ",runnable2)

#------------------ Message History with Dictionary Like Inputs ---------------

system = SystemMessagePromptTemplate.from_template("You are helpful assistant.")
human = HumanMessagePromptTemplate.from_template("{input}")

messages = [system, MessagesPlaceholder(variable_name='history'), human]
prompt = ChatPromptTemplate(messages=messages)
chain = prompt | llm | StrOutputParser()

runnable_with_history = RunnableWithMessageHistory(chain, get_session_history, 
                                                   input_messages_key='input', 
                                                   history_messages_key='history')
def chat_with_llm(session_id, input):
    output = runnable_with_history.invoke(
        {'input': input},
        config={'configurable': {'session_id': session_id}}
    )

    return output
user_id = "kgptalkie"
print(chat_with_llm(user_id, about))