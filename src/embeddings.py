import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "gemini-embedding-2"


def create_embedding(text, task_type):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768
        )
    )

    return result.embeddings[0].values


if __name__ == "__main__":
    test_text = "Kaveri Metals recorded 1150 defects per million."

    embedding = create_embedding(
        test_text,
        "RETRIEVAL_DOCUMENT"
    )

    print("Embedding created successfully!")
    print("Embedding dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])