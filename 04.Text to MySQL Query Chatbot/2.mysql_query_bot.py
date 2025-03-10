from query_utils import write_query,execute_query, generate_answer
from config import State

# Ask how many employees are in the database
user_question = "how many employees are there?"
#question = "List all the albums"
query = write_query({"question": user_question})
print("query-> ",query)

# Execute the generated query
result = execute_query(query)
print("result-> ",result)

# Combine all information into a state dictionary
state_dict= {"question": user_question, **query, **result}
print("state ->",state_dict)

# Generate and print the final answer
print("answer-> ",generate_answer(state_dict))



