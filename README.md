````markdown
# Langflow Proxy Server

A simple educational project demonstrating how to interact with Langflow agents. This repository contains two applications:

1. **FastAPI Proxy Server** (`app.py`) - A backend API that acts as an intermediary to Langflow
2. **Streamlit Chat Interface** (`streamlit_app.py`) - A user-friendly chat interface

Both applications are designed for **classroom use** with non-technical professionals in mind.

## Overview

### What This Project Does

This project helps you:

- **Connect to AI agents** built in Langflow
- **Send messages** to these agents and get responses
- **Maintain conversation context** across multiple messages
- **Manage multiple agents** from a single interface

### Two Ways to Use It

1. **FastAPI App**: A backend server that other applications can connect to
2. **Streamlit App**: A ready-to-use chat interface (no programming required!)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Langflow instance with deployed flows
- Your Langflow API key

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd langflow-proxy
```

2. Install dependencies:
```bash
pip install -e .
```

3. Create a `.env` file with your Langflow API key:
```bash
echo "LANGFLOW_API_KEY=your-api-key-here" > .env
```

### Running the FastAPI Server

```bash
python app.py
```

The server will start at `http://localhost:8000`. Visit `http://localhost:8000/docs` to see the interactive API documentation.

### Running the Streamlit Interface

```bash
streamlit run streamlit_app.py
```

The chat interface will open in your browser automatically!

## Documentation

### Quick Start
- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Complete setup instructions for beginners

### For Users
- **[Streamlit Guide](docs/STREAMLIT_GUIDE.md)** - How to use the chat interface (no coding required!)

### For Developers  
- **[FastAPI Guide](docs/FASTAPI_GUIDE.md)** - Understanding how the API server works

### Setup & Deployment
- **[Langflow Setup](docs/LANGFLOW_SETUP.md)** - Setting up your Langflow instance
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploying the applications to production

### Need Help?
Start with the **Getting Started Guide** if this is your first time. It walks you through everything step by step.

## Project Structure

This is a **simplified, educational project** with just a few files:

```
langflow-proxy/
├── app.py                  # FastAPI server (single file)
├── streamlit_app.py        # Streamlit chat interface (single file)
├── examples.py             # Code examples
├── pyproject.toml          # Dependencies
├── .env                    # Your API key (create this)
├── docs/                   # Documentation
└── README.md               # This file
```

**Note**: Everything is intentionally kept simple for learning purposes!

## How It Works

### FastAPI Server (app.py)

The FastAPI server acts as a **middleman** between your applications and Langflow:

1. **Receives requests** from your applications (or the Streamlit interface)
2. **Forwards messages** to the appropriate Langflow agent
3. **Returns responses** in a simple format

**Key Features:**
- Multiple agent support (add as many agents as you want)
- Session management (conversations remember context)
- Error handling (graceful failures)
- Automatic API documentation

### Streamlit Interface (streamlit_app.py)

The Streamlit app provides a **chat interface** anyone can use:

1. **Select an agent** from the dropdown
2. **Type messages** in the chat box
3. **See responses** in real-time
4. **Maintain conversations** automatically

**Perfect for:**
- Testing your agents
- Demonstrating AI capabilities
- Classroom exercises
- Non-technical users

## Configuration

### Adding Your Langflow Agents

Edit `app.py` and find the `AGENT_CONFIGS` section (near the bottom):

```python
AGENT_CONFIGS = [
    {
        "path_prefix": "/my-first-agent",
        "url": "https://your-langflow-url.com/api/v1/run/your-flow-id",
        "summary": "My First Agent",
        "timeout": 30.0
    },
    # Add more agents here
]
```

**To get your Langflow URL:**
1. Open your Langflow flow
2. Click the "API" button
3. Copy the endpoint URL
4. Paste it in the `url` field above

### Environment Variables

Create a `.env` file:

```env
# Required
LANGFLOW_API_KEY=your-api-key-here

# Optional
ENVIRONMENT=development
LOG_LEVEL=INFO
DEFAULT_REQUEST_TIMEOUT=30.0
```

## Using the Applications

### Testing the FastAPI Server

Visit `http://localhost:8000/docs` to see interactive documentation where you can:
- See all available agents
- Test sending messages
- View response formats

Or use curl:
```bash
curl -X POST http://localhost:8000/api/my-first-agent \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "session_id": "test-123"}'
```

### Using the Streamlit Interface

1. Run `streamlit run streamlit_app.py`
2. Your browser will open automatically
3. Select an agent from the dropdown
4. Start chatting!

**Tips:**
- Click "New Session" to start a fresh conversation
- Use "Clear Chat" to reset the display
- The session ID maintains conversation context

## Common Questions

**Q: Do I need to know programming to use this?**  
A: No! If you just want to chat with agents, use the Streamlit interface. Just run it and start chatting.

**Q: What's a session ID?**  
A: It's like a conversation ID. Messages with the same session ID are treated as part of the same conversation, so the agent remembers context.

**Q: Can I add multiple agents?**  
A: Yes! Just add more entries to the `AGENT_CONFIGS` list in `app.py`.

**Q: Do I need both FastAPI and Streamlit?**  
A: Not necessarily. The Streamlit app can work on its own if you configure it to connect directly to Langflow. However, the FastAPI server is useful if you want to build your own applications.

**Q: Is this ready for production?**  
A: No, this is an educational example. For production, you'd need to add authentication, rate limiting, proper error handling, and security measures.

## Troubleshooting

**"LANGFLOW_API_KEY is required"**
- Make sure you created a `.env` file with your API key

**"Connection refused"**
- Check that your Langflow instance is running
- Verify the URLs in `AGENT_CONFIGS` are correct

**"No agents available"**
- Make sure you added agents to `AGENT_CONFIGS` in `app.py`
- Restart the server after making changes

**Streamlit won't start**
- Install Streamlit: `pip install streamlit`
- Make sure the FastAPI server is running first

## Learning More

This project demonstrates several important concepts:

- **API Design**: How to structure a REST API
- **HTTP Communication**: Making requests between services
- **Error Handling**: Gracefully managing failures
- **Configuration**: Using environment variables
- **Session Management**: Maintaining state across requests
- **User Interfaces**: Building chat applications

For more details, check out the documentation in the `docs/` folder!

## Educational Purpose

This repository is designed for **classroom use** to teach:

- How AI agents work
- Basic API architecture
- Building chat interfaces
- Connecting different services together

It prioritizes **clarity and simplicity** over production-readiness.

## License

[Your License Here]

## Support

For issues or questions, please [open an issue](link-to-issues) or contact [your contact info].

---

**Happy Learning!**

````
