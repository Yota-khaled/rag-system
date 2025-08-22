import os
import re
import time
import shutil
import gc
import requests
from pypdf import PdfReader
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_TOKEN = os.getenv("OPENROUTER_API_KEY", "")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_TOKEN}",
    "Content-Type": "application/json"
}

# Read and extract text from a PDF file
def read_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    if not text.strip():
        raise ValueError("Failed to extract text from PDF.")
    return text

# Split text into smaller chunks
def split_text(text):
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    ).split_text(text)


# Create and persist a ChromaDB database from text chunks
def create_chromadb(chunks, persist_directory="db"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    db = Chroma.from_texts(
        chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    db.persist()
    return db


# Search ChromaDB for the most relevant chunks
def search_db(db, query, k=3):
    docs = db.similarity_search(query, k=k)
    unique_content = set(doc.page_content.strip() for doc in docs)
    return "\n".join(unique_content)


# Send a request to OpenRouter API
def query_openrouter(messages):
    payload = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.2
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise Exception(f"OpenRouter API Error {response.status_code}: {response.text}")
    return response.json()


# Generate an answer using OpenRouter API based on provided context and question
def generate_answer(context, question):
    messages = [
        {
            "role": "system",
            "content": "Answer the question based ONLY on the context provided. If you don't know, say 'I don't know'. Return the answer in English only."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}"
        }
    ]
    
    result = query_openrouter(messages)
    try:
        response = result["choices"][0]["message"]["content"]
    except:
        response = str(result)

    response = re.sub(r"<\|.*?\|>|<s>|</s>", "", response).strip()

    english_only = "\n".join(
        [line for line in response.split("\n") if re.search(r"[A-Za-z]", line)]
    ).strip()

    return english_only


# Close Chroma DB and safely delete the 'db' folder.
def close_and_delete_db():
    if "db" in st.session_state and st.session_state.db is not None:
        try:
            if hasattr(st.session_state.db, "persist"):
                st.session_state.db.persist()  
        except Exception as e:
            st.warning(f"Could not persist DB: {e}")
        
        try:
            del st.session_state.db
        except Exception:
            pass
        st.session_state.db = None

    gc.collect()
    time.sleep(1)  

    db_path = "db"
    if os.path.exists(db_path):
        for i in range(5):
            try:
                shutil.rmtree(db_path)
                break
            except PermissionError:
                time.sleep(0.5)
        else:
            st.warning(
                "Could not delete DB folder after 5 attempts. "
                "Make sure no program (including this app) is using it, "
                "then try again."
            )
