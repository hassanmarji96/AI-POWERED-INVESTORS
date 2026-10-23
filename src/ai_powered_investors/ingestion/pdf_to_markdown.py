from pathlib import Path
import pymupdf4llm

class PDFToMarkDownConverter:
    """_summary_: Questa classe si occupa di convertire i file passati nella ingestion dal formato PDF, a markdown.
    Ciò viene fatto in quanto i file MD, preservano la struttura, di conseguenza, facilita ed aiuta la fase di chunking
    """
    
    def convert_pdf(self, pdf_path: str, output_dir: str) -> str:
        """_summary_
        Converte un documento PDF in un file markdown strutturato
        Args:
            pdf_path (str): cartella sorgente in cui è contenuto il file
            output_dir (str): cartella di destinazione

        Returns:
            Markdown file generato
        """
        pdf_file = Path(pdf_path)
        
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF File not found in : {pdf_path}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        