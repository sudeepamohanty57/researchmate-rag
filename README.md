# 📚 ResearchMate – AI-Powered Research Paper Assistant

ResearchMate is an AI-powered research paper assistant that allows users to upload research papers in PDF format and ask questions about their content.

The application uses a **Retrieval-Augmented Generation (RAG)** pipeline to extract, process, index, and retrieve relevant information from uploaded research documents before generating answers using a language model.

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
