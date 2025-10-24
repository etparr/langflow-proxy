# Streamlit Chat Interface Guide

This guide explains how to use and understand the Streamlit chat interface for interacting with Langflow AI agents.

## What is the Streamlit App?

The Streamlit app is a web-based chat interface for communicating with AI agents. It requires no coding knowledge to use.

## Why Use the Streamlit Interface?

- **No coding required** - Point-and-click interface
- **Visual interface** - Clear conversation history display
- **Easy agent switching** - Configure different AI agents
- **Session management** - Automatic conversation context handling
- **Demonstration ready** - Suitable for presentations and testing

## Starting the Streamlit App

### Step 1: Install Streamlit

If you haven't already:

```bash
pip install streamlit
```

Or install with all optional dependencies:

```bash
pip install -e ".[streamlit]"
```

### Step 2: Configure Your Settings

Create or edit your `.env` file:

```env
LANGFLOW_API_KEY=your-api-key-here
```

### Step 3: Run the App

```bash
streamlit run streamlit_app.py
```

Your browser will automatically open to the app!

If it doesn't, visit: http://localhost:8501

## Understanding the Interface

### Top Section: Title and Configuration

```
Langflow Chat Interface
Chat with your Langflow AI agents
```

This displays the application title and description.

### Sidebar: Configuration Panel

The sidebar (left panel) contains configuration options:

#### 1. Agent Configuration

**Langflow Agent URL**
- This is the direct URL to your Langflow agent
- Format: `https://your-langflow-url.com/api/v1/run/your-flow-id`
- Get this from Langflow by clicking the "API" button

**Langflow API Key**
- Your authentication key
- Automatically loaded from your `.env` file
- You can override it by typing a different key

#### 2. Session Management

**Current Session ID**
- A unique ID for your conversation
- Allows the agent to remember context
- Shown as `Session: abc12345...`

**New Session Button**
- Starts a fresh conversation
- Generates a new session ID
- Clears the chat history

#### 3. Settings (Expandable)

Click to access advanced options:

**Request Timeout**
- How long to wait for a response (in seconds)
- Default: 30 seconds
- Increase if your agent is slow

**Input Type**
- Usually "chat"
- Could be "text" for some agents

**Output Type**
- Usually "chat"
- Determines response format

### Main Chat Area

This displays the conversation history:

```
You: Hello!
Assistant: Hello! How can I help you today?
You: What's the weather?
Assistant: I'd be happy to check the weather for you...
```

**Features:**
- Automatic scrolling to latest message
- Clear distinction between your messages and agent responses
- Persistent history during your session

### Bottom: Message Input

```
Type your message here...
```

- Type your message
- Press Enter or click Send
- Wait for the response
- Continue the conversation!

## How to Use the App

### Basic Chat Flow

1. **Ensure Configuration**
   - Check that your Langflow URL is correct
   - Verify your API key is loaded

2. **Type a Message**
   - Click in the message box at the bottom
   - Type your question or statement
   - Press Enter

3. **Wait for Response**
   - You'll see a "Thinking..." indicator
   - The response appears in the chat area
   - You can immediately send another message

4. **Continue Conversation**
   - The agent remembers previous messages in the same session
   - Ask follow-up questions
   - Reference earlier parts of the conversation

### Starting a New Conversation

Click the **New Session** button when you want to:
- Start a completely fresh conversation
- Clear the agent's memory of previous messages
- Begin a different topic

### Adjusting Settings

If the agent is taking too long:
1. Click "Settings" in the sidebar
2. Increase the "Request Timeout"
3. Try your message again

## Understanding the Code

Here are the key components of the Streamlit application:

### 1. Page Configuration

```python
st.set_page_config(
    page_title="Langflow Chat",
    page_icon=":robot:",
    layout="centered"
)
```

**Purpose:** Configures the browser tab title and page layout.

### 2. Session State

```python
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
```

**Purpose:**
- Creates persistent variables across page interactions
- `session_id`: Unique identifier for the conversation
- `chat_history`: Stores all messages in the conversation

### 3. Langflow Client

```python
class LangflowClient:
    async def run(self, input_value: str, session_id: str) -> str:
        # Sends message to Langflow
        # Returns the response
```

**Purpose:**
- Formats messages for Langflow API
- Handles authentication
- Extracts response text from API response

### 4. Chat Display

```python
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)
```

**Purpose:** Renders the conversation history in the interface.

### 5. Message Input Handler

```python
if prompt := st.chat_input("Type your message here..."):
    # Add to history
    st.session_state.chat_history.append(("user", prompt))
    
    # Get response
    response = asyncio.run(client.run(prompt, session_id))
    
    # Add response to history
    st.session_state.chat_history.append(("assistant", response))
```

**Purpose:** Processes new messages and updates the chat display.

## Customizing the App

### Change the Title

```python
st.title("My Custom Chat Interface")
```

### Change the Icon

```python
st.set_page_config(page_icon=":speech_balloon:")
```

### Add a Custom Greeting

```python
if not st.session_state.chat_history:
    st.info("Welcome! Start chatting below.")
```

### Modify Default Timeout

```python
timeout = st.sidebar.slider(
    "Request Timeout (seconds)",
    min_value=10,
    max_value=300,  # Changed from 120
    value=30
)
```

## Common Use Cases

### 1. Testing a New Agent

1. Deploy your agent in Langflow
2. Get the API URL
3. Paste it in the Streamlit sidebar
4. Test various queries
5. Verify responses are correct

### 2. Demonstrating AI Capabilities

1. Run the app
2. Share your screen
3. Show how the agent responds
4. Switch between different agents
5. Demonstrate conversation memory

### 3. Classroom Exercise

**For Students:**
1. Each student runs their own instance
2. They configure their own Langflow agent
3. They test and refine their agent
4. They present their results

**For Instructors:**
1. Pre-configure agents for students
2. Provide the Langflow URLs
3. Students focus on interaction patterns
4. Discuss responses and improvements

### 4. Quick Prototyping

1. Build a flow in Langflow
2. Immediately test in Streamlit
3. Iterate on the Langflow design
4. Refresh the app to test changes
5. Repeat until satisfied

## Troubleshooting

### App Won't Start

**Error:** "streamlit: command not found"
```bash
pip install streamlit
```

**Error:** "No module named 'streamlit'"
```bash
pip install -e ".[streamlit]"
```

### Connection Errors

**Error:** "Connection refused"
- **Check:** Is your Langflow URL correct?
- **Check:** Is Langflow actually running?
- **Check:** Can you access the URL in a browser?

**Error:** "Unauthorized" or "403"
- **Check:** Is your API key correct?
- **Check:** Is the API key still valid?
- **Solution:** Get a new API key from Langflow

### Response Issues

**Problem:** Agent takes too long, then times out
- **Solution:** Increase the timeout slider
- **Alternative:** Optimize your Langflow flow

**Problem:** Agent gives strange or empty responses
- **Check:** Test the Langflow flow directly
- **Check:** Look at the Streamlit error messages
- **Debug:** Enable debug mode in Langflow

**Problem:** Agent doesn't remember context
- **Check:** Verify you're using the same session ID for all messages
- **Check:** Review the session ID displayed in the sidebar
- **Solution:** Avoid clicking "New Session" during active conversations

### Display Issues

**Problem:** Messages not displaying
- **Solution:** Click "New Session" to refresh the interface
- **Alternative:** Reload the browser page

**Problem:** Chat history cleared unexpectedly
- **Note:** History is lost when the page is refreshed
- **Workaround:** Keep the application open in one browser tab

## Advanced Features

### Adding Error Displays

Show more detailed errors to users:

```python
try:
    response = asyncio.run(client.run(prompt, session_id))
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.exception(e)  # Show full error details
```

### Adding Response Time

Show how long each response took:

```python
import time

start_time = time.time()
response = asyncio.run(client.run(prompt, session_id))
elapsed = time.time() - start_time

st.caption(f"Response time: {elapsed:.2f} seconds")
```

### Exporting Chat History

Allow users to download their conversation:

```python
if st.sidebar.button("Download Chat"):
    chat_text = "\n\n".join([
        f"{role.title()}: {message}"
        for role, message in st.session_state.chat_history
    ])
    st.sidebar.download_button(
        "Download",
        chat_text,
        "chat_history.txt"
    )
```

### Multiple Agent Support

Let users choose between agents:

```python
agents = {
    "Customer Support": "https://langflow.com/api/v1/run/support-id",
    "Research Assistant": "https://langflow.com/api/v1/run/research-id",
}

selected = st.sidebar.selectbox("Choose an agent:", list(agents.keys()))
agent_url = agents[selected]
```

## Best Practices

### For Users

1. **Start with simple questions** to verify agent functionality
2. **Be clear and specific** in your messages
3. **Use New Session** when changing conversation topics
4. **Avoid refreshing the page** to preserve history
5. **Adjust timeout** for queries requiring longer processing time

### For Developers

1. **Test Langflow flows** independently before integrating with Streamlit
2. **Provide clear error messages** for user guidance
3. **Set reasonable default timeouts** based on agent complexity
4. **Add helpful instructions** in the interface
5. **Include example queries** to demonstrate agent capabilities

### For Instructors

1. **Pre-configure agents** for student use
2. **Provide clear usage instructions**
3. **Create example conversations** for demonstration
4. **Maintain backup agents** in case of failure
5. **Monitor student usage** to identify common issues

## Comparison with FastAPI

| Feature | Streamlit App | FastAPI Server |
|---------|---------------|----------------|
| **Interface** | Visual chat UI | API endpoints |
| **User** | Anyone (no coding) | Developers |
| **Purpose** | Testing & demos | Integration |
| **Setup** | Run and use | Configure + integrate |
| **Best for** | Quick interactions | Building applications |

**When to use Streamlit:**
- Testing agents
- Demonstrations
- Classroom exercises
- Quick prototypes
- Non-technical users

**When to use FastAPI:**
- Building applications
- Integration with other systems
- Multiple agents
- Production deployments
- Programmatic access

## Integration Examples

### Using Both Together

You can use the FastAPI server as a backend for Streamlit:

```python
# Instead of connecting directly to Langflow,
# connect to your FastAPI server

async def chat_via_proxy(message: str, session_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/my-agent",
            json={"message": message, "session_id": session_id}
        )
        return response.json()["data"]
```

**Benefits:**
- Centralized agent management
- Better security (API key in one place)
- Easier to switch Langflow instances

## Next Steps

- Read the [FastAPI Guide](FASTAPI_GUIDE.md) to understand the server
- Check the [Getting Started Guide](GETTING_STARTED.md) for setup
- See the [Langflow Setup Guide](LANGFLOW_SETUP.md) for agent creation
- Try the [API Reference](API_REFERENCE.md) for programmatic access

## Learning Resources

To learn more about Streamlit:

- **Official Docs:** https://docs.streamlit.io/
- **API Reference:** https://docs.streamlit.io/library/api-reference
- **Gallery:** https://streamlit.io/gallery
- **Tutorials:** https://docs.streamlit.io/get-started/tutorials

---

**Remember:** Streamlit is designed for simplicity and rapid prototyping.
