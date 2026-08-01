from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(pages):
    """
    Split PDF pages into smaller chunks while preserving page numbers.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for page in pages:

        page_chunks = splitter.split_text(
            page["text"]
        )

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "page_number": page["page_number"]
            })

    return chunks