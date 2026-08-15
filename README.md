# SupplyChain RAG System

A Retrieval-Augmented Generation (RAG) system designed for intelligent supply chain document analysis and question answering.

## Overview

The SupplyChain RAG System allows users to interact with supply chain-related documents using natural language. The system processes PDF documents, divides them into smaller chunks, creates embeddings, stores them in a vector database, retrieves relevant information, and generates context-aware answers.

## Features

* PDF document loading and processing
* Text extraction from documents
* Document chunking
* Text embedding generation
* Vector-based document retrieval
* Retrieval-Augmented Generation (RAG)
* Natural language question answering
* Supply chain document analysis

## Project Structure

```text
SupplyChain_RAG_System/
│
├── data/
│   ├── Supply Chain Documents
│   └── Reference Documents
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
├── .gitignore
└── README.md
```

## RAG Workflow

```text
PDF Documents
      ↓
Text Extraction
      ↓
Document Chunking
      ↓
Embedding Generation
      ↓
Vector Store
      ↓
Relevant Document Retrieval
      ↓
Context + User Query
      ↓
Generated Answer
```

## Technologies Used

* Python
* Retrieval-Augmented Generation (RAG)
* Natural Language Processing
* Text Embeddings
* Vector Database
* PDF Processing

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/hasiniconnect01/SupplyChain_RAG_System.git
cd SupplyChain_RAG_System
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

Install the required Python packages used by the project.

### 4. Configure the API key

Create a `.env` file in the project directory and add your API key.

**Do not upload the `.env` file to GitHub.**

The `.gitignore` file is configured to keep sensitive information such as API keys private.

### 5. Run the application

```bash
python app.py
```

## Security

API keys and environment variables are kept outside the GitHub repository using `.env`. The `.env` file is included in `.gitignore` to prevent accidental exposure of sensitive credentials.

## Purpose

This project was developed as **Assignment 2 – Supply Chain RAG System**, demonstrating the application of Retrieval-Augmented Generation for document-based supply chain information retrieval and question answering.
