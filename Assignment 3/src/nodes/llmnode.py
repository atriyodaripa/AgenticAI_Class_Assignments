from src.utils import get_llm_model
from src.state import AgentState
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class LLMNode:
    def __init__(self):
        self.llm = get_llm_model()

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