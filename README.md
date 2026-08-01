# 📚 ResearchMate – AI-Powered Research Paper Assistant

ResearchMate is an AI-powered research paper assistant that allows users to upload research papers in PDF format and ask questions about their content.

The application uses a **Retrieval-Augmented Generation (RAG)** pipeline to extract, process, index, retrieve, and answer questions from uploaded research documents using a local LLM.

---

## 🚀 Project Overview

Research papers can be long and difficult to analyze manually. ResearchMate simplifies this process by allowing users to upload a research paper and interact with it using natural language questions.

The system follows this workflow:

```text
📄 Upload Research Paper
        ↓
📖 Extract PDF Text
        ↓
✂️ Split Text into Chunks
        ↓
🧠 Generate Embeddings
        ↓
🗄️ Store in FAISS Vector Database
        ↓
🔎 Retrieve Relevant Chunks
        ↓
🤖 Generate AI Answer
```

---

## ✨ Features

- 📄 Upload research papers in PDF format
- 📖 Extract text page-by-page
- ✂️ Split documents into searchable chunks
- 🧠 Generate semantic embeddings
- 🗄️ Store embeddings using FAISS
- 🔎 Retrieve relevant document sections
- 🤖 Generate answers using a local LLM
- 💬 Ask follow-up questions
- 📝 Generate structured research paper summaries
- 📚 Display source pages for answers
- 💾 Save and reload document indexes
- 📥 Download chat history
- 🗑️ Clear chat history

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web interface |
| pypdf | PDF text extraction |
| LangChain | Document processing |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Ollama | Local LLM inference |
| Llama 3.2:1b | Answer generation |
| Git & GitHub | Version control |

---

## 📁 Project Structure

```text
researchmate-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── src/
    ├── document_loader.py
    ├── text_splitter.py
    ├── embeddings.py
    ├── vector_store.py
    ├── retriever.py
    ├── generator.py
    └── qa_chain.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sudeepamohanty57/researchmate-rag.git
cd researchmate-rag
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Ollama Setup

ResearchMate uses Ollama to run the language model locally.

Download the required model:

```bash
ollama pull llama3.2:1b
```

Check that the model is available:

```bash
ollama list
```

You should see:

```text
llama3.2:1b
```

---

## ▶️ Run the Application

Activate the virtual environment and run:

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 💬 Example Usage

### 1. Upload a Research Paper

Upload a PDF research paper using the document uploader.

### 2. Ask Questions

Example questions:

```text
What is the main objective of this research?
```

```text
What methodology was used?
```

```text
What dataset was used in the study?
```

```text
What were the main results?
```

### 3. Ask Follow-up Questions

ResearchMate supports conversational follow-up questions.

For example:

```text
What is the proposed model?
```

followed by:

```text
What are its main advantages?
```

The application rewrites follow-up questions into standalone questions before retrieving relevant document sections.

---

## 📝 Research Paper Summary

ResearchMate can generate a structured summary of an uploaded research paper.

The summary covers:

1. Research Objective
2. Proposed Methodology
3. Dataset and Experimental Setup
4. Main Results
5. Key Findings
6. Limitations
7. Conclusion

---

## 🔎 RAG Architecture

The application follows a Retrieval-Augmented Generation architecture:

```text
                 Research Paper PDF
                         │
                         ▼
                 PDF Text Extraction
                         │
                         ▼
                  Text Chunking
                         │
                         ▼
              Sentence Embeddings
                         │
                         ▼
                 FAISS Vector Store
                         │
                         │
User Question ───────────┘
      │
      ▼
Question Rewriting
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Document Chunks
      │
      ▼
Context Construction
      │
      ▼
   Ollama / Llama 3.2
      │
      ▼
ResearchMate Answer
```

---

## 🧠 How the RAG Pipeline Works

### Step 1 – PDF Extraction

The uploaded PDF is processed and its text is extracted page-by-page.

### Step 2 – Text Splitting

The extracted text is divided into smaller chunks so that relevant sections can be retrieved efficiently.

### Step 3 – Embeddings

Each text chunk is converted into a numerical vector representation using a sentence-transformer embedding model.

### Step 4 – FAISS Indexing

The embeddings are stored in a FAISS vector database for efficient similarity search.

### Step 5 – Retrieval

When the user asks a question, ResearchMate searches the vector database and retrieves the most relevant document chunks.

### Step 6 – Answer Generation

The retrieved document sections are provided as context to the local Llama 3.2 model through Ollama.

The model generates an answer based on the retrieved research-paper content.

---

## 📚 Source References

ResearchMate displays the page numbers of the retrieved document sections used to answer a question.

This helps users identify the relevant parts of the original research paper.

---

## 💾 Document Indexing

ResearchMate saves the FAISS vector index locally.

When the same research paper is uploaded again, the existing index can be loaded instead of rebuilding the complete vector database.

This reduces unnecessary processing time.

---

## ⚠️ Limitations

- PDF extraction quality depends on the structure of the document.
- Complex tables, figures, and mathematical notation may not be extracted perfectly.
- Answer quality depends on the retrieved document chunks.
- The lightweight `llama3.2:1b` model may provide less detailed answers than larger language models.
- The application currently focuses on one uploaded research paper at a time.
- The system is intended as a research-assistance tool and should not replace expert interpretation.

---

## 🔮 Future Improvements

- Support multiple research papers simultaneously
- Hybrid keyword and semantic retrieval
- Document reranking
- Improved citation generation
- Figure and table understanding
- Larger local language models
- Better hallucination detection
- Research-paper comparison
- Conversation persistence
- Cloud deployment
- Improved document visualization

---

## 🔐 Privacy

ResearchMate uses a local language model through Ollama for answer generation.

The research paper content is processed locally by the application rather than requiring an external hosted LLM API for generation.

---

## 🎯 Project Objective

The objective of ResearchMate is to provide an accessible AI-assisted interface for exploring research papers through natural-language interaction while maintaining a retrieval-based connection to the source document.

---

## 👨‍💻 Author

**Sudeepa Mohanty**

B.Tech – Computer Science and Engineering (Data Science)

Siksha 'O' Anusandhan (Deemed to be University)

---

## 📜 License

This project is intended for educational and research purposes.
