# Multimodal RAG API

This repository is a Python-based Retrieval-Augmented Generation (RAG) backend focused on building a working text-first multimodal retrieval pipeline. The current implementation is structured around loading documents, splitting them into chunks, generating embeddings, storing them in Pinecone, and retrieving the most relevant content for a query.

## What is implemented

The project currently includes the following core pieces:

- FastAPI application setup with health and logs endpoints
- environment-based configuration for app settings
- document loading from local files
- recursive text chunking for indexed content
- embedding generation using Hugging Face sentence-transformers
- Pinecone vector storage and semantic search
- ingestion workflow that hashes documents and stores chunk metadata

## Project structure

- `app/main.py` — FastAPI application entry point
- `app/core/config.py` — environment and app configuration
- `app/core/logging_config.py` — logging setup
- `app/ingestion/loader.py` — file text loading utilities
- `app/ingestion/chunker.py` — recursive chunk splitting logic
- `app/embeddings/text_embeddings.py` — embedding generation service
- `app/vectorstore/pinecone.py` — Pinecone index integration and vector search
- `app/services/ingestionservice.py` — main ingestion pipeline
- `app/api/routes/health.py` — health check endpoint
- `app/api/routes/logs.py` — basic logging endpoint

## Current ingestion flow

The current working flow is:

1. Read a text file from disk
2. Validate that the file contains content
3. Create a document ID and content hash
4. Split the text into chunks using `RecursiveCharacterTextSplitter`
5. Generate embeddings for each chunk
6. Upsert the vectors into Pinecone with metadata such as source, document ID, and chunk index
7. Return summary counts about the ingestion process

This is a solid foundation for later extending the pipeline to richer multimodal content such as images or non-text documents.

## Tech stack

- Python
- FastAPI
- LangChain
- Hugging Face embeddings
- Pinecone
- Pydantic settings

## Environment setup

Create a `.env` file in the project root with the required configuration values, for example:

```env
APP_NAME=Multimodal RAG API
ENVIRONMENT=development
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=multimodal-rag-dense
DATABASE_URL=your_postgres_connection_string
DATABASE_URL_POOLED=your_pooled_postgres_connection_string
```

The application reads these values from the environment through the settings object in `app/core/config.py`.

## Running the app

From the project folder:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then the API will be available locally on the default FastAPI port.

## Health check

The app currently exposes a health endpoint:

- `GET /health`

This returns the service status and current environment.

## Current status

This project is in the early-to-mid development stage: the foundation for a document-based RAG pipeline is in place and the code is organized around modular services. The project is positioned for expansion into more advanced retrieval and multimodal capabilities while keeping a clean backend structure.

## Future direction

Planned extensions include:

- more retrieval and reranking layers
- support for image and multimodal embeddings
- stronger API endpoints for query and ingestion workflows
- database-backed metadata management
- improved evaluation and search quality tuning

## Summary

The repository already contains a usable text-based RAG foundation: loading, chunking, embedding, vector storage, and retrieval logic are all represented in the current code. The system is ready for the next stage of development, where it can evolve from a document-search backend into a broader multimodal knowledge system.
