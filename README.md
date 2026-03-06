# Minimal Inference Gateway

A FastAPI-based gateway for AI inference with multi-backend support. Routes requests to different backends (Echo, HTTP) based on the `model` field in the request body.

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Backends

Edit `config.yaml` to define your backends:

```yaml
default_backend: local

backends:
  - name: local
    type: echo

  - name: remote
    type: http
    url: http://localhost:8081
    timeout: 60.0
```

### 3. Run the Gateway

```bash
uv run python -m app.main
```

The server starts on `http://localhost:8080`.

## Configuration

### Config File (config.yaml)

| Field | Description |
|-------|-------------|
| `default_backend` | Backend name to use when model field is missing or unrecognized |
| `backends` | List of backend configurations |
| `backends[].name` | Unique identifier for the backend |
| `backends[].type` | Backend type: `echo` or `http` |
| `backends[].url` | (HTTP only) Base URL of the remote backend |
| `backends[].timeout` | (HTTP only) Request timeout in seconds |

### Backend Types

- **echo**: Returns "Echo: {prompt}" - useful for testing
- **http**: Forwards requests to a remote HTTP endpoint

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | Server port |
| `HOST` | 0.0.0.0 | Server bind address |
| `CONFIG_FILE` | config.yaml | Path to YAML config file |

Create a `.env` file:

```bash
PORT=8080
HOST=0.0.0.0
CONFIG_FILE=config.yaml
```

## Usage Modes

### Echo-Only Mode (No Remote Backend)

Set `config.yaml` to only include the echo backend:

```yaml
default_backend: local

backends:
  - name: local
    type: echo
```

All requests will be handled by the local echo backend regardless of the model field.

### With Remote Backend

Add an HTTP backend pointing to your remote endpoint:

```yaml
default_backend: local

backends:
  - name: local
    type: echo

  - name: remote
    type: http
    url: http://localhost:8081
    timeout: 60.0
```

The remote backend can be:
- A llama.cpp server
- A classmate's gateway
- A Modal deployment
- Any OpenAI-compatible endpoint

## API

### POST /v1/chat/completions

**Request:**

```json
{
  "model": "local",
  "messages": [
    {"role": "user", "content": "Hello world"}
  ]
}
```

**Response:**

```json
{
  "id": "uuid-string",
  "backend": "local",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Echo: Hello world"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 2,
    "completion_tokens": 3,
    "total_tokens": 5
  }
}
```

The `backend` field indicates which backend handled the request.

## Testing

Run the test script:

```bash
./test.sh
```

Or use curl directly:

```bash
# Test 1: Route to local backend
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "local", "messages": [{"role": "user", "content": "Hello"}]}'

# Test 2: Route to remote backend
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "remote", "messages": [{"role": "user", "content": "Hello"}]}'

# Test 3: Fallback to default (omit model field)
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

## Project Structure

```
app/
├── main.py                       # FastAPI app entry point
├── api/v1/endpoints/
│   └── chat_completion.py        # API endpoint
├── core/
│   ├── config.py                 # Settings & YAML config loading
│   ├── dependencies.py           # DI providers
│   └── utils/
│       ├── prompt.py             # Extract user messages
│       ├── request_id.py         # Request ID handling
│       └── token_usage.py        # Token counting
├── schemas/
│   └── chat.py                   # Pydantic models
└── services/
    ├── inference.py              # Routing logic
    └── backends/
        ├── base.py               # Backend interface (ABC)
        ├── echo_backend.py       # Echo implementation
        └── http_backend.py       # HTTP implementation
```

## Backend Interface

All backends implement `BaseBackend`:

```python
class BaseBackend(ABC):
    @abstractmethod
    async def generate(self, prompt: str, payload: dict, request_id: str) -> str:
        pass
```

The `InferenceService` only calls `generate()` - no if/else on backend type in the handler.
