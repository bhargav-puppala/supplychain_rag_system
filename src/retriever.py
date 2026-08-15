from vector_store import get_collection
from embeddings import create_embedding


def search_documents(question, top_k=4):
    collection = get_collection()

    query_embedding = create_embedding(
        question,
        "RETRIEVAL_QUERY"
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    results = search_documents(question)

    print("\n==============================")
    print("RETRIEVED RESULTS")
    print("==============================")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1
    ):

        print(f"\nResult {i}")
        print("-" * 50)

        print(f"File: {metadata['file']}")
        print(f"Page: {metadata['page']}")
        print(f"Type: {metadata['document_type']}")
        print(f"Distance: {distance:.4f}")

        print("\nText:")
        print(document[:700])