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
        
        markdown_content = pymupdf4llm.to_markdown(str(pdf_file))
        markdown_file = output_path / f"{pdf_file.stem}.md"
        
        markdown_file.write_text(
            markdown_content,
            encoding="utf-8"
        )
        
        return str(markdown_file)
    
    def convert_all_files_in_directory(self, input_dir: str, outpu_dir: str) -> list[str]:
        """_summary_ Converto tutti i file presenti all'interno di una directory

        Args:
            input_dir (str): cartella sorgente in cui è contenuto il file
            outpu_dir (str): cartella di destinazione

        Returns:
            list[str]: Lista generata dei file MD
        """
        
        input_path = Path(input_dir)
        markdown_files = list()
        
        for pdf_file in input_path.glob("*.pdf"):
            markdown_file = self.convert_pdf(
                pdf_path=pdf_file,
                output_dir=outpu_dir
            )
            
            markdown_files.append(markdown_file)
        
        return markdown_files
    
if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[3]
    
    print(f"Cartella sorgente: {repo_root}")
    
    input_dir = repo_root/"data"/"raw_pdf"
    output_dir = repo_root/"data"/"markdown"
    
    pdf_to_markdown_converter = PDFToMarkDownConverter()
    
    markdown_files = pdf_to_markdown_converter.convert_all_files_in_directory(
        input_dir=input_dir,
        outpu_dir=output_dir
    )
    
    print(f"L'intera cartella è stata convertita con successo. PDF convertiti con successo: {len(markdown_files)}")
    
    for markdown_file in markdown_files:
        print(f"  - {markdown_file}")
            
        