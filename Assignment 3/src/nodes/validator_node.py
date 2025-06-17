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
from src.output_parsers.validator_parser import validator_parser
from langchain.prompts import PromptTemplate

class ValidatorNode:
    def __init__(self):
        print("Initializing ValidatorNode Class...")
        self.model_loader=ModelLoader()
        self.llm = self.model_loader.load_llm()
    
    def validator_llm_response_prompt(self):
        validator_llm_response_template = """
            You are an expert tasked with evaluating the quality of AI-generated responses. 
            Your evaluation should be thorough and based on the following evaluation criteria:

            Evaluation Criteria:  
            1. Relevance to Query: Does the response directly address the query and relevant to the question topic?  
            2. Factual Accuracy: Is response factually correct and supported by evidence or reliable knowledge?  
            3. Completeness: Does the response fully answer the query, covering all necessary aspects without omitting key details?  
            4. Source Citation: If sources are mentioned, are they credible, relevant, and properly cited with clear attribution?


            Query: {query}

            Response: {intermediate_response}

            {format_output}
            """
        llm_validator_prompt = PromptTemplate(
            template=validator_llm_response_template,
            input_variables=["query","intermediate_response"],
            partial_variables={"format_output":validator_parser.get_format_instructions()}
        )
        return llm_validator_prompt
    
    def validator_rag_response_prompt(self):
        validator_rag_response_template = """
            You are an expert tasked with evaluating the quality of AI-generated responses. 
            Your evaluation should be thorough and based on the following evaluation criteria:

            Evaluation Criteria:  
            1. Relevance to Query: Does the response directly address the query and relevant to the question topic?  
            2. Factual Accuracy: Is response factually correct and supported by evidence or reliable knowledge?  
            3. Completeness: Does the response fully answer the query, covering all necessary aspects without omitting key details?  
            4. Source Citation: If sources are mentioned, are they credible, relevant, and properly cited with clear attribution?


            Query: {query}

            Response: {intermediate_response}

            {format_output}
            """
        rag_validator_prompt = PromptTemplate(
            template=validator_rag_response_template,
            input_variables=["query","intermediate_response"],
            partial_variables={"format_output":validator_parser.get_format_instructions()}
        )
        return rag_validator_prompt

    def function_validation(self, state:AgentState):
        print("-> Inside Function Validator <-")
        question = state["messages"][0]
        answer = state["messages"][-1]
        context = state["contexts"]
        print(f"context: {context}")
        if not context:
            print("Context is empty")
            validator_llm_chain = self.validator_llm_response_prompt | self.llm | validator_parser
            response = validator_llm_chain.invoke({
            "query": question,
            "intermediate_response": answer
            })
        else:
            print("Context is not empty")
            validator_rag_chain = self.validator_rag_response_prompt | self.llm | validator_parser
            response = validator_rag_chain.invoke({
                "query": question,
                "context": context,
                "intermediate_response": answer
                })
        return {"messages": [response.Is_Valid]}

if __name__ == "__main__":
    supervisor = ValidatorNode()
    state={"messages":["What is the current weather of West Bengal?"]}
    response = supervisor.function_supervisor(state)
    print(response)