import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Common resume and job-description section names

SECTION_NAMES = [
    "education",
    "academic qualifications",
    "academic background",
    "educational background",

    "experience",
    "work experience",
    "professional experience",
    "internship",
    "internships",

    "skills",
    "technical skills",
    "key skills",
    "technical expertise",

    "projects",
    "key projects",
    "academic projects",
    "personal projects",

    "certifications",
    "certificates",

    "achievements",
    "scholastic achievements",
    "awards",
    "honors",

    "courses",
    "relevant courses",
    "coursework",

    "publications",
    "research",
    "research experience",

    "extracurricular activities",
    "extra curricular activities",
    "activities",

    "summary",
    "professional summary",
    "profile",
    "objective",

    "responsibilities",
    "job responsibilities",

    "requirements",
    "qualifications",
    "required qualifications",
    "required skills",
    "preferred qualifications",
    "preferred skills",

    "about the role",
    "about the job",

    "project experience",
    "what we are looking for",

    "interests",
    "references"
]


def normalize_heading(text):
    """Normalize text for heading comparison."""

    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def is_section_heading(line):
    """Check whether a line is likely to be a section heading."""

    normalized = normalize_heading(line)

    # Known section
    if normalized in SECTION_NAMES:
        return True

    # Uppercase multi-word heading
    # Avoid treating things like SQL, R, NLP as headings
    if line.isupper() and 2 <= len(line.split()) <= 6:
        return True

    return False


def split_document_into_sections(text):
    """
    Split the complete document into logical sections.

    The entire PDF is treated as one continuous document,
    so sections can continue naturally across PDF pages.
    """

    sections = []

    current_section = "General"
    current_text = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if is_section_heading(line):

            # Save previous section
            if current_text:

                sections.append({
                    "section": current_section,
                    "text": "\n".join(current_text)
                })

            # Start new section
            current_section = line
            current_text = []

        else:

            current_text.append(line)

    # Save final section
    if current_text:

        sections.append({
            "section": current_section,
            "text": "\n".join(current_text)
        })

    return sections


def create_chunks(text, document_type):

    sections = split_document_into_sections(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for section in sections:

        section_chunks = splitter.split_text(
            section["text"]
        )

        for chunk in section_chunks:

            chunks.append({
                "text": chunk,
                "metadata": {
                    "document_type": document_type,
                    "section": section["section"]
                }
            })

    return chunks