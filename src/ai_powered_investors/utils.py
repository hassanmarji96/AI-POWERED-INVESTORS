from pathlib import Path
from langchain_core.documents import (Document)
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.embeddings import Embeddings

from dotenv import load_dotenv
import os

load_dotenv()


    
def get_embedding_model(
    model: str="text-embedding-3-small"
) -> AzureOpenAIEmbeddings:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    embedding_model = os.getenv("AZURE_OPENAI_DEPLOYMENT", model)
    if not all([
        endpoint,
        api_key
    ]):
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

def get_vector_store(embedding_model: Embeddings) -> AzureSearch:
    vector_store_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    vector_store_api_key = os.getenv("AZURE_SEARCH_API_KEY")
    vector_store_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    
    if not all([
        vector_store_endpoint,
        vector_store_api_key,
        vector_store_index_name
    ]):
        raise RuntimeError("Missing Azure AI Search configuration.")
    
    return AzureSearch(
        azure_search_endpoint=vector_store_endpoint,
        azure_search_key=vector_store_api_key,
        index_name=vector_store_index_name,
        embedding_function= embedding_model.embed_query
    )
