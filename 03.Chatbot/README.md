# Chat message memory

## Overview

- We need to store the historical chat messages in a efficient way
- It wraps another Runnable and manages the chat message history for it.
- Specifically, it loads previous messages in the conversation BEFORE passing it to the Runnable, and it saves the generated response as a message AFTER calling the runnable.
- This class also enables multiple conversations by saving each conversation with a `session_id` it then expects a `session_id` to be passed in the config when calling the runnable, and uses that to look up the relevant conversation history
![Alt text](assets/memory_flow.JPG)


# Build your own chatbot