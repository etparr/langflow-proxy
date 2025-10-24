# FastAPI Server Guide

This guide explains how the FastAPI server works in simple terms, suitable for non-technical professionals learning about AI and APIs.

## What is the FastAPI Server?

Think of the FastAPI server as a **smart receptionist** for your AI agents:

1. It receives requests (messages) from applications
2. It knows which AI agent should handle each request
3. It sends the message to the right agent in Langflow
4. It receives the response and sends it back

### Why Use a Proxy Server?

Instead of having every application connect directly to Langflow, the proxy server:

- **Centralizes access**: One place to manage all your agents
- **Simplifies configuration**: Applications don't need Langflow API keys
- **Adds flexibility**: You can switch Langflow instances without changing your apps
- **Improves security**: API keys are kept in one secure location

## Understanding the Code

The entire FastAPI server is in one file: `app.py`. Let's break it down into sections:

### 1. Configuration (Settings Class)

```python
class Settings:
    """Application settings with sensible defaults."""
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LANGFLOW_API_KEY: Optional[str] = os.getenv("LANGFLOW_API_KEY")
    DEFAULT_REQUEST_TIMEOUT: float = 30.0
```

**What this does:**
- Loads settings from environment variables
- Sets default values if not provided
- Validates that required settings (like API key) exist

**Think of it as:** The server's rulebook that defines how it should behave.

### 2. Data Models (Pydantic Models)

```python
class ChatRequest(BaseModel):
    message: str = Field(..., description="The message to send")
    session_id: str = Field(..., description="Session identifier")

class ChatResponse(BaseModel):
    data: str = Field(..., description="The response text")
```

**What this does:**
- Defines the structure of requests and responses
- Automatically validates incoming data
- Generates documentation

**Think of it as:** Forms that define what information can be sent and received.

### 3. HTTP Client

```python
async def get_http_client() -> httpx.AsyncClient:
    """Get or create a simple HTTP client."""
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=30.0)
    return _http_client
```

**What this does:**
- Creates a reusable connection to make HTTP requests
- Manages timeouts (how long to wait for responses)
- Reuses connections for better performance

**Think of it as:** A phone line that stays open instead of dialing every time.

### 4. Langflow Client

```python
class LangFlowClient:
    """Simple async wrapper around a Langflow REST endpoint."""
    
    async def run(self, input_value: str, session_id: str) -> Dict[str, Any]:
        """Execute a request to the Langflow endpoint."""
        payload = {
            "input_value": input_value,
            "session_id": session_id,
        }
        # ... makes HTTP request to Langflow ...
```

**What this does:**
- Formats messages for Langflow
- Sends messages with authentication
- Handles errors gracefully
- Extracts the response text

**Think of it as:** A translator that speaks Langflow's language.

### 5. Agent Registration

```python
def create_langflow_router(path_prefix: str, url: str, summary: str):
    """Create a simple router for a Langflow agent endpoint."""
    
    @router.post("")
    async def chat(req: ChatRequest) -> ChatResponse:
        """Handle chat requests to this agent."""
        # ... process the message ...
```

**What this does:**
- Creates a unique endpoint for each agent
- Handles incoming messages
- Routes them to the correct Langflow agent
- Returns responses in a standard format

**Think of it as:** Creating a dedicated phone extension for each agent.

### 6. Agent Configuration

```python
AGENT_CONFIGS = [
    {
        "path_prefix": "/example-agent",
        "url": "https://langflow.example.com/api/v1/run/flow-id",
        "summary": "Example Agent",
        "timeout": 30.0
    },
]
```

**What this does:**
- Lists all your AI agents
- Specifies their endpoints
- Connects each to its Langflow URL

**Think of it as:** Your organization's directory of AI agents.

## How Requests Flow Through the System

Let's trace what happens when someone sends a message:

```
User Application
      ↓
   [Sends POST request to /api/my-agent]
      ↓
FastAPI Server Receives Request
      ↓
   [Validates the message format]
      ↓
   [Looks up which Langflow URL to use]
      ↓
Langflow Client
      ↓
   [Formats message for Langflow]
   [Adds API key for authentication]
      ↓
Langflow API
      ↓
   [AI agent processes the message]
      ↓
Response comes back
      ↓
   [Extract just the text response]
      ↓
FastAPI Returns Response
      ↓
User Application Gets Answer
```

## Key Features Explained

### Session Management

**What it is:** The ability to maintain context across multiple messages.

**How it works:**
```python
# First message
POST /api/my-agent
{
  "message": "What is 2 + 2?",
  "session_id": "user-123"
}
# Response: "4"

# Second message (same session_id)
POST /api/my-agent
{
  "message": "And what is that plus 3?",
  "session_id": "user-123"
}
# Response: "7" (remembers we were talking about 4)
```

The `session_id` tells Langflow that these messages are part of the same conversation.

### Error Handling

The server handles various errors gracefully:

```python
try:
    result = await client.run(...)
except httpx.HTTPStatusError as e:
    # Langflow returned an error
    raise HTTPException(status_code=502, detail="Upstream error")
except httpx.RequestError as e:
    # Connection failed
    raise HTTPException(status_code=500, detail="Connection failed")
```

**What this means:** Instead of crashing, the server returns helpful error messages.

### Logging

```python
logger.info(f"Agent request to {path_prefix} with session_id: {req.session_id}")
```

The server logs important events, which helps with:
- Debugging problems
- Understanding usage patterns
- Monitoring performance

## API Endpoints

### 1. Root (/)
- **Purpose:** Redirects to documentation
- **Method:** GET
- **Response:** Redirects to `/docs`

### 2. Health Check
- **Purpose:** Check if server is running
- **Endpoint:** GET /health (not implemented in current version)
- **Use case:** Monitoring systems checking server status

### 3. List Agents
- **Purpose:** See all available agents
- **Endpoint:** GET /api/solutions
- **Response:** Array of agent information

```json
[
  {
    "url": "/customer-support",
    "solution": "Customer Support Agent"
  }
]
```

### 4. Chat with Agent
- **Purpose:** Send a message to an agent
- **Endpoint:** POST /api/{agent-name}
- **Request:**
```json
{
  "message": "Hello, agent!",
  "session_id": "unique-session-id"
}
```
- **Response:**
```json
{
  "data": "Hello! How can I help you today?"
}
```

## Running the Server

### Development Mode

```bash
python app.py
```

This runs with:
- Auto-reload (restarts when you change code)
- Debug logging
- Development settings

### Production Mode

```bash
# Set environment first
export ENVIRONMENT=production

# Run with production settings
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

This runs with:
- Multiple workers (handles more traffic)
- Production logging
- No auto-reload

## Testing Your Server

### Using the Interactive Docs

1. Start the server
2. Open http://localhost:8000/docs
3. Click on an endpoint
4. Click "Try it out"
5. Fill in the parameters
6. Click "Execute"

You'll see the request and response!

### Using curl

```bash
# List agents
curl http://localhost:8000/api/solutions

# Send a message
curl -X POST http://localhost:8000/api/my-agent \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "test-123"}'
```

### Using Python

```python
import requests

# Send a message
response = requests.post(
    "http://localhost:8000/api/my-agent",
    json={
        "message": "Hello, agent!",
        "session_id": "my-session"
    }
)

result = response.json()
print(result["data"])
```

## Adding New Agents

To add a new agent:

1. **Get your Langflow URL**
   - Open your flow in Langflow
   - Click "API"
   - Copy the endpoint URL

2. **Edit app.py**
   Find the `AGENT_CONFIGS` list and add:
   ```python
   {
       "path_prefix": "/my-new-agent",
       "url": "https://your-langflow-url/api/v1/run/your-flow-id",
       "summary": "My New Agent",
       "timeout": 30.0
   }
   ```

3. **Restart the server**
   ```bash
   # Stop the server (Ctrl+C)
   # Start it again
   python app.py
   ```

4. **Test it**
   ```bash
   curl -X POST http://localhost:8000/api/my-new-agent \
     -H "Content-Type: application/json" \
     -d '{"message": "Test", "session_id": "test"}'
   ```

## Common Customizations

### Change the Port

```bash
# In app.py, change:
uvicorn.run("app:app", port=8080)  # Changed from 8000
```

### Add CORS for Specific Domains

```python
# In app.py, find add_middleware section:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # Only allow your domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Change Timeout

```env
# In .env file:
DEFAULT_REQUEST_TIMEOUT=60.0  # 60 seconds instead of 30
```

## Troubleshooting

### Server won't start

**Error:** "LANGFLOW_API_KEY is required"
- **Solution:** Create a `.env` file with your API key

**Error:** "Address already in use"
- **Solution:** Another app is using port 8000. Change the port or stop the other app.

### Agent requests fail

**Error:** 502 Bad Gateway
- **Cause:** Can't reach Langflow
- **Check:**
  - Is Langflow running?
  - Is the URL correct?
  - Is the API key valid?

**Error:** 504 Gateway Timeout
- **Cause:** Langflow took too long
- **Solution:** Increase `DEFAULT_REQUEST_TIMEOUT`

### Debugging Tips

1. **Enable debug logging:**
   ```env
   LOG_LEVEL=DEBUG
   ```

2. **Check the logs** for detailed error messages

3. **Test Langflow directly** using curl to verify it's working

4. **Use the /docs page** to test endpoints interactively

## Security Considerations

This is an educational example. For production:

1. **Add authentication:**
   - Require API keys from clients
   - Use OAuth or JWT tokens

2. **Add rate limiting:**
   - Prevent abuse
   - Protect Langflow from overload

3. **Validate input:**
   - Already done via Pydantic models
   - Add additional business logic validation

4. **Use HTTPS:**
   - Encrypt all communication
   - Use proper SSL certificates

5. **Secure API keys:**
   - Never commit to git
   - Use secret management services
   - Rotate regularly

## Next Steps

- Read the [API Reference](API_REFERENCE.md) for detailed endpoint documentation
- Check the [Configuration Guide](CONFIGURATION.md) for advanced settings
- See [GETTING_STARTED.md](GETTING_STARTED.md) for setup instructions
- Try the [Streamlit Guide](STREAMLIT_GUIDE.md) for a user interface

## Learning Resources

To learn more about the technologies used:

- **FastAPI:** https://fastapi.tiangolo.com/
- **Pydantic:** https://docs.pydantic.dev/
- **HTTPX:** https://www.python-httpx.org/
- **Langflow:** https://docs.langflow.org/

---

**Remember:** This is a learning tool. Take your time understanding each part!
