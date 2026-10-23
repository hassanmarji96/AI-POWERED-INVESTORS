from pathlib import Path
from langchain_core.documents import (Document)
from langchain_experimental.text_splitter import SemanticChunker
from dotenv import load_dotenv
from ai_powered_investors.utils import get_embedding_model


load_dotenv()

def read_markdown(markdown_file: str) -> str:
    """_summary_ Leggo un determinato file MD

    Args:
        markdown_file (str): percorso del file MD

    Returns:
        str: Contenuto del file
    """
    return Path(markdown_file).read_text(encoding="utf-8")

def chunk_markdown(
    markdown_file: str,
    embeddings
) -> list[Document]:
    """_summary_ Genera dei chunk semantici a partire dai documenti del markdown

    Args:
        markdown_file (str): percorso del file MD
        embeddings (_type_): Modello embedded di Azure OpenAI

    Returns:
        list[Document]: lista di chunk semantici
    """
    
    markdown_content = read_markdown(markdown_file=markdown_file)
    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile"
    )
    return splitter.create_documents([markdown_content])

if __name__ == "__main__":
    embedding_model = get_embedding_model()
    
    markdown_file = str(Path(__file__).resolve().parents[3] / "data" / "markdown" / "2024_Apple.md")
    
    chunks = chunk_markdown(
        markdown_file=markdown_file,
        embeddings=embedding_model
    )
    
    for index, chunk in enumerate(chunks[:3]):
        print("="*80)
        print(f"Chunk: {index + 1}")
        print("="*80)
        print(chunk.page_content[:1000])
        print()
        
    
    
    