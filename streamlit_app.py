"""
Streamlit Chat Interface for Langflow - Educational Example

A simple Streamlit app that communicates directly with Langflow APIs.
Perfect for non-technical users who want a simple chat interface!
"""

import streamlit as st
import httpx
import asyncio
import os
from typing import Optional
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LangflowClient:
    """Direct client for communicating with Langflow APIs."""
    
    def __init__(self, url: str, api_key: str, timeout: float = 30.0):
        """Initialize the Langflow client.
        
        Args:
            url: The Langflow API endpoint URL
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
    
    async def run(
        self,
        input_value: str,
        session_id: str,
        input_type: str = "chat",
        output_type: str = "chat"
    ) -> str:
        """Send a message to the Langflow endpoint and get response."""
        payload = {
            "input_value": input_value,
            "input_type": input_type,
            "output_type": output_type,
            "session_id": session_id,
        }

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract the response text from Langflow's nested structure
            return self._extract_response_text(result)
    
    def _extract_response_text(self, result: dict) -> str:
        """Extract the response text from Langflow's response structure."""
        try:
            # Navigate the nested structure
            outer_nodes = result.get("outputs", [])
            if not outer_nodes:
                return "No response from agent"

            last_outer = outer_nodes[-1]
            inner_nodes = last_outer.get("outputs", [])
            if not inner_nodes:
                return "No response from agent"

            last_inner = inner_nodes[-1]
            text = last_inner.get("results", {}).get("message", {}).get("text")
            
            return text or "Empty response from agent"
        except (TypeError, IndexError, KeyError):
            return "Error parsing agent response"


# Streamlit app configuration
st.set_page_config(
    page_title="Langflow Chat",
    page_icon=":robot:",
    layout="centered"
)

st.title("Langflow Chat Interface")
st.markdown("Chat with your Langflow AI agents")

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar configuration
st.sidebar.header("Configuration")

# Agent Configuration
st.sidebar.subheader("Agent Configuration")

# Langflow endpoint URL
agent_url = st.sidebar.text_input(
    "Langflow Agent URL",
    value=os.getenv("LANGFLOW_URL", ""),
    help="Your Langflow API endpoint URL (e.g., https://your-langflow.com/api/v1/run/your-flow-id)",
    placeholder="https://your-langflow.com/api/v1/run/flow-id"
)

# Langflow API key
api_key = st.sidebar.text_input(
    "Langflow API Key",
    value=os.getenv("LANGFLOW_API_KEY", ""),
    type="password",
    help="Your Langflow API key for authentication"
)

# Session management
st.sidebar.markdown("---")
st.sidebar.subheader("Session Management")

# Display current session ID
st.sidebar.text(f"Session: {st.session_state.session_id[:8]}...")

# New session button
if st.sidebar.button("New Session", help="Start a fresh conversation"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.rerun()

# Advanced settings
st.sidebar.markdown("---")
with st.sidebar.expander("Settings"):
    timeout = st.slider(
        "Request Timeout (seconds)",
        min_value=10,
        max_value=120,
        value=30,
        help="How long to wait for a response"
    )
    
    input_type = st.text_input(
        "Input Type",
        value="chat",
        help="Usually 'chat' for conversational agents"
    )
    
    output_type = st.text_input(
        "Output Type",
        value="chat",
        help="Usually 'chat' for text responses"
    )

# Validation
if not agent_url:
    st.warning("Please enter your Langflow Agent URL in the sidebar to get started.")
    st.info("""
    **How to find your Langflow URL:**
    1. Open your Langflow flow
    2. Click the "API" button
    3. Copy the endpoint URL
    4. Paste it in the sidebar
    """)
    st.stop()

if not api_key:
    st.warning("Please enter your Langflow API Key in the sidebar.")
    st.info("""
    **How to get your API key:**
    1. Open your Langflow instance
    2. Go to Settings
    3. Find or generate an API key
    4. Paste it in the sidebar (or add to .env file)
    """)
    st.stop()

# Initialize Langflow client
try:
    client = LangflowClient(url=agent_url, api_key=api_key, timeout=timeout)
    st.sidebar.success("Configuration loaded")
except Exception as e:
    st.sidebar.error(f"Configuration error: {str(e)}")
    st.stop()

# Main chat interface
st.markdown("---")

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# Chat input
if prompt := st.chat_input("💬 Type your message here..."):
    # Add user message to history and display it
    st.session_state.chat_history.append(("user", prompt))
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = asyncio.run(
                    client.run(
                        input_value=prompt,
                        session_id=st.session_state.session_id,
                        input_type=input_type,
                        output_type=output_type
                    )
                )
                st.write(response)
                # Add response to history
                st.session_state.chat_history.append(("assistant", response))
            except httpx.HTTPStatusError as e:
                error_msg = f"Server error ({e.response.status_code}): {e.response.text}"
                st.error(error_msg)
                st.session_state.chat_history.append(("assistant", error_msg))
            except httpx.RequestError as e:
                error_msg = f"Connection error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append(("assistant", error_msg))
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                st.error(error_msg)
                st.session_state.chat_history.append(("assistant", error_msg))

# Sidebar information
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.markdown("""
**Langflow Chat Interface**

A simple interface for chatting with your Langflow AI agents.

**Features:**
- Direct connection to Langflow
- Conversation history
- Session management
- Configurable timeouts

**Note:** This is an educational example designed for classroom use.
""")

# Technical details
with st.sidebar.expander("Technical Details"):
    st.json({
        "agent_url": agent_url,
        "session_id": st.session_state.session_id,
        "chat_messages": len(st.session_state.chat_history),
        "timeout": timeout,
        "input_type": input_type,
        "output_type": output_type
    })

# Instructions for first-time users
if not st.session_state.chat_history:
    st.info("""
    **Welcome to Langflow Chat!** 
    
    **To get started:**
    1. Make sure your Langflow URL and API Key are configured in the sidebar
    2. Type your message in the chat box below
    3. Press Enter or click Send
    4. Continue the conversation!
    
    **Tips:**
    - The agent remembers previous messages in the same session
    - Click "New Session" in the sidebar to start fresh
    - Adjust the timeout if responses are slow
    """)