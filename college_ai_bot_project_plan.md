# College AI Bot — Final Project Plan

## 1. Project Overview

### Goal
Build an AI-powered college information assistant that answers questions about the college in natural language.

Examples:

- “Where is the library?”
- “Who is the HOD of the EC department?”
- “What are the college timings?”
- “What are the library rules?”

The project will be developed in **two versions** so that V1 establishes a simple baseline and V2 demonstrates a meaningful upgrade using **RAG (Retrieval-Augmented Generation)**.

### Important scope decision
Users **do not upload documents**.

The college/project team prepares the knowledge base beforehand. In V2, the documents are processed during setup and stored in a searchable vector database. Users only ask questions through the frontend.

---

# 2. Overall Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- HTTP client for the chosen LLM API

## Frontend

- React
- Vite
- Basic CSS/Tailwind if desired

## V1 knowledge source

- JSON file containing structured college information

## V2 knowledge source

- College-provided documents prepared beforehand
- PDF/text extraction
- Text chunking
- Embeddings
- Vector database such as Chroma or FAISS

## LLM

Use any suitable LLM API available to the team.

The exact provider is not important to the architecture. The important concept is:

> **knowledge → relevant context → LLM → natural-language answer**

---

# 3. System Progression

The main idea of the project is to show the evolution from a simple LLM application to a retrieval-augmented application.

## V1

```text
React Frontend
      ↓
FastAPI Backend
      ↓
College JSON Data
      ↓
Prompt + Question + College Data
      ↓
LLM API
      ↓
Natural-language Answer
      ↓
React Frontend
```

## V2

```text
          COLLEGE KNOWLEDGE (prepared beforehand)
                         ↓
                 Documents / PDFs
                         ↓
               Text extraction
                         ↓
                     Chunking
                         ↓
                    Embeddings
                         ↓
                  Vector Database

USER QUESTION
      ↓
React Frontend
      ↓
FastAPI Backend
      ↓
Question Embedding
      ↓
Semantic Retrieval
      ↓
Top relevant chunks
      ↓
Prompt + Retrieved Context + Question
      ↓
LLM API
      ↓
Answer + Source information
      ↓
React Frontend
```

---

# 4. Version 1 — Basic LLM + JSON

## 4.1 What V1 is

V1 is a simple **LLM-powered college information bot**.

The college information is stored in a JSON file. For every user question, the backend sends the relevant college data along with a system prompt and the user's question to the LLM.

The LLM converts the information into a natural-language answer.

## 4.2 Purpose of V1

V1 demonstrates the basic AI application pipeline:

1. Receive a question.
2. Load college information.
3. Construct a controlled prompt.
4. Call the LLM API.
5. Return the generated answer to the frontend.

V1 should remain intentionally simple. Do **not** add the main RAG features here; those are the important improvements reserved for V2.

---

# 5. V1 Knowledge Structure

A simple structure is enough.

Example:

```json
{
  "college": {
    "name": "Example College",
    "timings": "9:00 AM to 4:00 PM",
    "address": "Main Campus"
  },
  "library": {
    "location": "Block C, Ground Floor",
    "timings": "9:00 AM to 6:00 PM"
  },
  "departments": {
    "EC": {
      "name": "Electronics and Communication Engineering",
      "hod": "Dr. Example",
      "location": "Block A, Second Floor"
    },
    "CS": {
      "name": "Computer Science and Engineering",
      "hod": "Dr. Example",
      "location": "Block B, First Floor"
    }
  }
}
```

The actual project should replace this with the college's real information.

## Suggested categories

Keep the first dataset limited to useful information such as:

- College timings
- Departments
- HODs
- Department locations
- Library location and timings
- Office locations
- Important contact information
- Basic campus facilities

---

# 6. V1 Backend Design

Suggested FastAPI structure:

```text
college-ai-bot/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── data/
│   │   └── college.json
│   │
│   ├── routes/
│   │   └── chat.py
│   │
│   └── services/
│       └── llm.py
│
└── frontend/
    ├── package.json
    ├── index.html
    ├── public/
    │
    └── src/
        ├── main.jsx
        ├── App.jsx
        │
        ├── components/
        │   ├── Chat.jsx
        │   ├── Message.jsx
        │   └── ChatInput.jsx
        │
        └── services/
            └── api.js
```

Notes:

- Keep API keys in `backend/.env` (not committed).
- Run the API with `uvicorn main:app --reload` from inside `backend/`.

This is only a suggested structure; the project can be kept even simpler if time is tight.

## Main API

Use one basic endpoint:

```text
POST /api/chat
```

Request:

```json
{
  "question": "Where is the library?"
}
```

Response:

```json
{
  "answer": "The library is located in Block C on the ground floor."
}
```

---

# 7. V1 Request Flow

### Step 1 — Frontend

User types a question into a chat box.

### Step 2 — React → FastAPI

React sends:

```text
POST /api/chat
```

with the user's question.

### Step 3 — Backend loads knowledge

FastAPI reads `college.json`.

### Step 4 — Prompt construction

Create a prompt containing:

- System instructions
- College information
- User question

Example concept:

```text
SYSTEM:
You are a college information assistant.
Answer using only the provided college information.
If the information is not available, say that you do not know.

COLLEGE INFORMATION:
{college_json}

USER QUESTION:
{question}
```

### Step 5 — LLM API call

Backend sends the prompt to the selected LLM API.

### Step 6 — Return answer

FastAPI returns the LLM's answer to React.

### Step 7 — Display

React displays the answer in the chat interface.

---

# 8. V1 Important Implementation Details

## Environment variables

Keep API credentials in `.env`.

Example:

```text
LLM_API_KEY=...
```

Never hard-code API keys in the source code.

## Basic validation

Validate that:

- The question is not empty.
- The request has the expected JSON structure.

## Basic error handling

Handle:

- LLM API failure
- Invalid requests
- Empty responses
- Timeouts

## Hallucination control

The system prompt should explicitly tell the LLM to use only the supplied information and say that it does not know when information is missing.

This is an important part of the project because the bot is supposed to answer **college-specific factual questions**, not general questions from the model's own knowledge.

---

# 9. V1 Frontend

Keep the frontend simple.

## Main UI

```text
+--------------------------------------+
|        College AI Assistant          |
+--------------------------------------+
|                                      |
| User: Where is the library?          |
|                                      |
| Bot: The library is in Block C...    |
|                                      |
+--------------------------------------+
| [ Ask your question...       ] [Send]|
+--------------------------------------+
```

Required frontend features:

- Chat input
- Send button
- Message history
- Loading state
- Error message

Do not spend much time on visual design in V1.

---

# 10. Version 2 — RAG

## 10.1 What RAG means

**RAG = Retrieval-Augmented Generation**.

Instead of giving the LLM the entire college knowledge base for every question, the system first searches the college knowledge base for information relevant to the question.

Only the relevant retrieved information is then given to the LLM.

The basic idea is:

```text
Question
   ↓
Retrieve relevant knowledge
   ↓
Give retrieved knowledge to LLM
   ↓
Generate answer
```

This separates two jobs:

- **Retriever:** find useful information.
- **LLM:** understand the information and produce the answer.

---

# 11. V2 Knowledge Base

The knowledge base should be prepared by the project team before the application is used.

Users never upload documents.

Example source files:

```text
knowledge/
├── college_information.pdf
├── departments.pdf
├── library_information.pdf
├── academic_rules.pdf
└── hostel_information.pdf
```

The exact files depend on what information the college provides.

For a 4-day project, a small number of good documents is better than trying to collect everything.

---

# 12. How RAG Works in This Project

## Stage A — Prepare the knowledge base

This happens before users ask questions.

### 1. Read documents

Extract text from PDFs or other supported documents.

### 2. Split the text into chunks

Large documents are divided into smaller pieces.

Example:

```text
Document
  ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
```

The chunks should be small enough to retrieve meaningful sections but large enough to retain context.

### 3. Create embeddings

Each chunk is converted into an embedding vector.

Conceptually:

```text
"Library is located in Block C..."
             ↓
      [0.21, -0.48, 0.77, ...]
```

The embedding represents the semantic meaning of the text.

### 4. Store vectors

Store:

- Chunk text
- Embedding vector
- Metadata such as filename/page/category

inside the vector database.

---

# 13. V2 Runtime Flow

When a user asks a question:

### Step 1 — User question

Example:

```text
What are the rules for library membership?
```

### Step 2 — Convert question to embedding

The question is converted into an embedding using the same embedding approach used for the stored chunks.

### Step 3 — Search vector database

Find the chunks that are most semantically similar to the question.

For example:

```text
Top result 1 → library_membership section
Top result 2 → library rules section
Top result 3 → student ID section
```

### Step 4 — Build LLM prompt

Send the LLM:

- System instruction
- Retrieved chunks
- User question

Conceptually:

```text
SYSTEM:
You are a college information assistant.
Answer using only the supplied context.
If the context does not contain the answer, say you do not know.

RETRIEVED CONTEXT:
{relevant_chunks}

USER QUESTION:
{question}
```

### Step 5 — LLM generates answer

The model turns the retrieved information into a natural-language response.

### Step 6 — Return answer and source metadata

V2 can return both:

```json
{
  "answer": "Library membership is available to enrolled students...",
  "sources": [
    {
      "document": "library_information.pdf",
      "page": 3
    }
  ]
}
```

This source display is a useful V2 feature for the final presentation.

---

# 14. V2 Suggested Architecture

```text
                   PREPARATION PHASE

 College PDFs / Documents
            ↓
      Text Extraction
            ↓
          Chunking
            ↓
        Embeddings
            ↓
      Vector Database

================================================

                    USER PHASE

User Question
      ↓
React Frontend
      ↓
FastAPI /api/chat
      ↓
Question Embedding
      ↓
Vector Search
      ↓
Top-K Relevant Chunks
      ↓
Prompt Construction
      ↓
LLM API
      ↓
Answer + Sources
      ↓
React Frontend
```

---

# 15. V2 Backend Structure

A reasonable evolution of the V1 backend is:

```text
backend/
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── chat.py
│   ├── services/
│   │   ├── llm.py
│   │   ├── retrieval.py
│   │   └── embeddings.py
│   ├── schemas/
│   │   └── chat.py
│   └── rag/
│       ├── ingest.py
│       ├── chunking.py
│       └── vector_store.py
├── knowledge/
│   ├── college_information.pdf
│   ├── departments.pdf
│   └── library_information.pdf
├── .env
└── requirements.txt
```

The ingestion scripts can be run separately when preparing/updating the knowledge base.

---

# 16. V2 Implementation Choice

For a 4-day college project, avoid building a complicated RAG platform.

Use the simplest implementation that clearly demonstrates the concept.

A practical stack is:

```text
FastAPI
PyPDF / PDF text extraction library
Embedding API or local embedding model
Chroma or FAISS
LLM API
React
```

### Recommended approach

Implement the retrieval logic explicitly enough that the team understands it:

```text
load documents
→ extract text
→ split text
→ create embeddings
→ store vectors
→ embed question
→ similarity search
→ pass top chunks to LLM
```

A framework such as LangChain or LlamaIndex can be added only if it saves time. It should not become something the team cannot explain during the presentation.

---

# 17. What to Reserve for V2

To keep the final presentation meaningful, avoid putting these into V1:

- RAG
- Embeddings
- Vector database
- PDF/document ingestion
- Semantic search
- Source citations
- Top-K retrieval
- Retrieval debugging information

V1 should intentionally look like the simpler first generation of the system.

---

# 18. V1 vs V2 Comparison

| Feature | V1 | V2 |
|---|---|---|
| Frontend | React | React |
| Backend | FastAPI | FastAPI |
| LLM | Yes | Yes |
| Knowledge source | JSON | College documents |
| Full knowledge sent to LLM | Yes | No |
| Retrieval | No | Yes |
| Embeddings | No | Yes |
| Vector database | No | Yes |
| Semantic search | No | Yes |
| Source metadata | Optional/No | Yes |
| User document upload | No | No |
| Main purpose | Baseline | Intelligent document-based retrieval |

---

# 19. Four-Day Implementation Plan

## Day 1 — V1 Backend + LLM

### Goal
Get a complete working backend-to-LLM pipeline.

### Tasks

1. Create Python environment.
2. Create FastAPI project.
3. Create `college.json`.
4. Create Pydantic request/response models.
5. Create `/api/chat` endpoint.
6. Implement LLM API service.
7. Build the system prompt.
8. Send JSON data + question to LLM.
9. Return the answer as JSON.
10. Test with curl/Postman/browser API docs.

### End-of-day target

```text
POST /api/chat
      ↓
LLM
      ↓
correct college answer
```

---

## Day 2 — V1 Frontend + V2 Ingestion

### V1 frontend

1. Create React/Vite app.
2. Create chat interface.
3. Connect to FastAPI.
4. Show user and bot messages.
5. Add loading/error states.

### V2 ingestion

1. Gather a small set of college documents.
2. Extract text.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings + metadata in the vector database.

### End-of-day target

V1 works end-to-end and the V2 vector database has usable data.

---

## Day 3 — V2 Retrieval + LLM

### Tasks

1. Receive user question.
2. Generate question embedding.
3. Search vector database.
4. Retrieve top-K chunks.
5. Build RAG prompt.
6. Call LLM.
7. Return answer.
8. Return document/page metadata.
9. Connect V2 to the frontend.
10. Test questions whose answers appear in different documents.

### End-of-day target

```text
Question
 ↓
Retriever
 ↓
Relevant chunks
 ↓
LLM
 ↓
Answer + source
```

---

## Day 4 — Testing + Presentation

### Testing

Test three categories:

#### 1. Direct questions

```text
Who is the EC HOD?
Where is the library?
```

#### 2. Questions requiring document retrieval

```text
What are the library membership rules?
What is the attendance requirement?
```

#### 3. Questions with no answer in the knowledge base

```text
What is tomorrow's weather?
Who is the Prime Minister?
```

The bot should avoid pretending that unavailable information exists.

### Presentation preparation

Prepare one simple architecture diagram for each version.

Show the same question being answered through V1 and V2 and explain the difference in how information reaches the LLM.

---

# 20. Final Demo Flow

A strong final demonstration can follow this sequence.

## Demo 1 — V1

Ask:

> Where is the library?

Explain:

> The backend sends the predefined college JSON along with the question to the LLM.

## Demo 2 — V2

Ask a question based on a document:

> What are the rules for library membership?

Show:

```text
Question
 ↓
Relevant chunks retrieved
 ↓
LLM
 ↓
Answer
```

Then show the source document/page.

## Demo 3 — Unknown information

Ask something outside the knowledge base.

Show that the bot responds that the information is unavailable instead of inventing an answer.

This demonstrates an important property of a college information assistant: **grounding responses in the college's knowledge base**.

---

# 21. Suggested Presentation Structure

## Slide 1 — Problem

Students often need quick answers about locations, departments, timings, rules, and college facilities.

## Slide 2 — Proposed Solution

An AI chatbot that answers college-specific questions in natural language.

## Slide 3 — V1 Architecture

```text
Frontend → FastAPI → JSON + LLM → Answer
```

## Slide 4 — Limitations of V1

The entire knowledge base is provided to the model for each query.

This becomes less practical as the amount of information grows.

## Slide 5 — V2: RAG

Introduce Retrieval-Augmented Generation.

```text
Question → Retrieve relevant knowledge → LLM → Answer
```

## Slide 6 — V2 Architecture

Show document ingestion, embeddings, vector database, retrieval, and LLM generation.

## Slide 7 — Live Demo

Ask questions in the frontend.

## Slide 8 — V1 vs V2

Show how the information flow changes.

## Slide 9 — Result

The system can answer college-specific questions using prepared institutional knowledge.

---

# 22. What Not to Build in These Four Days

Do not spend time on:

- User login/authentication
- Admin panel
- User document uploads
- Multi-college support
- Complex agent systems
- Voice input/output
- Fine-tuning the LLM
- Training your own model
- Complicated frontend animations
- Large-scale deployment architecture

These are outside the useful scope of the assignment.

---

# 23. Minimum Viable Deliverables

## V1 must have

- React chat UI
- FastAPI backend
- College JSON knowledge base
- LLM API integration
- System prompt
- Basic error handling
- Working question → answer flow

## V2 must have

- Prepared college documents
- Document text extraction
- Chunking
- Embeddings
- Vector database
- Semantic retrieval
- LLM generation using retrieved context
- Source/document metadata in the response
- Working React UI

---

# 24. Core Concepts the Team Should Be Able to Explain

By the final presentation, every team member should understand these concepts at a basic level:

### V1

- REST API
- FastAPI endpoint
- JSON
- Prompt
- System prompt
- LLM API
- Request/response flow
- Hallucination

### V2

- RAG
- Embeddings
- Vector similarity search
- Chunking
- Vector database
- Retrieval
- Top-K results
- Context passed to the LLM
- Grounded generation

You do not need advanced mathematical explanations of embeddings for the project. You should be able to explain what they represent and why they are used.

---

# 25. Final Project Goal

The project should tell a clear technical story:

```text
V1
Simple LLM application
      ↓
College JSON is directly supplied to the model

V2
Retrieval-Augmented application
      ↓
College documents are indexed
      ↓
Relevant information is retrieved
      ↓
Only relevant context is supplied to the model
      ↓
Answer + source
```

The objective is not to build the largest AI system possible.

The objective is to demonstrate that the team understands **how an LLM application can evolve from a simple prompt-based implementation into a grounded knowledge-retrieval system**.
