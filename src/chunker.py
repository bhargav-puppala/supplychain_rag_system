from pdf_loader import extract_pdfs


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def create_chunks(documents):
    chunks = []

    for document in documents:
        text = document["text"]
        file_name = document["file"]
        page = document["page"]

        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "text": chunk_text,
                    "file": file_name,
                    "page": page,
                    "document_type": (
                        "policy"
                        if "Policy" in file_name
                        else "review"
                    )
                })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


if __name__ == "__main__":
    documents = extract_pdfs()
    chunks = create_chunks(documents)

    print("\n==============================")
    print(f"Total chunks created: {len(chunks)}")
    print("==============================")

    for i, chunk in enumerate(chunks[:3], start=1):
        print(f"\nChunk {i}")
        print(f"File: {chunk['file']}")
        print(f"Page: {chunk['page']}")
        print(f"Type: {chunk['document_type']}")
        print(f"Characters: {len(chunk['text'])}")
        print("-" * 40)
        print(chunk["text"][:300])