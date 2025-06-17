import sys
import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir,os.pardir)
)
sys.path.append(PROJECT_ROOT)
print(sys.path)
from utils.model_loader import ModelLoader
from src.state import AgentState
from src.output_parsers.supervisor_parser import supervisor_parser
from langchain.prompts import PromptTemplate

class SupervisorNode:
    def __init__(self):
        print("Initializing LLMNode Class...")
        self.model_loader=ModelLoader()
        self.llm = self.model_loader.load_llm()

    def function_supervisor(self, state:AgentState):
        print("-> Inside Supervisor Function <-")
        question = state["messages"][-1]
        # print(f"Question: {question}")

        superviser_template = """
        You are an expert in wildlife photography. Your task is to classify the user's query into one of the following categories: 
        [Unrelated, Wildlife Photography, real-time info]

        only respond with the category name and nothing more than that.

        User Query: {question}
        {format_output}
        """

        supervisor_prompt = PromptTemplate(
            template=superviser_template,
            input_variables=["question"],
            partial_variables={"format_output":supervisor_parser.get_format_instructions()}
        )

        supervisor_chain = supervisor_prompt | self.llm | supervisor_parser
        response = supervisor_chain.invoke({"question":question})

        print("Parsed response", response)
        return {"messages": [response.Topic]}

if __name__ == "__main__":
    supervisor = SupervisorNode()
    state={"messages":["What is the current weather of West Bengal?"]}
    response = supervisor.function_supervisor(state)
    print(response)