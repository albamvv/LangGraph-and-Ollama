from imports import*  # Import all necessary modules

st.title("Alba's Chatbot")  # Set the title of the chatbot application
st.write("WE CAN START NOW")  # Display an introductory message

# Define base URL and model for the chatbot
base_url = "http://localhost:11434"
model = 'llama3.2:3b'
user_id = "Alba Vadillo"

# Function to retrieve chat session history from the database
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

# Initialize chat history if it does not exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Button to start a new conversation
if st.button("Start New Conversation"):
    st.session_state.chat_history = []  # Clear chat history in session state
    history = get_session_history(user_id)
    history.clear()  # Clear stored history in the database

# Display previous chat messages from session history
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

### LLM (Language Model) Setup
llm = ChatOllama(base_url=base_url, model=model)  # Initialize chatbot model
system = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")  # Define system role
human = HumanMessagePromptTemplate.from_template("{input}")  # Define user input template
messages = [system, MessagesPlaceholder(variable_name='history'), human]  # Define message structure
prompt = ChatPromptTemplate(messages=messages)  # Create chat prompt template

# Create a processing chain for chatbot responses
chain = prompt | llm | StrOutputParser()
runnable_with_history = RunnableWithMessageHistory(
    chain, get_session_history, 
    input_messages_key='input', 
    history_messages_key='history'
)

# Function to process chat input and generate responses
def chat_with_llm(session_id, input):
    for output in runnable_with_history.stream({'input': input}, config={'configurable': {'session_id': session_id}}):
        yield output  # Stream responses as they are generated

# Input field for user messages
prompt = st.chat_input("What is up?")

if prompt:
    # Store user message in session history
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)  # Display user message
    
    with st.chat_message("assistant"):
        response = st.write_stream(chat_with_llm(user_id, prompt))  # Generate and display assistant response
    
    # Store assistant response in session history
    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
