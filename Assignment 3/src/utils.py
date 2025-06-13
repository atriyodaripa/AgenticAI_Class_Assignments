from langchain_groq import ChatGroq
from config import INFERENCE_MODEL

def get_llm_model():
    try:
        llm = ChatGroq(model=INFERENCE_MODEL)
        return llm
    except Exception as e:
        raise e