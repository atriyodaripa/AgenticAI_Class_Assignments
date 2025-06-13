from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class TopicSelectionParser(BaseModel):
    Topic: str=Field(description="Selected Topic")
    Reasoning: str=Field(description="Reasoining behind topic selection")

supervisor_parser = PydanticOutputParser(pydantic_object=TopicSelectionParser)