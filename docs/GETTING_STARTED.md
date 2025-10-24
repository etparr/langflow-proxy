# Getting Started with Langflow Proxy

This guide will walk you through setting up and running the Langflow Proxy server.

## Prerequisites

Before you begin, ensure you have:

- Python 3.13 or higher installed
- A deployed Langflow instance (see [Langflow Setup Guide](LANGFLOW_SETUP.md))
- Your Langflow API key
- Basic understanding of REST APIs

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd langflow-proxy
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

For development with testing tools:

```bash
pip install -e ".[dev]"
```

### 4. Configure Environment Variables

Copy the example environment file and edit it with your settings:

```bash
cp .env.example .env
```

Edit `.env` and set your Langflow API key:

```env
LANGFLOW_API_KEY=your_actual_api_key_here
```

You can obtain your API key from your Langflow instance's settings page.

### 5. Configure Your Agents

Edit `app/main.py` and update the `AGENT_CONFIGS` list with your actual Langflow endpoints:

```python
AGENT_CONFIGS = [
    {
        "path_prefix": "/my-agent",
        "url": "https://your-langflow-instance.com/api/v1/run/your-flow-id",
        "summary": "My Custom Agent",
        "timeout": 45.0
    },
    # Add more agents as needed
]
```

To get your Langflow flow URL:
1. Open your Langflow instance
2. Navigate to your flow
3. Click the API button
4. Copy the endpoint URL

### 6. Run the Server

Start the development server:

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the main.py script
python -m app.main
```

The server will start at `http://localhost:8000`.

### 7. Test Your Setup

````markdown
# Getting Started with Langflow Proxy

This guide provides setup and configuration instructions for the Langflow Proxy applications.

## What You'll Learn

- Application installation procedures
- Langflow connection configuration
- FastAPI server operation
- Streamlit chat interface usage

## Prerequisites

Required components:

- **Python 3.8 or higher**
  - Verify installation: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/
- **Langflow instance** with at least one deployed flow
  - See [Langflow Setup Guide](LANGFLOW_SETUP.md) for details
- **Langflow API key**
  - Obtain from Langflow settings

## Installation Steps

### Step 1: Download the Project

Navigate to project directory:
```bash
cd langflow-proxy
```

Clone from repository:
```bash
git clone <repository-url>
cd langflow-proxy
```

### Step 2: Install Dependencies

Install required Python packages:

```bash
pip install -e .
```

This installs all required dependencies. Installation may take 1-2 minutes.

For Streamlit interface:
```bash
pip install streamlit
```

### Step 3: Create Configuration File

Create a `.env` file in the `langflow-proxy` directory.

**macOS/Linux:**
```bash
echo "LANGFLOW_API_KEY=your-api-key-here" > .env
```

**Windows:**
```bash
echo LANGFLOW_API_KEY=your-api-key-here > .env
```

**Using a text editor:**
1. Create new file named `.env`
2. Add: `LANGFLOW_API_KEY=your-api-key-here`
3. Replace `your-api-key-here` with actual API key
4. Save in `langflow-proxy` directory

**Note:** Replace `your-api-key-here` with your actual Langflow API key.

## Running the Applications

Choose one or both applications based on your needs:

### Option 1: FastAPI Server (For Developers)

The FastAPI server provides a REST API for programmatic access to Langflow agents.

#### Step 1: Configure Your Agents

Edit `app.py` and locate the `AGENT_CONFIGS` section near the end of the file:

```python
AGENT_CONFIGS = [
    {
        "path_prefix": "/my-agent",
        "url": "https://your-langflow-url.com/api/v1/run/your-flow-id",
        "summary": "My Agent Name",
        "timeout": 30.0
    },
]
```

**Obtaining Langflow URL:**
1. Open your Langflow flow
2. Click the "API" button
3. Copy the endpoint URL
4. Paste in the `url` field

**Configuration example:**
```python
AGENT_CONFIGS = [
    {
        "path_prefix": "/customer-support",
        "url": "https://langflow.example.com/api/v1/run/abc123xyz",
        "summary": "Customer Support Agent",
        "timeout": 30.0
    },
]
```

#### Step 2: Start the Server

```bash
python app.py
```

Expected output:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 3: Verify Installation

Open web browser and visit:

**Interactive Documentation:** http://localhost:8000/docs

Available actions:
- View all configured agents
- Test message sending
- Review response formats

**Testing procedure:**
1. Click on your agent endpoint (e.g., `/api/customer-support`)
2. Click "Try it out"
3. Enter parameters:
   - `message`: "Hello!"
   - `session_id`: "test-123"
4. Click "Execute"
5. Review the response

### Option 2: Streamlit Chat Interface (For All Users)

The Streamlit interface provides a web-based chat interface requiring no programming knowledge.

#### Step 1: Run Streamlit

```bash
streamlit run streamlit_app.py
```

Browser will open automatically to the chat interface.

If browser doesn't open, navigate to: http://localhost:8501

#### Step 2: Configure Interface

Configure in the sidebar (left panel):

**Langflow Agent URL:** Enter your Langflow flow URL
- Obtain from Langflow (click API button)
- Format: `https://your-langflow.com/api/v1/run/your-flow-id`

**Langflow API Key:** Automatically loads from `.env`
- Can be manually entered if needed
- Input is masked for security

#### Step 3: Use the Interface

1. Enter message in chat box at bottom
2. Press Enter
3. Wait for response
4. Continue conversation

### Application Selection Guide

| Use Case | Recommended Application |
|----------|------------------------|
| Chat with agent | **Streamlit** |
| Quick agent testing | **Streamlit** |
| Classroom demonstration | **Streamlit** |
| Application development | **FastAPI** |
| System integration | **FastAPI** |
| Programmatic access | **FastAPI** |

## Common Issues and Solutions

### Issue: "command not found: python"

**Solution:** Use `python3` instead of `python`

Many systems use `python3` as the command identifier.

### Issue: "LANGFLOW_API_KEY is required"

**Solution:** 
1. Verify `.env` file exists
2. Confirm file contains `LANGFLOW_API_KEY=your-key`
3. Replace `your-key` with actual API key
4. File must be in `langflow-proxy` directory

### Issue: "Connection refused" or "Can't reach Langflow"

**Verification steps:**
1. Confirm Langflow instance is running
2. Verify URL accuracy (check for typos)
3. Test URL accessibility in browser
4. Validate API key

**Testing Langflow URL:**
URL should be accessible in browser without error page.

### Issue: "No module named..."

**Solution:** Reinstall dependencies
```bash
pip install -e .
pip install streamlit
```

### Issue: Streamlit shows "No agents available"

**For Streamlit:**
- Verify Langflow Agent URL entered in sidebar
- Click "New Session" to refresh

**For FastAPI:**
- Confirm `AGENT_CONFIGS` in `app.py` contains at least one agent
- Restart the server

### Issue: "Address already in use"

**Solution:** Port conflict exists
```bash
# For FastAPI (port 8000):
# Terminate other applications using port 8000, or change port

# For Streamlit (port 8501):
streamlit run streamlit_app.py --server.port 8502
```

## Testing Your Setup

### Verification Checklist

[ ] **Python installed**: `python --version` shows 3.8 or higher  
[ ] **Packages installed**: No errors when running pip install  
[ ] **API key configured**: `.env` file exists with your key  
[ ] **Langflow accessible**: Can open Langflow URL in browser  
[ ] **App starts**: No errors when running the app  
[ ] **Can send message**: Successfully get a response  

### For FastAPI:

1. **Check the server started:**
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```

2. **Visit the docs page:**
   http://localhost:8000/docs

3. **Try the list endpoint:**
   http://localhost:8000/api/solutions

4. **Send a test message:**
   Use the interactive docs to send a message

### For Streamlit:

1. **Check Streamlit started:**
   ```
   You can now view your Streamlit app in your browser.
   ```

2. **Streamlit shows green:**
   "Configuration loaded"

3. **Send a test message:**
   Type "Hello!" and press Enter

4. **Receive a response:**
   The agent should reply

## Understanding Your Setup

### Project Structure

Project directory contents:

```
langflow-proxy/
├── app.py              ← FastAPI server
├── streamlit_app.py    ← Streamlit interface
├── .env                ← API key configuration (create this)
├── examples.py         ← Code examples
├── pyproject.toml      ← Dependency specifications
└── docs/               ← Documentation files
```

The project uses a simplified two-file structure for educational purposes.

### Key Concepts

**API Key:** Authentication credential for Langflow API access.

**Session ID:** Unique identifier for a conversation. Messages with matching session IDs are treated as a continuous conversation.

**Endpoint:** URL path for sending messages (e.g., `/api/customer-support`).

**Timeout:** Maximum wait time for agent response before terminating the request.

## Next Steps

After completing setup:

### Documentation Resources

- **[Streamlit Guide](STREAMLIT_GUIDE.md)** - Detailed interface documentation
- **[FastAPI Guide](FASTAPI_GUIDE.md)** - Server architecture explanation
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Langflow Setup](LANGFLOW_SETUP.md)** - Agent creation and configuration

### Example Exercises

1. **Basic communication test**
   - Send simple queries
   - Verify agent responses
   - Test follow-up questions

2. **Conversation memory test**
   - Ask "What's 2 + 2?"
   - Follow with "What's that plus 3?"
   - Agent should respond with 7

3. **Multi-agent testing**
   - Add multiple agents to `AGENT_CONFIGS`
   - Test each agent independently
   - Compare response patterns

4. **Configuration experiments**
   - Modify timeout values
   - Use different session IDs
   - Observe behavior changes

## Getting Help

### Debug Mode

Enable detailed logging:

1. Edit `.env` file
2. Add: `LOG_LEVEL=DEBUG`
3. Restart application
4. Review console output for detailed information

### Log Review

**FastAPI:** Check terminal where `python app.py` was executed

**Streamlit:** Check terminal where `streamlit run streamlit_app.py` was executed

### Common Questions

**Q: Are both applications required?**  
A: No. Applications function independently. Use Streamlit only, FastAPI only, or both.

**Q: Can other users access my Streamlit interface?**  
A: Yes, if they have network access to your machine and the correct URL.

**Q: Is this production-ready?**  
A: No. This is an educational version. Production deployment requires authentication and additional security measures.

**Q: Can I modify the code?**  
A: Yes. The code is designed to be readable and modifiable for learning purposes.

## Advanced Setup (Optional)

### Virtual Environment Configuration

For isolated package management:

```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -e .
```

### Port Configuration

**FastAPI:**
Edit `app.py`, modify final line:
```python
uvicorn.run("app:app", port=8080)  # Changed from 8000
```

**Streamlit:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Production Deployment

For production use, refer to [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Cloud hosting options
- Security implementation
- Scaling strategies
- Monitoring configuration

---

**Setup complete.** Begin with Streamlit for immediate agent interaction.

````
