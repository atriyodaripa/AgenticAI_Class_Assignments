import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir,os.pardir)
)
sys.path.append(PROJECT_ROOT)
# print(sys.path)
from src.state import AgentState

def function_router(state:AgentState):
    print("-> Inside Function Router <-")

    last_message = state["messages"][-1]
    print(f"last_message: {last_message}")

    if "wildlife photography" in last_message.lower():
        return "RAG Call"
    elif "unrelated" in last_message.lower():
        return "LLM Call"
    else:
        return "Web Crawler Call"

def validation_router(state:AgentState):
    print("-> Inside ValidationRouter <-")

    validation_message = state["messages"][-1]
    print(f"last_message: {validation_message}")

    if not validation_message:
        return False
    else:
        return True