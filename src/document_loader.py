from pypdf import PdfReader


def load_pdf(file):
    """
    Extract text from an uploaded PDF while preserving page numbers.
    """

    reader = PdfReader(file)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            pages.append({
                "page_number": page_number,
                "text": page_text
            })

    return pages