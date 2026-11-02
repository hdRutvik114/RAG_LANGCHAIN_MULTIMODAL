import fitz
from pathlib import Path
from langchain_core.documents import Document


def load_pdf_documents(file_path: str) -> list[Document]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    documents = []

    with fitz.open(str(path)) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": path.name,
                            "page": page_number
                        }
                    )
                )

    if not documents:
        raise ValueError(
            "No extractable text found. This PDF may need OCR."
        )

    return documents