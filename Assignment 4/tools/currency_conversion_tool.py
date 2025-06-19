from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool

class CurrencyConverterTool:
    def __init__(self, api_key:str):
        self.currency_service = CurrencyConverter(api_key)

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""
        @tool
        def convert_currency(amount:float, from_currency:str, to_currency:str):
            """Convert amount from one currency to another"""
            return self.currency_service.convert(amount, from_currency, to_currency)
        
        return [convert_currency]