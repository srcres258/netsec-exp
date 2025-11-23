from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

def make_final_pdf(
    cover_pdf_path: str,
    source_pdf_path: str,
    output_pdf_path: str
) -> None:
    writer = PdfWriter()
    
    assert Path(cover_pdf_path).exists(), f"Cover PDF file not found: {cover_pdf_path}"
    assert Path(source_pdf_path).exists(), f"Source PDF file not found: {source_pdf_path}"
    
    with open(cover_pdf_path, "rb") as cover_file:
        cover_pdf = PdfReader(cover_file)
        writer.add_page(cover_pdf.pages[0])
    with open(source_pdf_path, "rb") as source_file:
        source_pdf = PdfReader(source_file)
        for page in source_pdf.pages:
            writer.add_page(page)
    
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

LAB_COUNT: int = 4

if __name__ == "__main__":
    for i in range(1, LAB_COUNT + 1):
        cover_pdf_path = f"lab{i}_cover.pdf"
        source_pdf_path = f"lab{i}.pdf"
        output_pdf_path = f"lab{i}_final.pdf"
        make_final_pdf(cover_pdf_path, source_pdf_path, output_pdf_path)
