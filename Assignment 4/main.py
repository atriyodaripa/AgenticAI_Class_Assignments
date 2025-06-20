from agent.workflow import GraphBuilder
from utils.save_to_document import save_document
import os
import datetime
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    graph = GraphBuilder(model_provider="openai")
    react_app = graph.build_graph()
    png_graph = react_app.get_graph().draw_mermaid_png()
    with open("my_graph.png", "wb") as f:
        f.write(png_graph)

    print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
    query = """
    Hi, I want to take a 12-day trip to Ladakh and Nubra Valley in August 2025. 
    My hotel budget is around 1300 Rs per night person. I would mostly prefer homestays for night stay. Suggest me some
    good homestay in Nubra Valley, Pangong and other remote places. 
    I would like to know what the weather will be like, what places I can visit, and how much the whole trip might cost. 
    Also, I prefer local food and public transportation. Can you plan it all for me?"
    """
    output = react_app.invoke({"messages":[query]})
    print(output)
    for m in output["messages"]:
        m.pretty_print()
    save_document(output["messages"][-1].content)