from langchain_community.vectorstores import FAISS
import os


def create_vector_store(chunks, embeddings):
    """
    Create a FAISS vector database from document chunks.
    """

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "page": chunk["page_number"]
        }
        for chunk in chunks
    ]

    vector_store = FAISS.from_texts(
        texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    return vector_store


def save_vector_store(
    vector_store,
    path="faiss_index"
):
    """
    Save FAISS vector database to disk.
    """

    vector_store.save_local(
        path
    )


def load_vector_store(
    embeddings,
    path="faiss_index"
):
    """
    Load an existing FAISS vector database.
    """

    if not os.path.exists(path):

        return None

    vector_store = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store