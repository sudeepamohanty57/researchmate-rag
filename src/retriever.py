from langchain_core.documents import Document


def retrieve_documents(
    vector_store,
    question,
    k=5
):

    documents = vector_store.similarity_search(
        question,
        k=k
    )

    return documents