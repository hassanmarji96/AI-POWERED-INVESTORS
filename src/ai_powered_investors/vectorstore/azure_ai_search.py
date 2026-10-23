import uuid
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from types import SimpleNamespace
from langchain_core.embeddings import Embeddings
from langchain_core.documents import (Document)


class AzureAISearchVectorStore:
    
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        index_name: str
    ) -> None:
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )
    
    def upload_chunks(
        self,
        chunks: list[Document],
        embeddings: Embeddings,
        company: str,
        year: str,
        source_file: str
    ) -> None:
        """_summary_ Carico i chunk nel servizio Azure AI Search

        Args:
            chunks (list[Document]): chunk
            embeddings (Embeddings): modello embedded
            company (str): nome azienda
            year (str): anno revenue
            source_file (str): file sorgente
        """
        documents = list()
        
        for chunk in chunks:
            vector = embeddings.embed_query(chunk.page_content)
            documents.append(
                {
                    "id": str(uuid.uuid4()),
                    "company": company,
                    "year": year,
                    "source_file": source_file,
                    "content": chunk.page_content,
                    "content_vector": vector
                }
            )
        
        result = self.client.upload_documents(documents=documents)
        uploaded = sum(item.succeeded for item in result)
        
        print(f"Chunks caricati: {uploaded}/{len(chunks)}")
        
class Retriever:
    """_summary_ Wrapper che gira sul servizio Azure Seach per fetchare i chunks più rilevanti.
    Funge come da componente retriever dell'estrattore RAG
    """
    
    def __init__(self, client: SearchClient):
        self.client = client
        
    def invoke(
        self,
        query: str,
        company: str | None = None,
        year: int | None = None,
        top_k: int = 20
    ) -> list[Document]:
        """_summary_ Ottiene i chunk più rilevanti dal servizio Azure AI Search

        Args:
            query (str): _description_
            company (str | None, optional): _description_. Defaults to None.
            year (int | None, optional): _description_. Defaults to None.
            top_k (int, optional): _description_. Defaults to 20.

        Returns:
            list: una lista di oggetti di tipo SimpleNamespace con il `page_content`
        """
        
        filter_expr = None
        if all([company, year]):
            filter_expr = (
                f"company eq '{company}'",
                f"year eq '{year}'"
            )
        results = (
            self.client.search(
                search_text= query,
                top=top_k,
                filter= filter_expr
            )
            if filter_expr
            else self.client.search(
                search_text=query,
                top=top_k
            )
        )
        
        documents = []
        for result in results:
            content = result.get("content", "")
            documents.append(SimpleNamespace(page_content=content))
            
        return documents
            