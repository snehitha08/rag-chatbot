import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import hnswlib
import numpy as np
import google.generativeai as genai

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Global vector store
index = None
chunks = []

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    result = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        result.append(chunk)
    return result

def build_index(pdf_file):
    global index, chunks
    text = extract_text_from_pdf(pdf_file)
    chunks = split_text(text)
    embeddings = embedder.encode(chunks)
    dim = embeddings.shape[1]
    index = hnswlib.Index(space="cosine", dim=dim)
    index.init_index(max_elements=len(chunks), ef_construction=100, M=16)
    index.add_items(embeddings, list(range(len(chunks))))
    index.set_ef(50)
    return len(chunks)

def get_relevant_chunks(query, k=3):
    query_vec = embedder.encode([query])
    labels, _ = index.knn_query(query_vec, k=k)
    return [chunks[i] for i in labels[0]]

def ask_gemini(query, context_chunks):
    context = "\n\n".join(context_chunks)
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""Answer the question based on the context below.

Context:
{context}

Question: {query}

Answer clearly and concisely."""
    response = model.generate_content(prompt)
    return response.text

def chat_with_gemini(messages):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    history = []
    for msg in messages[:-1]:
        history.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [msg["content"]]
        })

    chat = model.start_chat(history=history)
    response = chat.send_message(messages[-1]["content"])
    return response.text