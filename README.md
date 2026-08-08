# 📄 Resume-JD RAG Assistant

A **Retrieval-Augmented Generation (RAG)** application that analyzes a candidate's **Resume** and **Job Description (JD)**.

The application allows users to upload both documents and ask questions about:

* Candidate skills
* Projects
* Education
* Experience
* Job requirements
* Required qualifications
* Missing skills
* Resume-JD matching

The system retrieves relevant information from the uploaded documents and uses the **Groq LLM `llama-3.3-70b-versatile`** to generate context-grounded answers.

---

## 🎯 Project Objective

The objective of this project is to build a practical **RAG-based Resume-JD analysis system** that helps candidates understand how well their resume matches a particular job description.

Instead of directly providing the complete documents to the LLM, the application follows a retrieval pipeline:

1. Extracts text from PDF documents
2. Splits the extracted text into smaller chunks
3. Generates embeddings for the chunks
4. Stores the embeddings in a **FAISS vector store**
5. Routes the user's query to the **Resume, Job Description, or Both**
6. Retrieves the most relevant document chunks
7. Provides the retrieved context to the LLM
8. Generates a context-grounded response

---

# 🔄 Project Workflow

```text
                         User
                           │
                           ▼
                 ┌───────────────────┐
                 │    Streamlit UI   │
                 │                   │
                 │  Upload Resume    │
                 │  Upload JD        │
                 │  Ask Question     │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   PDF Processing  │
                 │      PyMuPDF      │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │      Chunking     │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │     Embeddings    │
                 │ SentenceTransformers
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   FAISS Vector    │
                 │       Store       │
                 └─────────┬─────────┘
                           │
                           ▼
                      User Query
                           │
                           ▼
                 ┌───────────────────┐
                 │    Query Router   │
                 └─────────┬─────────┘
                           │
                    ┌──────┼──────┐
                    ▼      ▼      ▼
                 Resume    JD     Both
                    │      │      │
                    └──────┼──────┘
                           ▼
                 ┌───────────────────┐
                 │ Relevant Context  │
                 │     Retrieval     │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌────────────────────────┐
                 │       Groq LLM         │
                 │ llama-3.3-70b-versatile│
                 └────────────┬───────────┘
                              │
                              ▼
                         Final Answer
```

---

# 🛠️ Technologies Used

| Technology                  | Purpose                         |
| --------------------------- | ------------------------------- |
| **Python**                  | Main programming language       |
| **Streamlit**               | Web application interface       |
| **LangChain**               | RAG and LLM integration         |
| **PyMuPDF**                 | PDF text extraction             |
| **Sentence Transformers**   | Text embedding generation       |
| **FAISS**                   | Vector similarity search        |
| **Groq**                    | LLM API                         |
| **Llama 3.3 70B Versatile** | Language model                  |
| **python-dotenv**           | Environment variable management |

### 🤖 LLM Model

```text
Provider: Groq
Model: llama-3.3-70b-versatile
```

---

# 📂 Project Structure

```text
resume-jd-rag/
│
├── app.py
├── chunking.py
├── document_processor.py
├── embeddings.py
├── query_router.py
├── rag_chain.py
├── retriever.py
├── vector_store.py
│
├── requirements.txt
├── .gitignore
├── README.md
│
└── sample_data/
    ├── resume.pdf
    └── job_description.pdf
```

---

# 🚀 How to Use

Follow the steps below to set up and run the **Resume-JD RAG Assistant** on your local machine.

## 1. Clone the Repository

```bash
git clone https://github.com/shubhamstat10/resume-jd-rag.git
cd resume-jd-rag


## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install all required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 4. Configure the Groq API Key

This project uses the **Groq API** with the following model:

```text
llama-3.3-70b-versatile
```

Create a `.env` file in the root directory of the project:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace:

```text
your_groq_api_key_here
```

with your actual Groq API key.

---

## 6. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

---

# 🧑‍💻 Using the Application

Once the application is running:

```text
Step 1  → Open the Streamlit application

Step 2  → Upload your Resume

Step 3  → Upload the Job Description

Step 4  → The application extracts text from the PDFs

Step 5  → The extracted text is divided into smaller chunks

Step 6  → Embeddings are generated for the chunks

Step 7  → Embeddings are stored in FAISS

Step 8  → Enter your question

Step 9  → The Query Router identifies the relevant source

Step 10 → Relevant document chunks are retrieved

Step 11 → Retrieved context is provided to the Groq LLM

Step 12 → `llama-3.3-70b-versatile` generates the final answer
```

---

# 💬 Example Questions

You can ask questions such as:

```text
What skills are missing from my resume for this job?

How well does my resume match this job description?

What are the most important skills required for this position?

Which skills should I add to my resume?

What are the key requirements mentioned in the job description?

Does my resume contain the required technical skills?

What experience gaps exist between my resume and this job?

How can I improve my resume for this job?

Give me a summary of the job description.

Which projects from my resume are most relevant to this job?
```

---

# 🧠 Example

### Question

```text
What skills should I improve to better match this job description?
```

### Example Answer

```text
Based on the job description, the important skills include:

1. Python
2. SQL
3. Machine Learning
4. Statistics
5. Data Visualization

Your resume already demonstrates Python, Statistics,
and Machine Learning.

However, SQL and Data Visualization could be
strengthened to improve your match with the job.
```

---

# 🔍 How the RAG System Works

The application follows a **Retrieval-Augmented Generation** approach.

```text
Resume + Job Description
          │
          ▼
     PDF Extraction
          │
          ▼
       Chunking
          │
          ▼
      Embeddings
          │
          ▼
    FAISS Vector Store
          │
          ▼
      User Question
          │
          ▼
     Query Routing
          │
          ▼
   Relevant Documents
          │
          ▼
    Similarity Search
          │
          ▼
   Relevant Context
          │
          ▼
      Groq LLM
          │
          ▼
llama-3.3-70b-versatile
          │
          ▼
      Final Answer
```

The system first retrieves relevant information from the uploaded Resume and Job Description.

The retrieved information is then passed as context to the **Groq `llama-3.3-70b-versatile` model**, which generates the final response.

This approach helps the application provide answers that are grounded in the user's uploaded documents.

---

# ⚠️ Limitations

* Answer quality depends on the quality and content of the uploaded documents.
* Poorly formatted or scanned PDFs may result in incomplete text extraction.
* The system cannot reliably answer questions about information that is not present in the uploaded documents.
* Very large documents may increase processing time.
* LLM-generated responses may occasionally contain incorrect interpretations.
* The current version primarily supports PDF documents.
* The application requires a valid Groq API key.
* Groq API usage may be subject to rate limits and usage restrictions.

---

# 🚀 Future Improvements

Possible future improvements include:

* Add support for DOCX and TXT files
* Add automatic ATS-style resume scoring
* Add Resume-JD similarity scoring
* Add skill-gap detection
* Add multiple resume comparison
* Add job recommendations based on resume similarity
* Add conversation memory
* Improve processing of scanned PDFs using OCR
* Add support for multiple LLM providers
* Add authentication
* Deploy the application to Streamlit Cloud or another cloud platform

Upload your **Resume** and **Job Description**, ask a question, and the application will retrieve relevant information using **FAISS** and generate a context-grounded response using the **Groq `llama-3.3-70b-versatile` model**.
