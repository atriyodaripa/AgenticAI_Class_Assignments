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
from langchain_tavily import TavilySearch
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

class WebCrawlerNode:
    def __init__(self):
        print("Initializing WebCrawlerNode Class...")
        self.model_loader=ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tavily_tool = TavilySearch(max_results=5, topic="news")
    
    def _web_retriever(self, query):
        # query = inputs["question"]
        result = self.tavily_tool.invoke({"query": query})
        snippets = [r["content"] for r in result["results"] if "content" in r]
        # return "\n\n".join(snippets)
        return {"context": "\n\n".join(snippets), "question": query}

    def function_web_crawl(self, state:AgentState):
        print("-> Inside Web Crawler <-")
        question = state["messages"][0]

        web_crawl_template="""
        You are an assistant with extensive knowledge about current affairs. 
        Using the following pieces of retrieved context from internet, provide a clear and concise response to the user's question.
        
        Question: {question}
        Context: {context}
        Answer:
        """
        web_crawl_prompt=PromptTemplate(
            template=web_crawl_template,
            input_variables=["question"]
        )

        web_crawl_chain = (
            RunnableLambda(self._web_retriever)
            | web_crawl_prompt
            | self.llm
            | StrOutputParser()
        )
        response = web_crawl_chain.invoke(question)
        return {"messages": [response],
                "contexts": [self._web_retriever(question)["context"]]}

if __name__ == "__main__":
    webcrawler = WebCrawlerNode()
    state={"messages":["What is the current weather of West Bengal?"]}
    response = webcrawler.function_web_crawl(state)
    print(response)