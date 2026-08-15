import sys
from pathlib import Path

import streamlit as st


# ============================================================
# FIND THE SRC FOLDER
# ============================================================

SRC_FOLDER = Path(__file__).parent / "src"
sys.path.append(str(SRC_FOLDER))


# Import RAG functions
from rag import generate_answer
from vector_store import get_collection, index_documents


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supply Chain RAG Assistant",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# MAIN TITLE
# ============================================================

st.title("📦 Supply Chain RAG Assistant")

st.write(
    "Ask questions about the Supply Chain Performance Review and Procurement Policy Handbook."
    
    "Also Upload Documents and ask questions about them."
)


# ============================================================
# SIDEBAR - SYSTEM INFORMATION
# ============================================================

st.sidebar.header("System Information")

try:

    collection = get_collection()

    st.sidebar.metric(
        "Indexed Chunks",
        collection.count()
    )

except Exception:

    st.sidebar.warning(
        "ChromaDB is not available yet."
    )


# ============================================================
# DOCUMENTS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📚 Documents")

st.sidebar.write(
    "📄 Supply Chain Performance Review"
)

st.sidebar.write(
    "📄 Procurement Policy Handbook"
)


# ============================================================
# UPLOAD NEW DOCUMENTS
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📤 Add a Document")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


# ============================================================
# INDEX NEW DOCUMENTS
# ============================================================

if uploaded_files:

    st.sidebar.write(
        f"**{len(uploaded_files)} PDF(s) selected**"
    )

    if st.sidebar.button(
        "🔄 Index Documents",
        type="primary"
    ):

        data_folder = (
            Path(__file__).parent / "data"
        )

        data_folder.mkdir(
            exist_ok=True
        )

        # Keep track of ONLY the newly uploaded PDFs
        uploaded_paths = []

        # Save uploaded files
        for uploaded_file in uploaded_files:

            file_path = (
                data_folder / uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            uploaded_paths.append(
                file_path
            )


        # Index only newly uploaded PDFs
        with st.spinner(
            "Extracting text, creating chunks, "
            "generating embeddings and indexing..."
        ):

            try:

                new_chunks = index_documents(
                    uploaded_paths
                )

                st.sidebar.success(
                    f"✅ Indexing complete! "
                    f"{new_chunks} new chunks added."
                )

                st.rerun()

            except Exception as e:

                st.sidebar.error(
                    f"❌ Indexing failed: {e}"
                )


# ============================================================
# QUESTION SECTION
# ============================================================

st.subheader("🔎 Ask a Question")

question = st.text_area(
    "Enter your question:",
    placeholder=(
        "Example: Kaveri Metals recorded 1150 PPM defects. "
        "Which clause does this trigger and what does it cost?"
    ),
    height=120
)


ask_button = st.button(
    "🔍 Ask Question",
    type="primary"
)


# ============================================================
# GENERATE ANSWER
# ============================================================

if ask_button:

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                answer, sources = generate_answer(
                    question,
                    top_k=6
                )


                # ====================================================
                # ANSWER
                # ====================================================

                st.subheader("💬 Answer")

                st.markdown(answer)


                # ====================================================
                # SOURCES
                # ====================================================

                st.subheader("📚 Sources")

                seen = set()

                for source in sources:

                    key = (
                        source["file"],
                        source["page"]
                    )

                    if key not in seen:

                        st.write(
                            f"📄 **{source['file']}** "
                            f"— Page {source['page']}"
                        )

                        seen.add(key)


            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Supply Chain RAG Assistant • "
    "Gemini + ChromaDB + Streamlit"
)