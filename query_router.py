import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def route_query(query):

    query_lower = query.lower().strip()

    # -----------------------------
    # BOTH: comparison questions
    # -----------------------------

    both_keywords = [
        "missing",
        "required skills not demonstrated",
        "required skills missing",
        "match",
        "matches",
        "satisfy",
        "satisfies",
        "compare",
        "comparison",
        "gap",
        "gaps",
        "suitable",
        "fit for this job",
        "qualified for this job",
        "requirements do i",
        "requirements does my resume",
        "which required skills are not demonstrated"
    ]

    if any(keyword in query_lower for keyword in both_keywords):
        return "both"

    # -----------------------------
    # RESUME: candidate information
    # -----------------------------

    resume_keywords = [
        "my skills",
        "my skill",
        "my project",
        "my projects",
        "project name",
        "projects on my resume",
        "my education",
        "my degree",
        "my experience",
        "my achievement",
        "my achievements",
        "my programming",
        "my libraries",
        "my courses",
        "my background",
        "what do i know",
        "what have i done"
    ]

    if any(keyword in query_lower for keyword in resume_keywords):
        return "resume"

    # -----------------------------
    # JD: job description information
    # -----------------------------

    jd_keywords = [
        "required skills",
        "required qualification",
        "required qualifications",
        "job requirements",
        "job responsibility",
        "job responsibilities",
        "preferred skills",
        "preferred qualification",
        "preferred qualifications",
        "what skills are required",
        "what qualifications are required",
        "what does the job require"
    ]

    if any(keyword in query_lower for keyword in jd_keywords):
        return "jd"

    # -----------------------------
    # LLM fallback
    # -----------------------------

    prompt = f"""
Classify the user's question into exactly ONE category:

resume
jd
both
out_of_scope

resume = The question asks only about the candidate's resume,
candidate skills, education, projects, experience, achievements,
or background.

jd = The question asks only about the job description,
job requirements, required skills, qualifications,
responsibilities, preferred skills, interview process,
selection process, or project requirements.

both = The question requires comparing or using BOTH
the resume and job description.
out_of_scope = The question is unrelated to the candidate's resume
or the job description.

User question:
{query}

Return ONLY one word:
resume
jd
both
"""

   
    response = llm.invoke(prompt)

    route = response.content.strip().lower()

    if route not in ["resume", "jd", "both","out_of_scope"]:
        route = "out_of_scope"

    return route