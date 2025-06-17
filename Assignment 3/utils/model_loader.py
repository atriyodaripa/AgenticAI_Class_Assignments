import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from utils.config_loader import load_config
from langchain_groq import ChatGroq

class ModelLoader:
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config=load_config()
    
    def _validate_env(self):
        required_vars = ["TAVILY_API_KEY","GROQ_API_KEY"]
        self.groq_api_key=os.getenv("GROQ_API_KEY")
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
    
    def load_embeddings(self):
        """
        Load and return the embedding model.
        """
        print("Loading Embedding model")
        model_name=self.config["embedding_model"]["model_name"]
        return HuggingFaceEmbeddings(model=model_name)
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        model_name=self.config["llm"]["model_name"]
        print(self.groq_api_key)
        llm=ChatGroq(model=model_name,api_key=self.groq_api_key)
        
        return llm 