import os
import json
from langchain_tavily import TavilySearch
from langchain_google_community import GooglePlacesTool, GooglePlacesAPIWrapper 

class GooglePlaceSearchTool:
    def __init__(self, api_key: str):
        self.places_wrapper = GooglePlacesAPIWrapper(gplaces_api_key=api_key)
        self.places_tool = GooglePlacesTool(api_wrapper=self.places_wrapper)
    
    def google_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"top attractive places in and around {place}")
    
    def google_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"what are the top 10 restaurants and eateries in and around {place}?")
    
    def google_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"Activities in and around {place}")

    def google_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using GooglePlaces API.
        """
        return self.places_tool.run(f"What are the different modes of transportations available in {place}")

class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    # def _run(self, query: str, **kwargs) -> str:
    #     """
    #     Runs the tool. The query is expected to be a JSON string with two keys:
    #       - "operation": One of ["attractions", "restaurants", "activities", "transportation"]
    #       - "place": The location to search.
          
    #     Example input:
    #       {"operation": "attractions", "place": "Paris"}
    #     """
    #     try:
    #         print(query)
    #         data = json.loads(query)
    #         print("$$$$$$$$$$$$$$$$")
    #     except Exception as e:
    #         return f"Error parsing input: expected a JSON formatted string. Details: {str(e)}"

    #     operation = data.get("operation")
    #     place = data.get("place")
    #     if not operation or not place:
    #         return "Input error: please specify both 'operation' and 'place'."

    #     if operation == "attractions":
    #         result = self.search_attractions(place)
    #     elif operation == "restaurants":
    #         result = self.search_restaurants(place)
    #     elif operation == "activities":
    #         result = self.search_activity(place)
    #     elif operation == "transportation":
    #         result = self.search_transportation(place)
    #     else:
    #         return (f"Unsupported operation '{operation}'. "
    #                 "Choose from attractions, restaurants, activities, or transportation.")

    #     return json.dumps(result, indent=2)