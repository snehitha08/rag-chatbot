# 🧠 DocMind AI

An AI-powered assistant that lets you chat with PDFs and have general conversations using Google Gemini.

## Features
- 💬 **AI Chat** — Chat freely like ChatGPT
- 📄 **PDF Chat** — Upload any PDF and ask questions about it
- 🎨 **Beautiful UI** — Dark gradient design with smooth UX

## Tech Stack
- Python, Streamlit
- Google Gemini API
- Sentence Transformers (all-MiniLM-L6-v2)
- HNSWlib (vector search)
- PyPDF

## How to Run
```bash
git clone https://github.com/snehitha08/rag-chatbot.git
cd rag-chatbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## How it Works
1. PDF is split into chunks and converted to vector embeddings
2. User query is embedded and matched to relevant chunks using cosine similarity
3. Relevant chunks are passed to Gemini as context
4. Gemini generates an accurate answer based on the document

