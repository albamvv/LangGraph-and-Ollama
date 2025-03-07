from langgraph.graph import  START, StateGraph
from IPython.display import display, Image
from query_utils import write_query,execute_query, generate_answer

# Ask how many employees are in the database
question = "how many employees are there?"
#question = "List all the albums"
query = write_query({"question": question})
print("query-> ",query)

# Execute the generated query
result = execute_query(query)
print("result-> ",result)

# Combine all information into a state dictionary
state = {"question": question, **query, **result}
print("state ->",state)

# Generate and print the final answer
print("answer-> ",generate_answer(state))

