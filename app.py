import streamlit as st

from rag_chain import ask_question
from vector_store import create_vector_store


st.set_page_config(
    page_title="Resume-JD Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume-JD Assistant")

st.markdown(
    "Analyze a resume against a job description using AI-powered RAG."
)

#sidebar
with st.sidebar:

    st.header("📂 Documents")

    st.caption("Upload your resume and the job description.")

    resume_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

    jd_file = st.file_uploader(
        "💼 Upload Job Description",
        type=["pdf"]
    )

    if resume_file and jd_file:
        st.success("✅ Both documents uploaded")
    elif resume_file:
        st.info("Resume uploaded. Please upload the JD.")
    elif jd_file:
        st.info("JD uploaded. Please upload the resume.")

        st.divider()

    st.subheader("💡 How to use")

    st.markdown("""
    1. Upload your **resume**
    2. Upload the **job description**
    3. Ask a question below

    **Example questions:**
    - What are my projects?
    - What skills do I have?
    - What skills are required?
    - Which requirements do I satisfy?
    """)

#________chat__________

if resume_file and jd_file:

    vector_store = create_vector_store(
        resume_file,
        jd_file
    )

    question = st.chat_input("Ask something...")

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_question(
                    question,
                    vector_store
                )

            st.write(answer)

else:

    st.info("Please upload both your resume and job description.")