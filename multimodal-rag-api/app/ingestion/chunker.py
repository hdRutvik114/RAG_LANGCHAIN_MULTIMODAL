from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_document(document: Document) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
    )

    return splitter.split_documents([document])