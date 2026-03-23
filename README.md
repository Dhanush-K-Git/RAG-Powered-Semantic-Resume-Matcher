# 🎯 RAG-Powered Semantic Resume Matcher

A high-performance Recruitment Intelligence tool that leverages **Retrieval-Augmented Generation (RAG)** to rank resumes with semantic precision. Unlike traditional ATS tools that rely on keyword matching, this system understands the *context* and *intent* of professional experience.

---

## 🚀 Core Features
- **Semantic Ranking:** Uses **S-BERT (all-MiniLM-L6-v2)** to calculate cosine similarity between Job Descriptions and candidate profiles.
- **Persistent Vector Vault:** Integrated **ChromaDB** to ensure resume embeddings are stored locally and remain consistent across sessions.
- **Automated Data Sync:** Real-time reconciliation logic that keeps the physical PDF storage in sync with the vector database.
- **100% Local AI:** Operates entirely on-device using Sentence-Transformers, ensuring data privacy and high-speed processing.

---

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence-Transformers (S-BERT)
- **Frontend:** Streamlit
- **Parsing:** PyPDF2

---

## 🏗️ System Architecture
The system follows a classic RAG (Retrieval-Augmented Generation) pipeline:
1. **Ingestion:** Extracts raw text from uploaded PDF resumes.
2. **Vectorization:** Converts text into high-dimensional embeddings.
3. **Storage:** Saves embeddings in a persistent ChromaDB collection.
4. **Retrieval:** When a JD is provided, the system queries the vector space to find the most mathematically similar profiles.

---

## 📦 Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/Dhanush-K-Git/RAG-Powered-Semantic-Resume-Matcher.git](https://github.com/Dhanush-K-Git/RAG-Powered-Semantic-Resume-Matcher.git)



2. Install dependencies: pip install -r requirements.txt
3. Run the application: streamlit run app.py
   
