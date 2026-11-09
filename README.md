# Financial Document Management with Semantic Analysis

I built this project to explore how financial documents can be stored, organised and searched using semantic search instead of relying only on exact keyword matches.

The application provides a FastAPI backend for managing users and financial documents. It also uses a small RAG pipeline to split document text into chunks, generate embeddings and retrieve relevant content when a user submits a query.

## What it does

- **Document management:** Upload financial text files with details such as title, company name and document type. List, view and delete document records.
- **Semantic search:** Search indexed text by meaning rather than having to use the exact words from the document.
- **RAG-based retrieval:** Split text into smaller chunks, embed those chunks and retrieve the most relevant results for a query.
- **Basic role management:** Store user roles and expose endpoints for creating roles, assigning roles and checking the permissions associated with a role.

The roles currently represented in the code are Admin, Analyst, Auditor and Client.

## Tech stack

| Technology | Purpose |
| --- | --- |
| Python | Main development language |
| FastAPI | REST API |
| SQLAlchemy | Database models and database access |
| SQLite | Stores user and document records |
| Qdrant | Vector storage and similarity search |
| LangChain | Vector store integration and text splitting |
| Hugging Face Sentence Transformers | Text embeddings using `all-MiniLM-L6-v2` |
| Uvicorn | Runs the API server |

## How the project works

At a high level, the flow looks like this:

1. A document is uploaded through the API along with its basic details.
2. The application reads the uploaded text and creates a document record in SQLite.
3. The RAG engine splits the text into chunks (700 characters, with an overlap of 70 characters).
4. Each chunk is converted into an embedding and stored in the Qdrant collection.
5. When a search query arrives, the vector store finds similar chunks and the API returns the most relevant results.

The current search pipeline retrieves up to 20 candidates and returns the first 5.

## Project structure

```text
Financial-Document-Management-with-Semantic-Analysis/
│
├── main.py             # FastAPI routes and application entry point
├── rag_engine.py       # Text splitting, embeddings and semantic retrieval
├── database.py         # SQLite database setup and SQLAlchemy models
├── auth.py             # Role definitions and permission-check helper
├── models.py           # Reserved for additional models
├── requirements.txt    # Python dependencies
└── financial_app.db    # SQLite database (created by the application)
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Yashyc27/Financial-Document-Management-with-Semantic-Analysis.git
cd Financial-Document-Management-with-Semantic-Analysis
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
python main.py
```

The server starts at:

```text
http://127.0.0.1:8000
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The first run may take a little longer because the embedding model needs to be downloaded.

## Available API endpoints

These are the main routes currently defined in `main.py`.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Return the current placeholder login token |
| POST | `/roles/create` | Create a role response |
| POST | `/users/assign-role` | Assign a role to a user |
| GET | `/users/{id}/roles` | Get a user's role |
| GET | `/users/{id}/permissions` | Get the permission label for a user's role |
| POST | `/documents/upload` | Upload and index a document |
| GET | `/documents` | List document records |
| GET | `/documents/{document_id}` | Get a document record |
| DELETE | `/documents/{document_id}` | Delete a document record and its indexed chunks |
| POST | `/rag/index-document` | Index text directly |
| POST | `/rag/search` | Search indexed content |
| GET | `/rag/context/{document_id}` | Return the current placeholder context response |

## A quick semantic search example

Once some text has been indexed, send a POST request to `/rag/search`:

```json
{
  "query": "What financial risks could affect the company's ability to repay debt?"
}
```

The API returns matching text chunks along with their metadata.

You can also try the sample financial text in `test_upload.txt` as an example of the kind of content the project is intended to work with.

## Current limitations

This is a working project in development, and there are a few things worth knowing before using it beyond a local demo:

- The upload route currently reads the file as UTF-8 text. It does not yet extract text from PDF or scanned documents.
- Qdrant is configured with an in-memory client, so the vector collection is not persistent across application restarts.
- The login endpoint currently returns a placeholder token. Full JWT authentication is not wired into the API yet.
- Passwords are currently stored as plain text, so this implementation is not suitable for real user accounts.
- The role and permission endpoints demonstrate basic role handling, but permissions are not yet enforced across the document routes.
- The context endpoint currently returns placeholder content rather than retrieving document-specific context.

These are the main areas I would work on next: proper authentication, persistent vector storage, PDF text extraction and permission checks.

## What's next

Some improvements I have in mind:

- Add PDF and other financial document formats.
- Persist the Qdrant collection so indexed data survives restarts.
- Implement secure password hashing and real JWT-based authentication.
- Enforce role-based access on document operations and search.
- Add document-specific context retrieval and better filtering.
- Add tests for upload, deletion, indexing and search.

## Running it locally

This project is intended as a local development/demo application at this stage. Please avoid uploading confidential financial documents or real customer data until authentication, authorisation and storage security have been strengthened.

## Author

**Yash Chaudhary**

GitHub: [@Yashyc27](https://github.com/Yashyc27)

---

This project is a work in progress. Suggestions and feedback are welcome.
