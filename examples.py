"""Simple usage examples for the Langflow Proxy."""

import asyncio
import httpx


class LangflowProxyClient:
    """Simple client for interacting with the Langflow Proxy."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    

    
    async def list_agents(self) -> list[dict]:
        """Get list of available agents."""
        response = await self.client.get(f"{self.base_url}/api/solutions")
        response.raise_for_status()
        return response.json()
    
    async def chat(self, agent: str, message: str, session_id: str) -> str:
        """Send a message to an agent."""
        response = await self.client.post(
            f"{self.base_url}/api/{agent}",
            json={
                "message": message,
                "session_id": session_id
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["data"]
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def basic_example():
    """Example: Basic usage of the proxy."""
    print("=== Basic Usage Example ===\n")
    
    client = LangflowProxyClient()
    
    try:
        # Check health
        health = await client.health_check()
        print(f"Proxy status: {health['status']}")
        
        # List available agents
        agents = await client.list_agents()
        print(f"\nAvailable agents: {len(agents)}")
        for agent in agents:
            print(f"  - {agent['solution']} ({agent['url']})")
        
        # Chat with an agent (if any are available)
        if agents:
            agent_path = agents[0]['url'].lstrip('/')
            print(f"\n=== Chatting with {agents[0]['solution']} ===")
            
            response = await client.chat(
                agent=agent_path,
                message="Hello, can you help me?",
                session_id="example-session-001"
            )
            print(f"Agent response: {response}")
        else:
            print("\nNo agents configured. Update AGENT_CONFIGS in app/main.py")
    
    finally:
        await client.close()


async def conversation_example():
    """Example: Multi-turn conversation with context."""
    print("\n=== Multi-turn Conversation Example ===\n")
    
    client = LangflowProxyClient()
    
    try:
        agents = await client.list_agents()
        if not agents:
            print("No agents available")
            return
        
        agent_path = agents[0]['url'].lstrip('/')
        session_id = "conversation-example-001"
        
        # Simulate a conversation
        messages = [
            "Hello, I need help with something.",
            "Can you tell me about your capabilities?",
            "Thank you for the information."
        ]
        
        print(f"Starting conversation with {agents[0]['solution']}")
        print(f"Session ID: {session_id}\n")
        
        for i, message in enumerate(messages, 1):
            print(f"User (turn {i}): {message}")
            response = await client.chat(
                agent=agent_path,
                message=message,
                session_id=session_id
            )
            print(f"Agent: {response}\n")
            
            # Small delay between messages
            await asyncio.sleep(1)
    
    finally:
        await client.close()


def curl_examples():
    """Example: Equivalent curl commands."""
    print("\n=== Equivalent curl Commands ===\n")
    
    commands = [
        ("Health Check", 
         'curl http://localhost:8000/health'),
        
        ("List Agents",
         'curl http://localhost:8000/api/solutions'),
        
        ("Chat with Agent",
         '''curl -X POST http://localhost:8000/api/example-agent \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Hello, agent!",
    "session_id": "curl-example-001"
  }' '''),
    ]
    
    for title, command in commands:
        print(f"{title}:")
        print(f"{command}\n")


async def main():
    """Run examples."""
    print("=" * 50)
    print("Langflow Proxy - Usage Examples")
    print("=" * 50)
    
    await basic_example()
    await conversation_example()
    curl_examples()
    
    print("=" * 50)
    print("Examples completed!")
    print("Note: Make sure your proxy server is running on localhost:8000")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
