# 📘 Docu AI – AI-Powered Document Assistant

Docu AI is an AI-powered PDF question-answering application that allows users to upload PDF documents and ask questions about their content. It uses **Retrieval-Augmented Generation (RAG)** to provide relevant and context-based answers.

## ✨ Features
- Upload and process PDF documents.
- Ask questions based on document content.
- Retrieve relevant text using semantic search.
- Generate AI-powered answers.
- Interactive chat interface using Streamlit.

## 🛠️ Technologies Used
- Python
- Streamlit
- Google Gemini API
- FAISS
- Sentence Transformers
- PyPDF

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/AI-Document-Assistant.git
   ```

2. Navigate to the project folder:
   ```bash
   cd AI-Document-Assistant
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Gemini API key to `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-api-key"
   ```

5. Run the application:
   ```bash
   python -m streamlit run app.py
   ```

## 🚀 How to Use
1. Open the application in your browser.
2. Upload a PDF document.
3. Click **Process Document**.
4. Enter your questions in the chat box.
5. Get answers based on your document.

## 📁 Project Structure
```text
AI-Document-Assistant/
│
├── app.py
├── src/
│   ├── retriever.py
│   └── generator.py
├── data/
├── .streamlit/
│   └── secrets.toml
├── requirements.txt
└── README.md
```

## 🎯 Project Objective
To make document reading and information retrieval easier by using AI to understand PDF content and answer user questions efficiently.

## 👩‍💻 Author
**Ruth Glory Adapa**
