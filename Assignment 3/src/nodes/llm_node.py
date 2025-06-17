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
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LLMNode:
    def __init__(self):
        print("Initializing LLMNode Class...")
        self.model_loader=ModelLoader()
        self.llm = self.model_loader.load_llm()
        
    def function_llm(self, state:AgentState):
        print("-> Inside LLM Node <-")
        question = state["messages"][0]        
        # Normal LLM call
        llm_template="""
        You are an assistant for question-answering tasks. 

        Provide a clear and concise response to the following user questions.
        User Query: {question}
        """
        llm_prompt=PromptTemplate(
            template=llm_template,
            input_variables=["question"]
        )
        llm_chain = llm_prompt | self.llm | StrOutputParser()
        response = llm_chain.invoke({"question":question})
        return {"messages": [response]}

if __name__ == "__main__":
    llm = LLMNode()
    state={"messages":["Hi"]}
    response = llm.function_llm(state)
    print(response)