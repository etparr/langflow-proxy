"""
Consolidated Langflow Proxy Server - Educational Example

A simple FastAPI application that proxies requests to Langflow deployments.
This single-file version contains all the necessary components for educational purposes.
"""

import os
import logging
import json
import httpx
from typing import Any, Dict, Optional, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv(override=True)

# =============================================================================
# CONFIGURATION
# =============================================================================

class Settings:
    """Application settings with sensible defaults."""

    # Environment detection
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Timeout settings (in seconds)
    DEFAULT_REQUEST_TIMEOUT: float = float(os.getenv("DEFAULT_REQUEST_TIMEOUT", "30.0"))

    # Langflow settings
    LANGFLOW_API_KEY: Optional[str] = os.getenv("LANGFLOW_API_KEY")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT.lower() in ("production", "prod")

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT.lower() in ("development", "dev")

    @classmethod
    def validate(cls) -> None:
        """Validate required settings on startup."""
        instance = cls()
        
        # Show masked API key in development for debugging
        if instance.is_development and instance.LANGFLOW_API_KEY:
            api_key = instance.LANGFLOW_API_KEY
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            print(f"DEBUG: LANGFLOW_API_KEY loaded (length: {len(api_key)}): {masked_key}")
        
        # Validate required settings
        if not instance.LANGFLOW_API_KEY:
            raise ValueError(
                "LANGFLOW_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )


settings = Settings()

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class ChatRequest(BaseModel):
    """Request model for chatting with a Langflow agent."""
    message: str = Field(
        ...,
        description="The message to send to the Langflow agent",
        min_length=1,
        max_length=10000
    )
    session_id: str = Field(
        ...,
        description="Unique session identifier for conversation context",
        min_length=1,
        max_length=255
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "What is the weather like today?",
                    "session_id": "user-123-session-abc"
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Response model from a Langflow agent."""
    data: str = Field(
        ...,
        description="The response text from the Langflow agent"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": "The weather today is sunny with a high of 75°F."
                }
            ]
        }
    }


class AgentInfo(BaseModel):
    """Information about a registered agent."""
    url: str = Field(..., description="API endpoint path for the agent")
    solution: str = Field(..., description="Name/description of the agent")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "/competitive-insights-agent",
                    "solution": "Competitive Insights Agent"
                }
            ]
        }
    }

# =============================================================================
# HTTP CLIENT MANAGEMENT
# =============================================================================

# Global HTTP client
_http_client: httpx.AsyncClient | None = None


async def get_http_client() -> httpx.AsyncClient:
    """Get or create a simple HTTP client."""
    global _http_client

    if _http_client is None:
        timeout = httpx.Timeout(30.0)
        _http_client = httpx.AsyncClient(timeout=timeout)
        logger.info("HTTP client initialized")

    return _http_client


async def close_http_client():
    """Close the HTTP client."""
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None
        logger.info("HTTP client closed")

# =============================================================================
# LANGFLOW CLIENT
# =============================================================================

class LangFlowClient:
    """Simple async wrapper around a Langflow REST endpoint."""

    def __init__(self, *, url: str, timeout: float | None = None) -> None:
        """Initialize the Langflow client."""
        if not url:
            raise ValueError("LangFlowClient init error: 'url' must not be empty")

        self.url = url.rstrip("/")
        self.token = settings.LANGFLOW_API_KEY
        self.timeout = timeout or settings.DEFAULT_REQUEST_TIMEOUT
        
        # Validate API key
        if not self.token:
            logger.error("LANGFLOW_API_KEY is not set in configuration")
            raise ValueError("LANGFLOW_API_KEY is required but not found in configuration")
        
        # Log initialization (mask API key in production)
        if settings.is_development:
            masked_token = f"{self.token[:8]}...{self.token[-4:]}" if len(self.token) > 12 else "***"
            logger.info(f"LangFlowClient initialized with API key: {masked_token}")
        else:
            logger.info("LangFlowClient initialized with API key configured")
        
        logger.debug(f"LangFlowClient initialized with URL: {self.url}")

    async def run(
        self,
        input_value: str,
        *,
        input_type: str = "chat",
        output_type: str = "chat",
        session_id: str,
    ) -> Dict[str, Any]:
        """Execute a request to the Langflow endpoint."""
        # Prepare request payload
        payload = {
            "input_value": input_value,
            "input_type": input_type,
            "output_type": output_type,
            "session_id": session_id,
        }

        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.token,
        }
        
        # Debug log headers (mask API key) in development only
        if settings.is_development:
            debug_headers = headers.copy()
            if debug_headers.get("x-api-key"):
                key = debug_headers["x-api-key"]
                debug_headers["x-api-key"] = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
            logger.debug(f"Request headers: {debug_headers}")
        
        # Get HTTP client
        client = await get_http_client()
        
        logger.info(f"Making request to LangFlow: {self.url} (session: {session_id})")
        
        try:
            # Make the request
            resp = await client.post(
                self.url, 
                json=payload, 
                headers=headers, 
                timeout=self.timeout
            )
            resp.raise_for_status()
            result = resp.json()
            
            logger.info(f"LangFlow request successful: {self.url} (status: {resp.status_code})")
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(
                f"LangFlowClient HTTP error {e.response.status_code}: {e.response.text}",
                exc_info=True,
            )
            raise RuntimeError(
                f"Upstream error {e.response.status_code}: {e.response.text}"
            ) from e
            
        except httpx.RequestError as e:
            logger.error(f"LangFlowClient request failed: {str(e)}", exc_info=True)
            raise RuntimeError(f"Request failed: {e}") from e
            
        except Exception as e:
            logger.exception("Unexpected error in LangFlowClient")
            raise

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def extract_last_text(result: dict) -> str | None:
    """Extract the last message text from a Langflow run result."""
    try:
        # Navigate the nested structure:
        # result["outputs"] -> list of output nodes
        outer_nodes = result.get("outputs", [])
        if not outer_nodes:
            return None

        # Get the last output node
        last_outer = outer_nodes[-1]

        # Each output node has its own "outputs" list
        inner_nodes = last_outer.get("outputs", [])
        if not inner_nodes:
            return None

        # Get the last inner node
        last_inner = inner_nodes[-1]

        # Extract the text from results.message.text
        return last_inner.get("results", {}).get("message", {}).get("text")
        
    except (TypeError, IndexError, KeyError):
        # Any structural mismatch returns None
        return None

# =============================================================================
# AGENT REGISTRATION
# =============================================================================

# Global registry of all registered agents
REGISTERED_AGENTS: List[Dict] = []


def create_langflow_router(
    *, path_prefix: str, url: str, summary: str, timeout: float | None = None
) -> APIRouter:
    """Create a simple router for a Langflow agent endpoint."""
    actual_timeout = timeout or settings.DEFAULT_REQUEST_TIMEOUT
    
    # Create router with appropriate prefix and tags
    router = APIRouter(
        prefix="/api" + path_prefix,
        tags=["langflow", path_prefix.strip("/")],
    )

    @router.post(
        "",
        response_model=ChatResponse,
        summary=summary,
        description=f"Send a message to the {summary}",
    )
    async def chat(req: ChatRequest, request: Request) -> ChatResponse:
        """Handle chat requests to this agent."""
        logger.info(f"Agent request to {path_prefix} with session_id: {req.session_id}")
        
        return await _handle_chat_request(req, url, actual_timeout)

    # Register agent in global registry
    REGISTERED_AGENTS.append({"url": path_prefix, "solution": summary})
    
    logger.info(f"Created Langflow router for {summary} at {path_prefix}")

    return router


async def _handle_chat_request(
    req: ChatRequest, url: str, timeout: float
) -> ChatResponse:
    """Handle the actual chat request logic."""
    # Create Langflow client for this request
    client = LangFlowClient(url=url, timeout=timeout)
    
    try:
        # Execute the flow
        result = await client.run(
            input_value=req.message,
            session_id=req.session_id,
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON from LangFlow at {url}: {e}")
        raise HTTPException(
            status_code=502, 
            detail="Upstream service returned invalid JSON."
        )
    except Exception as e:
        logger.exception(f"Unhandled error in chat handler: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error."
        )

    # Validate we got a response
    if not result:
        logger.warning(f"Empty response from LangFlow service at {url}")
        raise HTTPException(
            status_code=502, 
            detail="Upstream service returned no content."
        )

    # Extract the text from the nested response structure
    last_text = extract_last_text(result)
    if not last_text:
        logger.warning(f"No output text found in LangFlow response: {result}")
        raise HTTPException(
            status_code=502, 
            detail="LangFlow response malformed or missing output."
        )

    return ChatResponse(data=last_text)

# =============================================================================
# FASTAPI APPLICATION SETUP
# =============================================================================

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting Langflow Proxy Server...")
    settings.validate()
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Log level: {settings.LOG_LEVEL}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Langflow Proxy Server...")
    await close_http_client()
    logger.info("HTTP client closed")


# Create FastAPI application
app = FastAPI(
    title="Langflow Proxy Server",
    description=(
        "A simple educational proxy server for Langflow deployments. "
        "Demonstrates basic API routing and communication with Langflow agents."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ROUTES
# =============================================================================

@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint redirects to docs."""
    return RedirectResponse(url="/docs")


# Router for listing all registered agents
agents_list_router = APIRouter(prefix="/api", tags=["agents"])


@agents_list_router.get(
    "/solutions",
    summary="List all available agents",
    description="Returns a list of all registered Langflow agents with their endpoints",
)
async def get_solutions() -> List[Dict]:
    """Get list of all registered agents."""
    return sorted(REGISTERED_AGENTS, key=lambda item: item["solution"])


# Include the agents list router
app.include_router(agents_list_router)

# =============================================================================
# AGENT CONFIGURATIONS
# =============================================================================

# Example agent configurations
# In a real application, these would come from a configuration file or database
AGENT_CONFIGS = [
    {
        "path_prefix": "/example-agent",
        "url": "https://langflow.example.com/api/v1/run/flow-id-here",
        "summary": "Example Agent",
        "timeout": 30.0
    },
    # Add more agents as needed
]

# Register agent routers
for config in AGENT_CONFIGS:
    router = create_langflow_router(
        path_prefix=config["path_prefix"],
        url=config["url"],
        summary=config["summary"],
        timeout=config.get("timeout")
    )
    app.include_router(router, tags=["agents"])
    logger.info(f"Registered agent: {config['summary']} at {config['path_prefix']}")

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development,
        log_level=settings.LOG_LEVEL.lower()
    )