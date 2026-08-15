from pathlib import Path
from pypdf import PdfReader


DATA_FOLDER = Path(__file__).parent.parent / "data"


def extract_pdfs(pdf_files=None):
    documents = []

    if pdf_files is None:
        pdf_files = list(DATA_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return documents

    for pdf_path in pdf_files:

        pdf_path = Path(pdf_path)

        reader = PdfReader(str(pdf_path))

        print(f"\nDocument: {pdf_path.name}")
        print(f"Pages: {len(reader.pages)}")

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text() or ""

            documents.append({
                "text": text,
                "file": pdf_path.name,
                "page": page_number
            })

            print(
                f"  Page {page_number}: "
                f"{len(text)} characters"
            )

    return documents


if __name__ == "__main__":

    documents = extract_pdfs()

    print("\n--------------------------------")
    print(
        f"Total pages extracted: "
        f"{len(documents)}"
    )
    print("--------------------------------")

    if documents:

        print("\nFirst page preview:")
        print(
            documents[0]["text"][:500]
        )