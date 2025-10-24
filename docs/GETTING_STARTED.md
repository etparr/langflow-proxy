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

This guide will help you set up and use the Langflow Proxy applications - designed for non-technical professionals and classroom environments.

## What You'll Learn

- How to install the applications
- How to configure your Langflow connection
- How to run the FastAPI server
- How to use the Streamlit chat interface

## Prerequisites

Before you begin, you'll need:

- **Python 3.8 or higher** installed on your computer
  - Check by running: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/
- **A Langflow instance** with at least one deployed flow
  - See [Langflow Setup Guide](LANGFLOW_SETUP.md) if you need help
- **Your Langflow API key**
  - Get this from your Langflow settings

**Don't worry if you're not technical!** This guide assumes no prior programming experience.

## Installation Steps

### Step 1: Download the Project

If you have the project files:
```bash
cd langflow-proxy
```

If you're cloning from a repository:
```bash
git clone <repository-url>
cd langflow-proxy
```

### Step 2: Install Python Packages

Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
pip install -e .
```

This installs everything you need. Wait for it to complete (may take a minute or two).

**For Streamlit users**, also run:
```bash
pip install streamlit
```

### Step 3: Create Your Configuration File

Create a file named `.env` in the `langflow-proxy` folder.

**On Mac/Linux:**
```bash
echo "LANGFLOW_API_KEY=your-api-key-here" > .env
```

**On Windows:**
```bash
echo LANGFLOW_API_KEY=your-api-key-here > .env
```

**Or use a text editor:**
1. Open a text editor (Notepad, TextEdit, etc.)
2. Type: `LANGFLOW_API_KEY=your-api-key-here`
3. Replace `your-api-key-here` with your actual API key
4. Save as `.env` in the `langflow-proxy` folder

**Important:** Replace `your-api-key-here` with your actual Langflow API key!

## Running the Applications

You can use either (or both) of these applications:

### Option 1: FastAPI Server (For Developers)

The FastAPI server is a backend API that other applications can connect to.

#### Step 1: Configure Your Agents

Open `app.py` in a text editor and find the `AGENT_CONFIGS` section (near the end of the file):

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

**How to get your Langflow URL:**
1. Open your Langflow flow
2. Click the "API" button (usually in the top right)
3. Copy the entire URL shown
4. Paste it in the `url` field

**Example:**
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

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 3: Test It

Open your web browser and visit:

**Interactive Documentation:** http://localhost:8000/docs

Here you can:
- See all your configured agents
- Test sending messages
- View response formats

**Try sending a message:**
1. Click on your agent endpoint (e.g., `/api/customer-support`)
2. Click "Try it out"
3. Fill in:
   - `message`: "Hello!"
   - `session_id`: "test-123"
4. Click "Execute"
5. See the response!

### Option 2: Streamlit Chat Interface (For Everyone!)

The Streamlit interface provides a simple chat window - perfect for non-technical users!

#### Step 1: Run Streamlit

```bash
streamlit run streamlit_app.py
```

Your browser should automatically open to the chat interface!

If not, visit: http://localhost:8501

#### Step 2: Configure in the Interface

In the sidebar (left side), you'll see:

**Langflow Agent URL:** Paste your Langflow flow URL here
- Get this from Langflow (click API button)
- Format: `https://your-langflow.com/api/v1/run/your-flow-id`

**Langflow API Key:** Your API key will automatically load from `.env`
- You can also type it directly here
- It will be hidden for security

#### Step 3: Start Chatting!

1. Type a message in the chat box at the bottom
2. Press Enter
3. Wait for the response
4. Continue the conversation!

**That's it!** No coding required.

## Which One Should I Use?

| Use | Recommended App |
|-----|-----------------|
| Just want to chat with an agent | **Streamlit** |
| Testing an agent quickly | **Streamlit** |
| Classroom demonstration | **Streamlit** |
| Building an application | **FastAPI** |
| Connecting multiple systems | **FastAPI** |
| Need programmatic access | **FastAPI** |

**For most users, start with Streamlit!**

## Common Issues and Solutions

### Issue: "command not found: python"

**Try:** `python3` instead of `python`

Many systems use `python3` as the command name.

### Issue: "LANGFLOW_API_KEY is required"

**Solution:** 
1. Make sure you created a `.env` file
2. Check that it contains `LANGFLOW_API_KEY=your-key`
3. Replace `your-key` with your actual API key
4. The file should be in the `langflow-proxy` folder

### Issue: "Connection refused" or "Can't reach Langflow"

**Check these:**
1. Is your Langflow instance running?
2. Is the URL correct? (Check for typos)
3. Can you access the URL in your browser?
4. Is your API key valid?

**Test your Langflow URL:**
Open it in a browser - you should see something, not an error page.

### Issue: "No module named..."

**Solution:** Reinstall dependencies
```bash
pip install -e .
pip install streamlit
```

### Issue: Streamlit shows "No agents available"

**For Streamlit:**
- Make sure you entered the Langflow Agent URL in the sidebar
- Click "New Session" to refresh

**For FastAPI:**
- Check that `AGENT_CONFIGS` in `app.py` has at least one agent
- Restart the server

### Issue: "Address already in use"

**Solution:** Something else is using the port
```bash
# For FastAPI (port 8000):
# Stop other apps using port 8000, or change the port

# For Streamlit (port 8501):
streamlit run streamlit_app.py --server.port 8502
```

## Testing Your Setup

### Quick Test Checklist

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

Your `langflow-proxy` folder contains:

```
langflow-proxy/
├── app.py              ← FastAPI server (all in one file!)
├── streamlit_app.py    ← Streamlit interface (all in one file!)
├── .env                ← Your API key (you create this)
├── examples.py         ← Code examples
├── pyproject.toml      ← Dependency list
└── docs/               ← Help files (like this one)
```

**That's it!** Just two main files - super simple.

### Key Concepts

**API Key:** Like a password that proves you're allowed to use Langflow.

**Session ID:** A unique identifier for a conversation. Messages with the same session ID are treated as one conversation.

**Endpoint:** A URL path where you send messages (e.g., `/api/customer-support`).

**Timeout:** How long to wait for a response before giving up.

## Next Steps

Now that everything is running:

### Learn More

- **[Streamlit Guide](STREAMLIT_GUIDE.md)** - Detailed guide for the chat interface
- **[FastAPI Guide](FASTAPI_GUIDE.md)** - Understanding the API server
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Langflow Setup](LANGFLOW_SETUP.md)** - Creating and configuring Langflow flows

### Try These Examples

1. **Test basic chat**
   - Send simple questions
   - See how the agent responds
   - Try follow-up questions

2. **Test conversation memory**
   - Ask "What's 2 + 2?"
   - Then ask "What's that plus 3?"
   - The agent should remember it was 4

3. **Try different agents**
   - Add multiple agents to `AGENT_CONFIGS`
   - Test each one
   - Compare their responses

4. **Experiment with settings**
   - Try different timeouts
   - Use different session IDs
   - See what happens!

## Getting Help

### Debug Mode

Enable more detailed logging:

1. Edit your `.env` file
2. Add: `LOG_LEVEL=DEBUG`
3. Restart the app
4. Check the console output for details

### Checking Logs

**FastAPI:** Look at the terminal where you ran `python app.py`

**Streamlit:** Look at the terminal where you ran `streamlit run streamlit_app.py`

### Common Questions

**Q: Do I need both apps running?**  
A: No! Use just Streamlit, or just FastAPI, or both. They work independently.

**Q: Can others use my Streamlit interface?**  
A: Yes, if you share your computer's URL. But they'll need network access to your machine.

**Q: Is this secure?**  
A: This is an educational version. For production, add authentication and other security measures.

**Q: Can I customize it?**  
A: Yes! The code is simple and meant to be modified. Try changing things!

## Tips for Classroom Use

### For Instructors

1. **Pre-configure agents** for students (edit `app.py`)
2. **Create a shared `.env`** with a classroom API key
3. **Provide the Langflow URL** to students
4. **Have students test** with Streamlit first
5. **Then explore** the FastAPI code together

### For Students

1. **Start with Streamlit** - it's the easiest
2. **Read the guides** in the `docs/` folder
3. **Experiment freely** - you can't break anything!
4. **Ask questions** when you get stuck
5. **Try modifying** the code after you understand it

## Advanced Setup (Optional)

### Using Virtual Environments

For cleaner package management:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Install packages
pip install -e .
```

### Running on a Different Port

**FastAPI:**
Edit `app.py`, find the last line:
```python
uvicorn.run("app:app", port=8080)  # Changed from 8000
```

**Streamlit:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Production Deployment

For real-world use, see [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Cloud hosting
- Security measures
- Scaling considerations
- Monitoring

---

**You're all set!** Start with Streamlit and have fun chatting with your AI agents!

For questions or issues, check the other docs or ask for help.

````
