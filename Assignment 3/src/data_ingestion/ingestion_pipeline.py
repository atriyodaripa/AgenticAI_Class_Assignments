import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir,os.pardir)
)
sys.path.append(PROJECT_ROOT)
from typing import List
from dotenv import load_dotenv
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
import chromadb



class DataIngestion:
    """
    Class to handle data transformation and ingestion into AstraDB vector store.
    """

    def __init__(self):
        """
        Initialize environment variables, embedding model, and set CSV file path.
        """
        print("Initializing DataIngestion pipeline...")
        self.model_loader=ModelLoader()
        self._load_env_variables()
        self._load_data()
        # self.product_data = self._load_data()
        self.config=load_config()
        self.chroma_client = chromadb.PersistentClient(path="./vector_db")
    
    def _load_env_variables(self):
        """
        Load and validate required environment variables.
        """
        load_dotenv()
        
        required_vars = ["GROQ_API_KEY"]
        
        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")
    
    def _load_data(self):
        """
        Get path to the data file located inside 'data' folder.
        """
        loader = DirectoryLoader("./data", glob="./*.pdf", loader_cls=PyPDFLoader)
        self.docs = loader.load()
    
    def split_data(self):
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        splitted_docs = text_splitter.split_documents(documents=self.docs)
        return splitted_docs
    
    def store_in_vector_db(self, documents: List[Document]):
        """
        Store documents into AstraDB vector store.
        """
        collection_name=self.config["chroma_db"]["collection_name"]
        embeddings = self.model_loader.load_embeddings()
        existing_collections = [col.name for col in self.chroma_client.list_collections()]
        print(f"********{existing_collections}*********")
        if collection_name not in existing_collections:
            print(f"Collection '{collection_name}' does not exist. Creating and adding documents...")
            # Create new collection and add documents
            vectordb=Chroma.from_documents(documents, embeddings, collection_name=collection_name, persist_directory="./vector_db")
        else:
            print(f"Collection '{collection_name}' exists. Loading...")
            collection = self.chroma_client.get_collection(name=collection_name)
            vectordb = Chroma(
                client=self.chroma_client,
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory="./vector_db"  # Make sure to include persist_directory here as well
            )
        self.retriever=vectordb.as_retriever(search_kwargs={"k": 5})
        print(f"Successfully inserted the embedded documents into ChromaDB.")
        return self.retriever
    
    def run_ingestion_pipeline(self):
        documents = self.split_data()
        self.retriever = self.store_in_vector_db(documents)

        # Optionally do a quick search
        query = "Can you tell me the low budget headphone?"
        results = self.retriever.invoke(query)

        # print(f"\nSample search results for query: '{query}'")
        # for res in results:
        #     print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")
        
        return self.retriever 


if __name__ == "__main__":
    d = DataIngestion()
    d.run_ingestion_pipeline()
