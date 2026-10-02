# AI Researcher

An AI research assistant, built backend-first and incrementally: a FastAPI service that will grow from a single LLM call into a full research pipeline (search, retrieval, reranking, citations).

## Project structure

```text
backend/
├── app/
│   ├── main.py          # app factory: wires config, logging, routers
│   ├── api/             # HTTP layer (routers only, no business logic)
│   ├── services/        # business logic
│   ├── ai/              # LLM abstraction and providers
│   ├── schemas/         # request/response models
│   └── core/            # settings, logging
└── tests/
```

Dependencies point one way: `api → services → ai`. Services never import FastAPI; the `ai` layer never imports services.

## Setup

Requires Python 3.12+.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # then set LLM_API_KEY
```

## Run

```bash
cd backend
uvicorn app.main:app --reload
```

- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

## Test and lint

```bash
cd backend
pytest
ruff check .
ruff format --check .
```

## Configuration

Settings come from environment variables, with `backend/.env` as a local-development convenience. Real environment variables take priority over the file. See `backend/.env.example` for all options.
