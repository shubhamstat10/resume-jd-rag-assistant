import os

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from retriever import retrieve


# -----------------------------
# LLM
# -----------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# -----------------------------
# Prompt
# 

prompt = ChatPromptTemplate.from_template(
"""
You are a Resume and Job Description assistant.

Use ONLY the provided context.
Do not invent information.

The retrieval route is:

{route}

Follow these rules:

IF route = resume:
Answer the user's question ONLY using the resume.
Do NOT compare with the job description.
Do NOT use "Required Qualifications".
Do NOT use "Preferred Qualifications".
Do NOT create a match analysis.

IF route = jd:
Answer the user's question ONLY using the job description.
Do NOT use resume information.
Do NOT compare with the candidate.

IF route = both:
Use BOTH the resume and job description.
This route is for questions such as:
- What skills am I missing?
- Which requirements do I satisfy?
- How well does my resume match this job?

For comparison questions, clearly explain the evidence
from the resume and the requirement from the job description.

Important:
Only consider a skill demonstrated if it is explicitly stated
or clearly evidenced in the provided resume context.

Do NOT infer, assume, or imply any skill, experience, or qualification.

A skill is demonstrated ONLY when the provided resume context
explicitly states it or clearly provides direct evidence of it.

Do NOT use phrases such as:
"implied", "suggests", "likely", "probably", or
"partially demonstrated" unless the resume context explicitly
provides evidence for that partial demonstration.

For example:
- Python does NOT prove Pandas or NumPy.
- A project description does NOT prove communication or
  technical explanation ability unless this is explicitly stated.
- A project name alone does NOT prove that a specific technology
  was used.

If there is no explicit evidence, say:
"Not demonstrated in the provided context."

If a required skill is not explicitly demonstrated in the resume
context, say:
"Not demonstrated in the provided context."

Do not guess or make assumptions.

Context:
{context}

User Question:
{question}

Answer:
"""
)

def create_context(results):

    context = ""

    for result in results:

        document_type = result.metadata.get(
            "document_type",
            "unknown"
        )

        section = result.metadata.get(
            "section",
            "unknown"
        )

        context += f"""
Document: {document_type}
Section: {section}

{result.page_content}

-------------------------
"""

    return context


def ask_question(question,vector_store):

    results, route = retrieve(question,vector_store)

    if route == "out_of_scope":
        return "I can only answer question related to the resume and the job description."

    context = create_context(results)

    messages = prompt.format_messages(
    context=context,
    question=question,
    route=route

    )

    response = llm.invoke(messages)

    return response.content