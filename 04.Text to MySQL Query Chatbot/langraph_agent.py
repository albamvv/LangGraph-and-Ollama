from langchain import hub

# LangGraph AGENTS: Automating query execution with AI
'''
# Agents can:
# - Query the database multiple times to refine their answer.
# - Recover from errors by detecting failed queries and regenerating them.
# - Answer questions based on both schema structure and database content.
'''

prompt = hub.pull("langchain-ai/sql-agent-system-prompt")
prompt.messages[0].pretty_print()
