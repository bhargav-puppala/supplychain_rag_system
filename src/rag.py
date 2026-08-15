import os
from dotenv import load_dotenv
from google import genai

from retriever import search_documents


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash"


def generate_answer(question, top_k=4):

    results = search_documents(question, top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):
        context_parts.append(
            f"""
SOURCE {i}
File: {metadata['file']}
Page: {metadata['page']}
Document Type: {metadata['document_type']}

Content:
{document}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are a supply chain procurement assistant.

Answer the user's question ONLY using the provided
document context.

Do not use outside knowledge.
Do not invent facts, numbers, clauses, penalties,
or policies.

If the answer cannot be found in the provided context,
say:

"I don't have enough information in the provided
documents to answer this question."

For questions requiring information from both documents,
combine the relevant facts carefully.

For cross-document answers, clearly explain:
1. The factual information from the Supply Chain Review.
2. The relevant rule or clause from the Policy Handbook.
3. The resulting action or consequence.

Always provide the source document name and page number.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text, metadatas


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    answer, sources = generate_answer(question)

    print("\n==============================")
    print("ANSWER")
    print("==============================")

    print(answer)

    print("\n==============================")
    print("SOURCES")
    print("==============================")

    seen = set()

    for source in sources:

        key = (
            source["file"],
            source["page"]
        )

        if key not in seen:

            print(
                f"- {source['file']} — Page {source['page']}"
            )

            seen.add(key)