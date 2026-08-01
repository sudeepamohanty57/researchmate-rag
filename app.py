import streamlit as st
import os
import json

from src.generator import (
    create_generator,
    generate_answer,
    rewrite_question,
    generate_full_summary
)

from src.document_loader import load_pdf
from src.text_splitter import split_text
from src.embeddings import create_embeddings

from src.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store
)

from src.retriever import retrieve_documents


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="ResearchMate",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =================================================
# CUSTOM CSS
# =================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-top: 0px;
        margin-bottom: 25px;
    }

    .source-box {
        padding: 10px;
        border-radius: 8px;
        background-color: rgba(128, 128, 128, 0.1);
        margin-bottom: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =================================================
# HEADER
# =================================================

st.markdown(
    '<div class="main-title">📚 ResearchMate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered research paper assistant'
    '</div>',
    unsafe_allow_html=True
)


# =================================================
# FAISS CONFIGURATION
# =================================================

FAISS_PATH = "faiss_index"

FAISS_METADATA_PATH = os.path.join(
    FAISS_PATH,
    "metadata.json"
)


# =================================================
# SESSION STATE
# =================================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "pages" not in st.session_state:
    st.session_state.pages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []


# =================================================
# SIDEBAR
# =================================================

with st.sidebar:

    st.header("📚 ResearchMate")

    st.markdown(
        "Your AI assistant for understanding "
        "research papers."
    )

    st.divider()

    st.subheader("📄 Document")

    uploaded_file = st.file_uploader(
        "Upload a research paper",
        type=["pdf"]
    )

    st.divider()

    if st.session_state.file_name:

        st.markdown("### 📖 Current Paper")

        st.write(
            st.session_state.file_name
        )

        st.divider()

        st.markdown(
            "### 📊 Document Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Pages",
                len(
                    st.session_state.pages
                )
            )

        with col2:

            st.metric(
                "Chunks",
                len(
                    st.session_state.chunks
                )
            )


    # =================================================
    # CHAT ACTIONS
    # =================================================

    if st.session_state.chat_history:

        st.divider()

        st.subheader(
            "💬 Chat Actions"
        )

        chat_text = ""

        for chat in (
            st.session_state.chat_history
        ):

            if chat["role"] == "user":

                chat_text += (
                    "USER:\n"
                    + chat["content"]
                    + "\n\n"
                )

            else:

                chat_text += (
                    "RESEARCHMATE:\n"
                    + chat["content"]
                    + "\n\n"
                )


        # ---------------------------------------------
        # Download Chat
        # ---------------------------------------------

        st.download_button(
            label="📥 Download Chat",
            data=chat_text,
            file_name="researchmate_chat.txt",
            mime="text/plain",
            use_container_width=True
        )


        # ---------------------------------------------
        # Clear Chat
        # ---------------------------------------------

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.rerun()


# =================================================
# PDF PROCESSING
# =================================================

if uploaded_file is not None:

    # -------------------------------------------------
    # Check if New PDF
    # -------------------------------------------------

    if (
        st.session_state.file_name
        != uploaded_file.name
    ):

        # Reset previous document

        st.session_state.chat_history = []

        st.session_state.vector_store = None

        st.session_state.pages = []

        st.session_state.chunks = []

        st.session_state.file_name = (
            uploaded_file.name
        )


        # -------------------------------------------------
        # Check Existing FAISS
        # -------------------------------------------------

        faiss_exists = (
            os.path.exists(
                FAISS_PATH
            )
            and os.path.exists(
                os.path.join(
                    FAISS_PATH,
                    "index.faiss"
                )
            )
            and os.path.exists(
                os.path.join(
                    FAISS_PATH,
                    "index.pkl"
                )
            )
            and os.path.exists(
                FAISS_METADATA_PATH
            )
        )


        existing_file_name = None


        if faiss_exists:

            try:

                with open(
                    FAISS_METADATA_PATH,
                    "r",
                    encoding="utf-8"
                ) as f:

                    metadata = json.load(f)

                    existing_file_name = (
                        metadata.get(
                            "file_name"
                        )
                    )

            except Exception:

                existing_file_name = None


        # -------------------------------------------------
        # Load Existing FAISS
        # -------------------------------------------------

        if (
            faiss_exists
            and existing_file_name
            == uploaded_file.name
        ):

            try:

                with st.spinner(
                    "⚡ Loading saved document index..."
                ):

                    embeddings = (
                        create_embeddings()
                    )

                    vector_store = (
                        load_vector_store(
                            embeddings,
                            FAISS_PATH
                        )
                    )


                if vector_store is not None:

                    st.session_state.vector_store = (
                        vector_store
                    )


                    with st.spinner(
                        "📖 Loading document..."
                    ):

                        pages = load_pdf(
                            uploaded_file
                        )


                    if pages:

                        st.session_state.pages = (
                            pages
                        )

                        chunks = split_text(
                            pages
                        )

                        st.session_state.chunks = (
                            chunks
                        )


                        st.success(
                            "⚡ Saved document index loaded!"
                        )

            except Exception as e:

                st.warning(
                    "⚠️ Could not load the saved "
                    "document index. A new index "
                    "will be created."
                )

                st.session_state.vector_store = None


        # -------------------------------------------------
        # Create New FAISS Index
        # -------------------------------------------------

        if (
            st.session_state.vector_store
            is None
        ):

            try:

                # -----------------------------------------
                # Extract PDF
                # -----------------------------------------

                with st.spinner(
                    "📖 Extracting text from PDF..."
                ):

                    pages = load_pdf(
                        uploaded_file
                    )


                if not pages:

                    st.error(
                        "❌ Could not extract text "
                        "from this PDF."
                    )

                    st.stop()


                st.session_state.pages = (
                    pages
                )


                st.success(
                    f"✅ Extracted "
                    f"{len(pages)} pages"
                )


                # -----------------------------------------
                # Split Text
                # -----------------------------------------

                with st.spinner(
                    "✂️ Splitting document..."
                ):

                    chunks = split_text(
                        pages
                    )


                if not chunks:

                    st.error(
                        "❌ No text chunks were "
                        "created from the PDF."
                    )

                    st.stop()


                st.session_state.chunks = (
                    chunks
                )


                st.success(
                    f"✅ Created "
                    f"{len(chunks)} chunks"
                )


                # -----------------------------------------
                # Create Embeddings
                # -----------------------------------------

                with st.spinner(
                    "🧠 Creating embeddings..."
                ):

                    embeddings = (
                        create_embeddings()
                    )


                # -----------------------------------------
                # Create FAISS
                # -----------------------------------------

                with st.spinner(
                    "🗄️ Building FAISS index..."
                ):

                    vector_store = (
                        create_vector_store(
                            chunks,
                            embeddings
                        )
                    )


                if vector_store is None:

                    st.error(
                        "❌ Failed to create "
                        "the FAISS vector store."
                    )

                    st.stop()


                # -----------------------------------------
                # Save FAISS
                # -----------------------------------------

                with st.spinner(
                    "💾 Saving document index..."
                ):

                    save_vector_store(
                        vector_store,
                        FAISS_PATH
                    )


                # -----------------------------------------
                # Save Metadata
                # -----------------------------------------

                os.makedirs(
                    FAISS_PATH,
                    exist_ok=True
                )


                with open(
                    FAISS_METADATA_PATH,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        {
                            "file_name":
                                uploaded_file.name
                        },
                        f,
                        indent=4
                    )


                st.session_state.vector_store = (
                    vector_store
                )


                st.success(
                    "✅ Document indexed successfully!"
                )


            except Exception as e:

                st.error(
                    "❌ An error occurred while "
                    "processing the PDF."
                )

                st.exception(e)

                st.stop()


# =================================================
# MAIN APPLICATION
# =================================================

if (
    st.session_state.vector_store
    is not None
):

    vector_store = (
        st.session_state.vector_store
    )


    # =================================================
    # DOCUMENT STATUS
    # =================================================

    st.info(
        f"📖 Currently reading: "
        f"**{st.session_state.file_name}**"
    )


    # =================================================
    # DOCUMENT CONTENT
    # =================================================

    with st.expander(
        "📖 View Extracted Text"
    ):

        for page in (
            st.session_state.pages
        ):

            st.markdown(
                f"### 📄 Page "
                f"{page['page_number']}"
            )

            st.write(
                page["text"]
            )

            st.divider()


    # =================================================
    # TEXT CHUNKS
    # =================================================

    with st.expander(
        "🧩 View Text Chunks"
    ):

        for i, chunk in enumerate(
            st.session_state.chunks
        ):

            st.markdown(
                f"**Chunk {i + 1}** "
                f"— 📄 Page "
                f"{chunk['page_number']}"
            )

            st.write(
                chunk["text"]
            )

            st.divider()


    # =================================================
    # RESEARCH PAPER SUMMARY
    # =================================================

    st.divider()

    st.subheader(
        "📝 Research Paper Summary"
    )

    st.caption(
        "Generate a structured summary of the "
        "uploaded research paper."
    )


    if st.button(
        "📝 Summarize This Research Paper",
        use_container_width=True
    ):

        try:

            generator = (
                create_generator()
            )

            with st.spinner(
                "🧠 Reading and summarizing "
                "the research paper..."
            ):

                summary = generate_full_summary(
                    generator,
                    st.session_state.chunks
                )


            st.subheader(
                "📄 Research Paper Summary"
            )

            st.write(
                summary
            )

        except Exception as e:

            st.error(
                "❌ Could not generate the "
                "research paper summary."
            )

            st.exception(e)


    # =================================================
    # CHAT
    # =================================================

    st.divider()

    st.subheader(
        "💬 Ask Your Research Paper"
    )

    st.caption(
        "Ask questions about the uploaded paper "
        "and ResearchMate will find relevant "
        "information and answer using the document."
    )


    # =================================================
    # DISPLAY CHAT HISTORY
    # =================================================

    for chat in (
        st.session_state.chat_history
    ):

        with st.chat_message(
            chat["role"]
        ):

            st.write(
                chat["content"]
            )


    # =================================================
    # CHAT INPUT
    # =================================================

    question = st.chat_input(
        "Ask a question about your research paper..."
    )


    # =================================================
    # PROCESS QUESTION
    # =================================================

    if question:

        # ---------------------------------------------
        # User Message
        # ---------------------------------------------

        with st.chat_message(
            "user"
        ):

            st.write(
                question
            )


        try:

            # ---------------------------------------------
            # Generator
            # ---------------------------------------------

            generator = (
                create_generator()
            )


            # ---------------------------------------------
            # Save User Message
            # ---------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            # ---------------------------------------------
            # Rewrite Question
            # ---------------------------------------------

            with st.spinner(
                "🧠 Understanding your question..."
            ):

                standalone_question = (
                    rewrite_question(
                        generator,
                        question,
                        st.session_state
                        .chat_history[:-1]
                    )
                )


            # ---------------------------------------------
            # Retrieve Documents
            # ---------------------------------------------

            with st.spinner(
                "🔍 Searching the research paper..."
            ):

                results = retrieve_documents(
                    vector_store,
                    standalone_question,
                    k=5
                )


            # ---------------------------------------------
            # Generate Answer
            # ---------------------------------------------

            with st.spinner(
                "🤖 ResearchMate is thinking..."
            ):

                answer = generate_answer(
                    generator,
                    standalone_question,
                    results
                )


            # ---------------------------------------------
            # Display Answer
            # ---------------------------------------------

            with st.chat_message(
                "assistant"
            ):

                st.write(
                    answer
                )


            # ---------------------------------------------
            # Save Answer
            # ---------------------------------------------

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


            # =================================================
            # SOURCES
            # =================================================

            if results:

                st.subheader(
                    "📚 Sources"
                )


                pages_found = []


                for document in results:

                    page_number = (
                        document.metadata.get(
                            "page",
                            "Unknown"
                        )
                    )


                    if (
                        page_number
                        not in pages_found
                    ):

                        pages_found.append(
                            page_number
                        )


                for page_number in sorted(
                    pages_found,
                    key=lambda x: (
                        isinstance(x, str),
                        x
                    )
                ):

                    st.markdown(
                        f'<div class="source-box">'
                        f"📄 Page <b>{page_number}</b>"
                        f"</div>",
                        unsafe_allow_html=True
                    )


                # =================================================
                # RELEVANT SECTIONS
                # =================================================

                with st.expander(
                    "📖 View Relevant Sections"
                ):

                    for i, document in enumerate(
                        results
                    ):

                        page_number = (
                            document.metadata.get(
                                "page",
                                "Unknown"
                            )
                        )


                        st.markdown(
                            f"### Section {i + 1} "
                            f"— 📄 Page {page_number}"
                        )


                        st.write(
                            document.page_content
                        )


                        st.divider()


            else:

                st.warning(
                    "No relevant sections found."
                )


        except Exception as e:

            st.error(
                "❌ Something went wrong while "
                "processing your question."
            )

            st.exception(e)
