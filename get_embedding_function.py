#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

def get_embedding_function():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",  
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    return embeddings

  