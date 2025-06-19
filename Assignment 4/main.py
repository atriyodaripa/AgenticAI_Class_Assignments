from tools.place_info_search import PlaceSearchTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(
    model_name="o4-mini"
)

place_search_tool = PlaceSearchTool()

tools=[place_search_tool.search_attractions, 
       place_search_tool.search_restaurants, 
       place_search_tool.search_activity, 
       place_search_tool.search_transportation]
llm_with_tools=llm.bind_tools(tools)

SYSTEM_PROMPT="You are a helpful assistant tasked to get the attractions, restaurants, activities and transportations of a " \
"given location using the list of tools provided. Obtain the informations as per the user requirement and then segregate " \
"the output as per the attractions, restaurants, activities and transportations"

input_question = [SYSTEM_PROMPT]+[HumanMessage(content="Give me details about Kolkata")]

if __name__ == "__main__":
    response = llm_with_tools.invoke(input_question)
    print(response)