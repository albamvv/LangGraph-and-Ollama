# Chat message memory

## Overview

- We need to store the historical chat messages in a efficient way
- It wraps another Runnable and manages the chat message history for it.
- Specifically, it loads previous messages in the conversation BEFORE passing it to the Runnable, and it saves the generated response as a message AFTER calling the runnable.
- This class also enables multiple conversations by saving each conversation with a `session_id` it then expects a `session_id` to be passed in the config when calling the runnable, and uses that to look up the relevant conversation history
![Alt text](assets/memory_flow.JPG)

## Usage

```sh
   python chat_message_memory.py
```

## Implementation

**1. Simple chain**

```python
   base_url = "http://localhost:11434"
model = 'llama3.2:3b' # Specify the model to be used (Llama 3.2 with 3 billion parameters)
llm = ChatOllama(base_url=base_url, model=model) # Initialize the ChatOllama model with the base URL and model

template = ChatPromptTemplate.from_template("{prompt}") # Create a chat prompt template that accepts a variable input as "prompt"
chain = template | llm | StrOutputParser() # Create a processing chain: the template is passed to the LLM, and the response is parsed into a string using StrOutputParser

about = "My name is Alba Vadillo. I work for KGP Talkie."
response1=chain.invoke({'prompt': about})
print("response1-> ",response1)
#------------------------
prompt = "What is my name?"
response2=chain.invoke({'prompt': prompt})
print("response2-> ",response2)
```
**Output:**

```sh
   response1->  Hello Alba, it's nice to meet you! Welcome to our conversation. KGP Talkies, that sounds like an interesting company. What does KGP Talkie do, if I might ask?
   response2->  I don't have any information about you, so I don't know your name. We just started our conversation, and I'm here to help answer any questions or provide information on a wide range of topics. How can I assist you today?
```

It looks like the model isn't retaining context between responses. This is likely because:

- Stateless Execution: Each invocation of `chain.invoke()` is independent, meaning the model doesn't remember previous inputs.
- Lack of Memory Component: LangChain allows memory modules to maintain conversational context, but your setup doesn't include one.

**2. Runable with history**

In order to properly set this up there are two main things to consider:
- How to store and load messages?
- What is the underlying Runnable you are wrapping and what are its inputs/outputs?

- This script stores and retrieves conversation history using SQLite.
- The function `get_session_history(session_id)` ensures each user has a separate conversation history.
- `RunnableWithMessageHistory` wraps the main processing chain (`chain`) to maintain memory.
- By using the same `session_id` (`user_id`), the model should remember previous interactions.
- The `invoke()` calls simulate a conversation where the model should recall the user’s name from history.

**3. Message History with Dictionary Like Inputs**
# Build your own chatbot