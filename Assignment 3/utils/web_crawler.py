import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir,os.pardir)
)
sys.path.append(PROJECT_ROOT)
print(sys.path)
from langchain_tavily import TavilySearch


class WebCrawler:
    def __init__(self):
        self.tavily_tool = TavilySearch(max_results=5, topic="news")
        
    def web_retriever(self, query):
        # query = inputs["question"]
        result = self.tavily_tool.invoke({"query": query})
        snippets = [r["content"] for r in result["results"] if "content" in r]
        # return "\n\n".join(snippets)
        return {"context": "\n\n".join(snippets), "question": query}