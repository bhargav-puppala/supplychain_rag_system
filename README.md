# SupplyChain RAG System

A Retrieval-Augmented Generation (RAG) system designed for intelligent supply chain document analysis and question answering.

The system allows users to ask natural-language questions about supply chain performance and procurement policies. It retrieves relevant information from the uploaded PDF documents and uses Google's Gemini models to generate grounded answers with source document and page references.

---

## 📌 Project Overview

The **SupplyChain RAG System** is a document-based question-answering application developed as part of:

> **HCLTech × ET Masterclass – AI Skills for the Future**  
> **Assignment 2 – Supply Chain RAG System**

The system works with two primary Meridian Components Pvt. Ltd. documents:

1. `Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf`
2. `Meridian_Procurement_Policy_Handbook_v4.2.pdf`

The application combines information from both documents when answering cross-document questions.

---

## 🎯 Objective

The objective of this project is to build a RAG-based assistant that can:

- Process supply chain PDF documents
- Extract and preserve page-level information
- Split documents into manageable chunks
- Generate vector embeddings
- Store embeddings in a persistent vector database
- Retrieve relevant document sections
- Generate grounded answers using an LLM
- Answer questions requiring information from multiple documents
- Provide document and page-level sources
- Refuse to answer when the requested information is not available in the documents

---

## 🏗️ System Architecture

```text
                         PDF Documents
                              │
                              ▼
                       PDF Text Extraction
                              │
                              ▼
                     Document Chunking
                       1200 / 200
                              │
                              ▼
                    Gemini Embeddings
                   gemini-embedding-2
                              │
                              ▼
                         ChromaDB
                   Persistent Vector Store
                              │
                              ▼
                     Similarity Search
                              │
                              ▼
                    Relevant Context
                              │
                              ▼
                    Gemini 3.5 Flash
                              │
                              ▼
                       Grounded Answer
                              │
                              ▼
                 Source Document + Page
```

---

## 🔄 RAG Workflow

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Search ChromaDB
      │
      ▼
Retrieve Top Relevant Chunks
      │
      ▼
Build Context
      │
      ▼
Send Context + Question to Gemini
      │
      ▼
Generate Grounded Answer
      │
      ▼
Display Answer + Sources
```

---

## ✨ Features

- PDF document loading and text extraction
- Page-level document metadata
- 1200-character document chunking
- 200-character chunk overlap
- Gemini-based text embeddings
- 768-dimensional embeddings
- Persistent ChromaDB vector storage
- Similarity-based document retrieval
- Retrieval-Augmented Generation
- Cross-document question answering
- Source document and page references
- Streamlit web interface
- PDF upload and indexing
- Duplicate chunk detection during indexing
- Refusal for questions that cannot be answered from the provided documents

---

## 📂 Project Structure

```text
SupplyChain_RAG_System/
│
├── data/
│   ├── Meridian_Procurement_Policy_Handbook_v4.2.pdf
│   └── Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
│
├── src/
│   ├── check_models.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── pdf_loader.py
│   ├── rag.py
│   ├── retriever.py
│   └── vector_store.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| PDF Processing | pypdf |
| Embedding Model | Gemini `gemini-embedding-2` |
| Embedding Dimension | 768 |
| Vector Database | ChromaDB |
| Language Model | Gemini `gemini-3.5-flash` |
| Environment Variables | python-dotenv |
| Architecture | Retrieval-Augmented Generation |

---

## 📄 Source Documents

The system uses the following two primary documents:

### 1. Supply Chain Review

```text
Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
```

Contains information related to:

- Supplier performance
- Supplier spend
- On-time delivery
- Defect rates
- Line stoppages
- Lead times
- Inventory
- Supply chain performance

### 2. Procurement Policy Handbook

```text
Meridian_Procurement_Policy_Handbook_v4.2.pdf
```

Contains information related to:

- Supplier classification
- Supplier rating bands
- Procurement approval authorities
- Supplier escalation procedures
- Sourcing policies
- Safety-stock requirements
- Quality-related policies
- Supplier penalties and consequences

Both documents are indexed into the same ChromaDB collection to support cross-document questions.

---

## ✂️ Document Chunking

The documents are divided into overlapping chunks before generating embeddings.

### Configuration

```text
Chunk Size    : 1200 characters
Chunk Overlap : 200 characters
```

The overlap helps preserve context when relevant information is located near the boundary between two chunks.

---

## 🧠 Embeddings

The project uses Google's:

```text
gemini-embedding-2
```

The embedding output dimensionality is configured as:

```text
768
```

These embeddings are stored in ChromaDB and used for similarity-based retrieval.

---

## 🗄️ Vector Database

The project uses **ChromaDB** as its vector database.

The database is persisted locally so that indexed documents remain available after restarting the application.

The collection used by the project is:

```text
supply_chain_documents
```

Both Meridian PDFs are stored in the same collection.

Each stored chunk contains metadata including:

```text
file
page
document_type
```

This allows the application to identify the original document and page from which the retrieved information came.

---

## 🤖 Answer Generation

The project uses:

```text
gemini-3.5-flash
```

The model receives:

1. The user's question
2. Retrieved document context
3. Source metadata

The model is instructed to answer using only the retrieved document context.

It is instructed not to invent:

- Facts
- Numbers
- Policies
- Clauses
- Penalties
- Other unsupported information

If the required information cannot be found in the provided documents, the system returns:

```text
I don't have enough information in the provided documents to answer this question.
```

---

## 🔗 Cross-Document Question Answering

Some questions require information from both documents.

For example:

```text
Kaveri Metals recorded 88.1% on-time delivery and 1,150 defects per million in Q1.
Which policy clauses does this trigger, and what exactly must the buyer do?
```

The system retrieves:

```text
Supply Chain Review
        +
Procurement Policy Handbook
        │
        ▼
Relevant Context
        │
        ▼
Gemini
        │
        ▼
Combined Grounded Answer
```

This allows factual supplier performance information to be combined with the applicable procurement policy.

---

## 📚 Source References

The application displays the source document and page number associated with retrieved information.

Example:

```text
Source: Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
Page: 1
```

or:

```text
Source: Meridian_Procurement_Policy_Handbook_v4.2.pdf
Page: 2
```

Duplicate source/page combinations are displayed only once.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/bhargav-puppala/supplychain_rag_system.git
```

Move into the project directory:

```bash
cd supplychain_rag_system
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

The application uses the Gemini API.

Create a file named:

```text
.env
```

in the project root.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit the `.env` file to GitHub.

The project uses `python-dotenv` to load the API key from the environment.

---

## 🔒 Security

Sensitive API credentials are stored in `.env`.

The `.env` file is excluded from Git using `.gitignore`.

Recommended `.gitignore` entries:

```text
.env
venv/
.venv/
__pycache__/
chroma_db/
*.pyc
```

Never hard-code an API key directly inside the source code.

---

## 📥 Index Documents

Before asking questions for the first time, index the PDF documents.

Run:

```bash
python src/vector_store.py
```

The indexing process performs:

```text
PDF Extraction
      ↓
Chunk Creation
      ↓
Gemini Embedding Generation
      ↓
ChromaDB Storage
```

The terminal displays the indexing progress and the final number of chunks stored.

---

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The terminal will display a local URL, normally similar to:

```text
http://localhost:8501
```

Open the displayed URL in a browser.

---

# 🧪 Test Questions

The application is designed to answer the following mandatory questions.

## Question 1

```text
Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?
```

## Question 2

```text
How many line stoppages happened in Q1, what was the total downtime, and what caused them?
```

## Question 3

```text
What is the approval authority for a purchase order worth ₹1.4 crore?
```

## Question 4

```text
What are the four supplier classification categories, and what qualifies a supplier as Critical?
```

## Question 5 — Cross-Document

```text
Kaveri Metals recorded 88.1% on-time delivery and 1,150 defects per million in Q1.
Which policy clauses does this trigger, and what exactly must the buyer do?
```

## Question 6 — Cross-Document

```text
The microcontroller supplier is single-source.
What does the sourcing policy require in this situation,
and what is the company already doing about it?
```

## Question 7 — Cross-Document

```text
Microcontrollers are imported with a 46-day lead time.
Using the safety-stock policy, how many days of stock should be held for this part?
```

## Question 8 — Cross-Document

```text
Trident Circuit Boards had a defect rate of 640 parts per million.
What is the cost consequence under the policy?
```

## Question 9 — Cross-Document

```text
Which suppliers would fall below the B rating band on on-time delivery alone,
and what is the escalation path for them?
```

## Question 10 — Trap Question

```text
What is the annual salary of the Head of Procurement?
```

The system should not invent a salary if the information is not present in the uploaded documents.

Expected behavior:

```text
I don't have enough information in the provided documents to answer this question.
```

---

# 📊 Test Results

The following table should contain the actual results obtained from the application.

| # | Test Case | Status | Sources |
|---|---|---|---|
| 1 | Highest supplier spend | ⏳ To be validated | Review |
| 2 | Line stoppages | ⏳ To be validated | Review |
| 3 | Purchase order approval | ⏳ To be validated | Policy |
| 4 | Supplier classification | ⏳ To be validated | Policy |
| 5 | Kaveri cross-document question | ⏳ To be validated | Review + Policy |
| 6 | Single-source supplier | ⏳ To be validated | Review + Policy |
| 7 | Safety stock | ⏳ To be validated | Review + Policy |
| 8 | Trident defect consequence | ⏳ To be validated | Review + Policy |
| 9 | Supplier rating / escalation | ⏳ To be validated | Review + Policy |
| 10 | Salary trap question | ⏳ To be validated | N/A |

> Replace the `⏳ To be validated` values with the actual test results before final submission. Do not claim a test passed unless it has been manually verified.

---

# 🖼️ Screenshots

Add screenshots of the working application to demonstrate the system.

Recommended screenshots:

### Application Interface

```markdown
![Application Interface](screenshots/app-interface.png)
```

### Document Indexing

```markdown
![Document Indexing](screenshots/indexing.png)
```

### Cross-Document Question

```markdown
![Cross Document Question](screenshots/cross-document.png)
```

### Source References

```markdown
![Source References](screenshots/sources.png)
```

### Trap Question

```markdown
![Trap Question](screenshots/trap-question.png)
```

Replace the screenshot paths with the actual screenshot filenames before submission.

---

# 🧪 Retrieval Testing

The retrieval component can also be tested independently.

Run:

```bash
python src/retriever.py
```

Enter a question when prompted.

The retrieval output includes:

- Retrieved document
- Page number
- Document type
- Similarity distance
- Retrieved text

This can be used to inspect retrieval quality before evaluating the final generated answer.

---

# 📈 Persistence

ChromaDB is configured as a persistent vector database.

The database is stored locally in:

```text
chroma_db/
```

After documents have been indexed, the application can reuse the existing vector collection rather than recreating embeddings every time.

The application also checks existing chunk IDs to avoid unnecessarily re-indexing identical chunks.

---

# ⚠️ Limitations

- The system relies on the quality of the retrieved document chunks.
- Answers are limited to the information contained in the uploaded documents.
- Complex questions may require information from multiple retrieved chunks.
- PDF table extraction may not always preserve the original visual table structure perfectly.
- Response quality depends on the Gemini model and retrieved context.
- The application does not use external web information when answering document-based questions.

---

# 🔮 Future Improvements

Potential future improvements include:

- Improved table-aware PDF extraction
- More advanced retrieval strategies
- Metadata filtering
- Retrieval evaluation metrics
- Automated RAG evaluation
- Improved source highlighting
- Additional document collections
- REST API integration
- Cloud deployment

---

# 🎥 Demo

The project demonstration should cover:

1. Opening the Streamlit application
2. Showing the indexed document count
3. Asking a normal supply chain question
4. Asking cross-document questions
5. Showing the retrieved sources and page numbers
6. Demonstrating the trap question refusal

The demonstration focuses on the complete RAG workflow:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Context
   ↓
Gemini
   ↓
Grounded Answer
   ↓
Sources
```

---

# 📌 Assignment Information

**Program:** HCLTech × ET Masterclass – AI Skills for the Future

**Project:** Assignment 2 – Supply Chain RAG System

**Domain:** Supply Chain / Procurement

**Architecture:** Retrieval-Augmented Generation (RAG)

---

# 👨‍💻 Author

**Bhargav Puppala**

GitHub:  
https://github.com/bhargav-puppala

Repository:  
https://github.com/bhargav-puppala/supplychain_rag_system

---

# 📄 License

This project was developed for educational and project-submission purposes.