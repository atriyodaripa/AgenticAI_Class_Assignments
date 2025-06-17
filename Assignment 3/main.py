import os
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.supervisor_node import SupervisorNode
from src.nodes.llm_node import LLMNode
from src.nodes.rag_node import RAGNode
from src.nodes.web_crawler_node import WebCrawlerNode
from src.nodes.validator_node import ValidatorNode
from src.nodes.final_output_node import function_final_output
from src.nodes.node_router import function_router, validation_router

supervisor = SupervisorNode()
llm = LLMNode()
rag = RAGNode()
web_crawl = WebCrawlerNode()
validator = ValidatorNode()

workflow = StateGraph(AgentState)
workflow.add_node('Supervisor', supervisor.function_supervisor)
workflow.add_node('RAG', rag.function_rag)
workflow.add_node('LLM', llm.function_llm)
workflow.add_node('Web Crawler', web_crawl.function_web_crawl)
workflow.add_node("Validator", validator.function_validation)
workflow.add_node("Final Output", function_final_output)
workflow.set_entry_point('Supervisor')
workflow.add_conditional_edges(
    'Supervisor',
    function_router,
    {
        "RAG Call":"RAG",
        "LLM Call":"LLM",
        "Web Crawler Call":"Web Crawler"
    }
)
workflow.add_conditional_edges(
    'Validator',
    validation_router,
    {
        False: "Supervisor",
        True: "Final Output"
    }
)
workflow.add_edge("RAG", "Validator")
workflow.add_edge("LLM", "Validator")
workflow.add_edge("Web Crawler", "Validator")
workflow.set_finish_point("Final Output")
app = workflow.compile()

if __name__ == "__main__":
    png_graph = app.get_graph().draw_mermaid_png()
    with open("my_graph.png", "wb") as f:
        f.write(png_graph)

    print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
    output = app.invoke({"messages":["What is framing in photography?"]})
    print(f"Final response: {output["messages"][-1]}")