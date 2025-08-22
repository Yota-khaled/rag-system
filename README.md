# RAG PDF Q\&A System

This project is a **Retrieval-Augmented Generation (RAG)** system that allows users to upload PDFs and ask questions about their content. It retrieves relevant information from the document and uses an LLM (Mistral-7B Instruct via OpenRouter API) to generate context-aware answers.

## Features

* Upload PDF files for processing
* Extract text and split it into chunks for efficient searching
* Store chunks in a Chroma vector database
* Search the database for relevant content based on user queries
* Generate answers using OpenRouter's Mistral-7B Instruct model
* Handles unanswered queries politely

## Tech Stack

* Backend: Flask
* PDF Processing: PyPDF
* Text Splitting: LangChain RecursiveCharacterTextSplitter
* Embeddings: HuggingFace all-MiniLM-L6-v2
* Vector DB: Chroma
* LLM: OpenRouter (Mistral-7B Instruct)
* Frontend: Simple HTML interface, CSS, JS, and bot image

## Installation

1. Clone the repository:

```bash
git clone <https://github.com/Yota-khaled/rag-system>
cd <rag-system>
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your OpenRouter API key in a `.env` file:

```text
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

1. Run the Flask app:

```bash
flask run
```

2. Open your browser and navigate to `http://127.0.0.1:5000/`

3. Upload a PDF file and start asking questions about its content.

## Project Structure

```
.
├── app.py                 # Flask app
├── rag_functions.py       # Functions for PDF processing, embeddings, and LLM calls
├── templates/
│   └── index.html         # HTML frontend
├── static/
│   ├── script.js          # Frontend JavaScript
│   ├── style.css          # Frontend CSS
│   └── bot.png            # Bot image used in frontend
├── db/                    # Chroma vector database (auto-generated)
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Notes

* Make sure the `db` folder is not locked by any other process when deleting or recreating the Chroma database.
* The system currently returns answers in English only.

---


