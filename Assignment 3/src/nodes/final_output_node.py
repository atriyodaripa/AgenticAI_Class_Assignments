import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir,os.pardir)
)
sys.path.append(PROJECT_ROOT)
print(sys.path)
from src.state import AgentState

def function_final_output(state:AgentState):
    final_response = state["messages"][-2]
    print(f"Final response: {final_response}")
    return {"messages": [final_response]}