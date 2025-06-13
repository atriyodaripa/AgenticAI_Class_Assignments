import os
from dotenv import load_dotenv
load_dotenv()

## Getting Groq API key
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
## Getting TAVILY API key
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

# LLM models for embedding and inferencing
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
INFERENCE_MODEL = "gemma2-9b-it"
