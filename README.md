# Minimal Inference Gateway

A minimalist, high-performance gateway for AI inference. This project serves as a versioned bridge that can either forward requests to an external provider (like llama.cpp) or operate in a standalone "Echo" mode for local development.

## Quick Start Guide

### 1. Installation

This project uses `uv` for modern, high-speed dependency management.

```bash
# Sync dependencies and create virtual environment
uv sync
```

### 2. Configuration

Create or edit the `.env` file in the root directory.

- **For Standalone Mode**: Leave `BACKEND_URL` empty.
- **For Backend Mode**: Set `BACKEND_URL` to your provider (e.g., `http://localhost:8081`).

```bash
PORT=8080
BACKEND_URL=http://localhost:8081
BACKEND_TIMEOUT=60.0
```

### 3. Execution

```bash
# Start the gateway server
uv run python -m app.main
```

## Project Skeleton

The project follows a clean architecture with clear separation of concerns:

```text
app/
├── main.py                 # App initialization using the Factory pattern
├── api/
│   └── v1/
│       ├── router.py       # Centralized route registration for versioned API
│       └── endpoints/
│           └── chat_completion.py  # Thin handler for Chat Completion logic
├── core/
│   ├── config.py           # Global settings management and .env integration
│   ├── dependencies.py     # Shared service providers (Dependency Injection)
│   └── utils/
│       ├── prompt.py       # Extraction logic for user messages
│       ├── request_id.py   # Unique ID generation and tracking
│       └── token_usage.py  # Utility for estimating token counts
├── schemas/
│   └── chat.py             # Pydantic models for request/response validation
└── services/
    ├── inference.py        # Orchestrates the decision between Echo and Backend
    ├── backend_client.py   # Handles communication with external AI providers
    └── echo_service.py     # Logic for generating standalone fallback replies
```

## Application Flow

When a client sends a request, the following precise steps occur:

1. **Entry**: The request hits `POST /v1/chat/completions`.
2. **Tracking**: `core/utils/request_id.py` checks for an existing `X-Request-Id` or generates a new one.
3. **Parsing**: The `api/v1/endpoints/chat_completion.py` handler validates the incoming JSON against the Pydantic schema.
4. **Extraction**: `core/utils/prompt.py` isolates the last user message from the conversation history.
5. **Injection**: FastAPI injects the `InferenceService` into the handler via `core/dependencies.py`.
6. **Orchestration**: `services/inference.py` checks the configuration:
    - **Backend Path**: If a URL is set, `services/backend_client.py` forwards the request and normalizes the response.
    - **Echo Path**: If no URL is set, `services/echo_service.py` generates a local response prefixed with "Echo: ".
7. **Finalization**: The handler attaches the `X-Request-Id` to the response headers and returns the final JSON to the client.

## Testing

Verify your setup with a simple curl command:

```bash
curl -i -X POST http://localhost:8080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "X-Request-Id: example-id-001" \
     -d '{"messages": [{"role": "user", "content": "Hello world"}]}'
```

## Group Members

- Layth AbuJafar
