from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class ValidationParser(BaseModel):
    Is_Valid: bool=Field(description="Is the query valid or not")
    Reason: str=Field(description="Reasoining behind marking a response valid or invalid")

validator_parser = PydanticOutputParser(pydantic_object=ValidationParser)
