from pathlib import Path
from langchain_core.documents import (Document)
from langchain_openai import AzureOpenAIEmbeddings

from dotenv import load_dotenv
import os

load_dotenv()


    
def get_embedding_model(
    model: str="text-embedding-3-small"
):
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    embedding_model = os.getenv("AZURE_OPENAI_DEPLOYMENT", model)
    if not endpoint or not api_key:
        raise RuntimeError(
            "Missing Azure OpenAI credentials. Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in your environment!"
        )
    
    embeddings = AzureOpenAIEmbeddings(
        api_key=api_key,
        azure_endpoint=endpoint,
        azure_deployment=embedding_model,
        model = model,
        api_version=api_version
    )
    return embeddings
