
import os
import streamlit as st

from src.retriever import build_retriever, retrieve_documents
from src.generator import generate_answer


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Docu AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #173d7d;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #061a38;
        min-width: 430px;
        width: 430px;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1.5rem;
    }

    [data-testid="stSidebar"] * {
        color: white;
    }

    .brand-title {
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 0;
    }

    .brand-subtitle {
        font-size: 22px;
        color: #c8d8f2;
        margin-bottom: 35px;
    }

    .section-heading {
        font-size: 29px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        font-size: 23px;
    }

    [data-testid="stSidebar"] button {
        min-height: 55px;
        border-radius: 12px;
        font-size: 22px;
        font-weight: 650;
        background-color: white;
        color: #061a38 !important;
        border: none;
    }

    [data-testid="stSidebar"] button p {
        color: #061a38 !important;
    }

    .document-name {
        overflow-wrap: anywhere;
        font-size: 25px;
        font-weight: 650;
        color: white;
        padding: 12px;
        background-color: #102b51;
        border-radius: 10px;
        margin-top: 12px;
    }

    /* Main heading */
    .main-title {
        font-size: 56px;
        font-weight: 850;
        color: white;
        margin-bottom: 5px;
    }

    .main-subtitle {
        font-size: 28px;
        color: #dbe8ff;
        margin-bottom: 30px;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3 {
        color: #102b51 !important;
        font-size: 23px;
        line-height: 1.6;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: white !important;
        border: 2px solid #d5e3fa !important;
        border-radius: 15px !important;
        padding: 5px !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #102b51 !important;
        background: white !important;
        font-size: 22px !important;
        caret-color: #102b51 !important;
        opacity: 1 !important;
        cursor: text !important;
        user-select: text !important;
        -webkit-user-select: text !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #63748e !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] button {
        color: #173d7d !important;
        background-color: #e6efff !important;
        opacity: 1 !important;
    }

    /* Keep the chat input interactive */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] textarea {
        pointer-events: auto !important;
    }

    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            min-width: 0;
            width: auto;
        }

        .main-title {
            font-size: 38px;
        }

        .main-subtitle {
            font-size: 21px;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li {
            font-size: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- SESSION STATE ----------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown(
        '<div class="brand-title">Docu AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Your intelligent document assistant'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">📂 Upload Document</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        key="pdf_uploader",
    )

    if uploaded_file is not None:
        st.markdown(
            f'<div class="document-name">📄 {uploaded_file.name}</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Process Document",
            use_container_width=True,
            key="process_document",
        ):
            try:
                os.makedirs("data", exist_ok=True)

                file_path = os.path.join(
                    "data",
                    os.path.basename(uploaded_file.name),
                )

                with st.spinner("Processing your document..."):
                    with open(file_path, "wb") as file:
                        file.write(uploaded_file.getvalue())

                    index, chunks = build_retriever(file_path)

                    if index is None or chunks is None or len(chunks) == 0:
                        raise ValueError(
                            "No readable text was found in this PDF."
                        )

                    st.session_state.index = index
                    st.session_state.chunks = chunks
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.document_ready = True
                    st.session_state.chat_history = []

                st.success("Document processed successfully!")

            except Exception as error:
                st.session_state.document_ready = False
                st.session_state.index = None
                st.session_state.chunks = None
                st.error(f"Could not process the PDF: {error}")

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">💬 Conversation</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "＋ New Conversation",
        use_container_width=True,
    ):
        st.session_state.chat_history = []
        st.rerun()

    if st.button(
        "🗑 Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">📑 Document Status</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.document_ready:
        st.success("Document ready")
        st.write(f"**Current PDF:** {st.session_state.document_name}")
        st.write(f"**Text chunks:** {len(st.session_state.chunks)}")
    else:
        st.info("Upload and process a PDF to begin.")


# ---------------- MAIN AREA ----------------

st.markdown(
    '<div class="main-title">Ask Your Document</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">'
    'Upload a PDF and get answers from its content.'
    '</div>',
    unsafe_allow_html=True,
)


# ---------------- WELCOME MESSAGE ----------------

if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        st.markdown(
            """
            ### Welcome to Docu AI! 👋

            I can help you understand your documents.

            **To get started:**

            1. Upload a PDF using the sidebar.
            2. Click **Process Document**.
            3. Type your question in the white chat box below.
            4. Press Enter to receive an answer.

            Ask for summaries, explanations, key points, definitions,
            or other information from your document.
            """
        )


# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------
# Do not set disabled=True here.

question = st.chat_input(
    "Ask anything about your document...",
    key="document_question",
)


# ---------------- HANDLE QUESTION ----------------

if question:
    if not st.session_state.document_ready:
        st.warning(
            "Please upload a PDF and click Process Document first."
        )

    else:
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Preparing your answer..."):
                    context = retrieve_documents(
                        st.session_state.index,
                        question,
                        st.session_state.chunks,
                    )

                    answer = generate_answer(
                        question,
                        context,
                    )

                if not answer:
                    answer = (
                        "I couldn't generate an answer. "
                        "Please try asking another question."
                    )

                answer = str(answer)
                st.markdown(answer)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as error:
                error_message = (
                    "Sorry, I couldn't answer your question. "
                    f"Error details: {error}"
                )

                st.error(error_message)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )
