from .calculator_tool import CalculatorTool
from .currency_conversion_tool import CurrencyConverterTool
from .place_search_tool import PlaceSearchTool
from .weather_info_tool import WeatherInfoTool

# Collect tools (these are decorated tool functions attached to the class)
__all__ = []

# def get_tools_from_class(cls):
#     return [getattr(cls, attr) for attr in dir(cls) if callable(getattr(cls, attr)) and hasattr(getattr(cls, attr), "args_schema")]
def get_tools_from_class(cls):
    return {
        attr: getattr(cls, attr)
        for attr in dir(cls)
        if callable(getattr(cls, attr)) and hasattr(getattr(cls, attr), "args_schema")
    }


# Flatten and expose
tool_classes = [CalculatorTool, CurrencyConverterTool, PlaceSearchTool, WeatherInfoTool]
__tools__ = []
for cls in tool_classes:
    tools = get_tools_from_class(cls)
    __tools__.extend(tools)

# for cls in tool_classes:
#     tools = get_tools_from_class(cls)
#     all_tools.extend(tools)
#     __all__.extend([tool.name for tool in tools])

# __tools__ = all_tools
# __all__.append("__tools__")
# Make tools accessible as module-level names
# Step 2: Register each tool as a global symbol by its `.name`
for tool in __tools__:
    globals()[tool.name] = tool  # Register as top-level symbol
# globals().update(all_tools)

# # Also export as a list
# __tools__ = list(all_tools.values())

# # Set __all__ for import *
# __all__ = list(all_tools.keys()) + ["__tools__"]

# Step 3: Add all tools themselves to __all__
__all__ = [tool.name for tool in __tools__] + ["__tools__"]
