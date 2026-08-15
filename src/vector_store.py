from pathlib import Path
import time

import chromadb

from pdf_loader import extract_pdfs
from chunker import create_chunks
from embeddings import create_embedding


# ============================================================
# CHROMA DATABASE
# ============================================================

CHROMA_PATH = (
    Path(__file__).parent.parent / "chroma_db"
)

COLLECTION_NAME = "supply_chain_documents"


# ============================================================
# GET CHROMA COLLECTION
# ============================================================

def get_collection():

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


# ============================================================
# CREATE UNIQUE CHUNK ID
# ============================================================

def create_chunk_id(chunk, index):

    return (
        f"{chunk['file']}_"
        f"page_{chunk['page']}_"
        f"chunk_{index}"
    )


# ============================================================
# INDEX DOCUMENTS
# ============================================================

def index_documents(pdf_paths=None):

    print("\n==============================")
    print("STARTING DOCUMENT INDEXING")
    print("==============================")

    # If specific PDFs are supplied,
    # process only those PDFs.
    #
    # If nothing is supplied,
    # process all PDFs in the data folder.
    documents = extract_pdfs(pdf_paths)

    if not documents:

        print("No documents found.")

        return 0


    # ========================================================
    # CREATE CHUNKS
    # ========================================================

    chunks = create_chunks(documents)

    print(
        f"\nTotal chunks created: {len(chunks)}"
    )


    # ========================================================
    # GET CHROMA COLLECTION
    # ========================================================

    collection = get_collection()


    # ========================================================
    # GET EXISTING IDS
    # ========================================================

    existing_data = collection.get()

    existing_ids = set(
        existing_data["ids"]
    )


    # ========================================================
    # PREPARE NEW DATA
    # ========================================================

    ids = []
    texts = []
    embeddings = []
    metadatas = []


    # ========================================================
    # CREATE EMBEDDINGS
    # ========================================================

    for index, chunk in enumerate(chunks):

        chunk_id = create_chunk_id(
            chunk,
            index
        )


        # ----------------------------------------------------
        # SKIP ALREADY INDEXED CHUNKS
        # ----------------------------------------------------

        if chunk_id in existing_ids:

            print(
                f"Skipping existing chunk: "
                f"{chunk_id}"
            )

            continue


        print(
            f"Creating embedding "
            f"{index + 1}/{len(chunks)}..."
        )


        # ----------------------------------------------------
        # RETRY EMBEDDING IF CONNECTION FAILS
        # ----------------------------------------------------

        embedding = None

        for attempt in range(3):

            try:

                embedding = create_embedding(
                    chunk["text"],
                    "RETRIEVAL_DOCUMENT"
                )

                break

            except Exception as e:

                print(
                    f"Embedding failed "
                    f"(attempt {attempt + 1}/3):"
                )

                print(e)

                if attempt < 2:

                    print(
                        "Waiting 5 seconds "
                        "before retry..."
                    )

                    time.sleep(5)

                else:

                    raise


        # ----------------------------------------------------
        # STORE DATA
        # ----------------------------------------------------

        ids.append(
            chunk_id
        )

        texts.append(
            chunk["text"]
        )

        embeddings.append(
            embedding
        )

        metadatas.append({

            "file": chunk["file"],

            "page": chunk["page"],

            "document_type": chunk[
                "document_type"
            ]

        })


    # ========================================================
    # ADD TO CHROMADB
    # ========================================================

    if ids:

        collection.upsert(

            ids=ids,

            documents=texts,

            embeddings=embeddings,

            metadatas=metadatas
        )


    # ========================================================
    # FINAL INFORMATION
    # ========================================================

    print("\n==============================")
    print("INDEXING COMPLETE")
    print("==============================")

    print(
        f"New chunks added: {len(ids)}"
    )

    print(
        f"Total chunks in ChromaDB: "
        f"{collection.count()}"
    )

    return len(ids)


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    index_documents()