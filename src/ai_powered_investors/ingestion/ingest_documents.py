import os
from pathlib import Path
from ai_powered_investors.utils import get_embedding_model, get_vector_store
from ai_powered_investors.ingestion.pdf_to_markdown import PDFToMarkDownConverter
from ai_powered_investors.ingestion.semantic_chunker import chunk_markdown
from ai_powered_investors.rag.kpi_extractor_rag import Retriever, extract_financial_metrics
from ai_powered_investors.database.save_metrics import save_metrics
from langchain_community.vectorstores.azuresearch import AzureSearch
from ai_powered_investors.vectorstore.azure_ai_search import AzureAISearchVectorStore

from dotenv import load_dotenv

load_dotenv()

def parse_company_year(pdf_file: Path) -> tuple[str, str]:
    """_summary_ Converte l'azienda e l'anno a partire dal file PDF

    Args:
        pdf_file (Path): Nome del file PDF

    Returns:
        tuple[str, str]: Tupla con nome ed anno dell'azienda
    """
    stem = pdf_file.stem
    parts = stem.split("_")
    
    if parts and parts[0].isdigit():
        year = parts[0]
        company = parts[-1]
    elif len(parts) >= 2:
        company = parts[0]
        year = parts[1]
    else:
        company = stem
        year = ""

    return company, year
        
def ingest_document(
    pdf_path: str,
    embeddings,
    vector_store: AzureAISearchVectorStore
) -> None:
    pdf_file = Path(pdf_path)
    
    company, year = parse_company_year(pdf_file=pdf_file)
    print(f"Caricando ed elaborando: {pdf_file}. Azienda: {company!r} - anno: {year!r}")
    
    pdf_to_markdown_converter = PDFToMarkDownConverter()
    
    markdown_file = pdf_to_markdown_converter.convert_pdf(
        pdf_path=pdf_path,
        output_dir = str(Path(__file__).resolve().parents[3] / "data" / "markdown")
    )
    
    chunks = chunk_markdown(
        markdown_file=markdown_file,
        embeddings=embeddings
    )
    
    print(f"Generati: {len(chunks)} per il file: {pdf_file.name}")
    
    vector_store.upload_chunks(
        chunks=chunks,
        embeddings=embeddings,
        company=company,
        year=year,
        source_file=pdf_file.name
    )
    
    # metrics = extract_financial_metrics(
    #     retriever=Retriever(vector_store.client),
    #     company=company,
    #     year=int(year) if year.isdigit() else None
    # )

    # # Persist metrics to PostgreSQL
    # if metrics:
    #     save_metrics(company=company, year=int(year) if str(year).isdigit() else None, metrics=metrics)
    
def ingest_directory(input_dir: str) -> None:
    """_summary_ Esegue l'ingesting di tutta la directory

    Args:
        input_dir (str): directory di riferimento
    """
    
    embeddings = get_embedding_model()
    vector_store = get_vector_store(embedding_model=embeddings)
    
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    
    print(f"Ho trovato {len(pdf_files)} files in formato pdf")
    
    for pdf_file in pdf_files:
        ingest_document(
            pdf_path=str(pdf_file),
            embeddings=embeddings,
            vector_store=vector_store
        )

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[3]
    
    embeddings = get_embedding_model()
    vector_store = AzureAISearchVectorStore(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        api_key=os.environ["AZURE_SEARCH_API_KEY"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"]
    )
    
    ingest_document(
        pdf_path=str(repo_root / "data" / "raw_pdf" / "2024_Apple.pdf"),
        embeddings=embeddings,
        vector_store=vector_store
    )