import pymupdf


def extract_text_from_pdf(pdf_path):

    doc = pymupdf.open(stream = pdf_path.getvalue(), filetype="pdf")

    all_text = []

    for page in doc:

        text = page.get_text()

        if text.strip():
            all_text.append(text)

    doc.close()

    # Combine all pages into one continuous document
    full_text = "\n".join(all_text)

    return full_text