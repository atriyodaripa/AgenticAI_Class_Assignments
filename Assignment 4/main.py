from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

# if __name__ == "__main__":
#     graph = GraphBuilder(model_provider="openai")
#     react_app = graph.build_graph()
#     png_graph = react_app.get_graph().draw_mermaid_png()
#     with open("my_graph.png", "wb") as f:
#         f.write(png_graph)

#     print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
#     query = """
#     Hi, I want to take a 12-day trip to Ladakh and Nubra Valley in August 2025. 
#     My hotel budget is around 1300 Rs per night person. I would mostly prefer homestays for night stay. Suggest me some
#     good homestay in Nubra Valley, Pangong and other remote places. 
#     I would like to know what the weather will be like, what places I can visit, and how much the whole trip might cost. 
#     Also, I prefer local food and public transportation. Can you plan it all for me?
#     """
#     output = react_app.invoke({"messages":[query]})
#     print(output)
#     for m in output["messages"]:
#         m.pretty_print()
#     save_document(output["messages"][-1].content)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print(query)
        graph = GraphBuilder(model_provider="openai")
        react_app = graph.build_graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})