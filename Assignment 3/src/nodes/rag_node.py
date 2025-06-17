import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir,os.pardir)
)
sys.path.append(PROJECT_ROOT)
# print(sys.path)
from utils.model_loader import ModelLoader
from src.data_ingestion.ingestion_pipeline import DataIngestion
from src.state import AgentState
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

class RAGNode:
    def __init__(self):
        print("Initializing RAGNode Class...")
        self.model_loader=ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.rag = DataIngestion()
        self.retriever = self.rag.run_ingestion_pipeline()
    
    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    def function_rag(self, state:AgentState):
        print("-> Inside RAG Node <-")
        question = state["messages"][0]

        rag_template="""
        You are a highly knowledgeable and reliable assistant having an extensive knowledge in wildlife photography. 
            
        Using the following pieces of retrieved context from the contexts, provide a clear and concise response to the user's question.
        If you don't know the answer, just say that you don't know. 
        
        Question: {question} 
        Context: {context} 
        Answer:
        """
        rag_prompt=PromptTemplate(
            template=rag_template,
            input_variables=["question"]
        )

        # context = format_docs(retriever.invoke(question))
        
        rag_chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )
        response = rag_chain.invoke(question)
        # print(response)
        return {"messages": [response],
                "contexts": [self._format_docs(self.retriever.invoke(question))]}

if __name__ == "__main__":
    rag = RAGNode()
    state={"messages":["What is framing in wild life photography?"]}
    response = rag.function_rag(state)
    print(response)