from langchain_community.vectorstores import FAISS

from document_processor import extract_text_from_pdf
from chunking import create_chunks
from embeddings import get_embedding_model
from langchain_core.documents import Document


def create_vector_store(resume_path, jd_path):

    # 1. Load documents

    resume_text = extract_text_from_pdf(resume_path)

    jd_text = extract_text_from_pdf(jd_path)

    # 2. Create chunks

    resume_chunks = create_chunks(
        resume_text,
        document_type="resume"
    )

    jd_chunks = create_chunks(
        jd_text,
        document_type="job_description"
    )

    all_chunks = resume_chunks + jd_chunks

    # 3. Convert chunks to LangChain Documents

    documents = [
        Document(
            page_content=chunk["text"],
            metadata=chunk["metadata"]
        )
        for chunk in all_chunks
    ]

    # 4. Load embedding model

    embedding_model = get_embedding_model()

    # 5. Create FAISS vector store

    vector_store = FAISS.from_documents(
        documents,
        embedding_model
    )

    return vector_store