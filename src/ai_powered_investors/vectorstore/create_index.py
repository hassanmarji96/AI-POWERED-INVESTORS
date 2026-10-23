from dotenv import load_dotenv
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SearchableField,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)

load_dotenv()

def create_index(
    endpoint: str,
    api_key: str,
    index_name: str,
    embedding_dimensions: int = 1536
) -> None:
    """_summary_ Crea un indice vettoriale su Azure

    Args:
        endpoint (str): Azure AI Search endpoint.
        api_key (str): Azure AI Search API key.
        index_name (str): Index name.
        embedding_dimensions (str): Embedding dimensions.
    """
    
    client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )
    
    # Definisco i campi e metadati del mio store vettoriale
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.STRING, key=True),
        SimpleField(name="company", type=SearchFieldDataType.STRING, filterable=True),
        SimpleField(name="year", type=SearchFieldDataType.STRING, filterable=True),
        SimpleField(name="source_file", type=SearchFieldDataType.STRING, filterable=True),
        SearchField(name="content", type=SearchFieldDataType.STRING, filterable=True),
        SearchableField(name="metadata",type=SearchFieldDataType.String),
        SearchField(
            name="content_vector", 
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=embedding_dimensions,
            searchable=True,
            vector_search_profile_name="vector-profile"
        )
    ]
    
    # La ricerca vettoriale non sarà fatta per match esatto, ma con Hierarchical Navigable Small World
    # che non mi assicura il match con il vettore più vicino, ma con i vettori dell'intorno più vicino
    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="hnsw-config")
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config"
            )
        ]
    )
    
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search
    )
    
    client.create_or_update_index(index=index)
    print(f"Indice vettoriale '{index_name}' creato con successo")
    
if __name__ == "__main__":
    create_index(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        api_key=os.getenv("AZURE_SEARCH_API_KEY"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME")
    )