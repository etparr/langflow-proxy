# Langflow Setup Guide  
This guide covers how to set up and deploy a Langflow instance for use with the proxy server.

## What is Langflow?

Langflow is an open-source UI for building and deploying LangChain-style flows (visual workflows of LLMs, tools, agents, etc.). It provides a drag-and-drop interface for designing agent workflows which you can then deploy as an API or embed in an application.

[Langflow Documentation](https://docs.langflow.org)

It supports major LLMs, vector stores, and agent components, and you can extend it with custom components.

[Langflow GitHub Repository](https://github.com/langflow-ai/langflow)

## Deployment Options

You can deploy Langflow in several ways (choose based on dev vs prod, scaling, maintenance):

1. Docker (Recommended for development)
2. Cloud platforms (Azure, AWS, GCP)
3. Kubernetes (Production deployments)  

---

## Option 1: Docker Deployment (Quick Start)  

### Prerequisites  
- Docker installed  
- Docker Compose (optional but recommended)  
- Preferably use a dedicated directory to isolate your flows + config  

### Basic Docker Setup  
Create a directory structure:  
\`\`\`bash
mkdir langflow‑deployment
cd langflow‑deployment
\`\`\`

Create a `docker.env` file with environment variables:  
\`\`\`env
LANGFLOW_AUTO_LOGIN=False
LANGFLOW_SAVE_DB_IN_CONFIG_DIR=True
LANGFLOW_BASE_URL=http://0.0.0.0:7860
OPENAI_API_KEY=your‑openai‑key‑here
\`\`\`

Create a `Dockerfile`:  
\`\`\`dockerfile
FROM langflowai/langflow:latest

RUN mkdir /app/flows
RUN mkdir /app/langflow-config-dir
WORKDIR /app

COPY flows /app/flows
COPY langflow-config-dir /app/langflow-config-dir
COPY docker.env /app/.env

ENV PYTHONPATH=/app
ENV LANGFLOW_LOAD_FLOWS_PATH=/app/flows
ENV LANGFLOW_CONFIG_DIR=/app/langflow-config-dir
ENV LANGFLOW_LOG_ENV=container

EXPOSE 7860
CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "7860"]
```

### Basic Docker Setup

Create a directory structure:

```bash
mkdir langflow-deployment
cd langflow-deployment
```

Create a `docker.env` file with environment variables:

```env
LANGFLOW_AUTO_LOGIN=False
LANGFLOW_SAVE_DB_IN_CONFIG_DIR=True
LANGFLOW_BASE_URL=http://0.0.0.0:7860
OPENAI_API_KEY=your-openai-key-here
```

Create a `Dockerfile`:

```dockerfile
FROM langflowai/langflow:latest

RUN mkdir /app/flows
RUN mkdir /app/langflow-config-dir
WORKDIR /app

COPY flows /app/flows
COPY langflow-config-dir /app/langflow-config-dir
COPY docker.env /app/.env

ENV PYTHONPATH=/app
ENV LANGFLOW_LOAD_FLOWS_PATH=/app/flows
ENV LANGFLOW_CONFIG_DIR=/app/langflow-config-dir
ENV LANGFLOW_LOG_ENV=container

EXPOSE 7860
CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "7860"]
```

Build & run:

```bash
docker build -t my-langflow:latest .
docker run -p 7860:7860 my-langflow:latest
```

Then access at `http://localhost:7860`.

### Docker Compose Setup
\`\`\`

Build & run:  
\`\`\`bash
docker build -t my‑langflow:latest .
docker run -p 7860:7860 my‑langflow:latest
\`\`\`

Then access → `http://localhost:7860`.

### Docker Compose Setup  
Create `docker-compose.yml`:  
\`\`\`yaml
version: '3.8'

services:
  langflow:
    image: langflowai/langflow:latest
    ports:
      - "7860:7860"
    environment:
      - LANGFLOW_AUTO_LOGIN=False
      - LANGFLOW_SAVE_DB_IN_CONFIG_DIR=True
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./flows:/app/flows
      - ./langflow-config-dir:/app/langflow-config-dir
    command: langflow run --host 0.0.0.0 --port 7860
```

Then:

```bash
docker-compose up -d
```

---
\`\`\`
Then:
\`\`\`bash
docker-compose up -d
\`\`\`

---

## Option 2: Cloud Platform Deployment  

### Azure Container Apps  
\`\`\`bash
docker build -t langflow:latest .
az acr login --name <your-registry>
docker tag langflow:latest <your-registry>.azurecr.io/langflow:latest
docker push <your-registry>.azurecr.io/langflow:latest
az containerapp create   --name langflow   --resource-group <your-resource-group>   --image <your-registry>.azurecr.io/langflow:latest   --target-port 7860   --ingress external   --environment <your-environment>
\`\`\`

### AWS ECS  
1. Create ECR repo and push your image  
2. Create ECS Task Definition  
3. Create ECS Service + Load Balancer  
[Amazon ECS Documentation](https://docs.aws.amazon.com/ecs/)

### Google Cloud Run  
\`\`\`bash
gcloud builds submit --tag gcr.io/PROJECT‑ID/langflow
gcloud run deploy langflow   --image gcr.io/PROJECT‑ID/langflow   --platform managed   --region us-central1   --allow-unauthenticated
\`\`\`

---

## Option 3: Kubernetes Deployment  

`langflow-deployment.yaml`:  
\`\`\`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langflow
spec:
  replicas: 2
  selector:
    matchLabels:
      app: langflow
  template:
    metadata:
      labels:
        app: langflow
    spec:
      containers:
      - name: langflow
        image: your-registry/langflow:latest
        ports:
        - containerPort: 7860
        env:
        - name: LANGFLOW_AUTO_LOGIN
          value: "False"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: langflow-secrets
              key: openai-api-key
---
apiVersion: v1
kind: Service
metadata:
  name: langflow
spec:
  selector:
    app: langflow
  ports:
  - port: 80
    targetPort: 7860
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f langflow-deployment.yaml
```
\`\`\`

Deploy:  
\`\`\`bash
kubectl apply -f langflow-deployment.yaml
\`\`\`

---

## Creating and Exporting Flows

1. Access your Langflow UI
2. Create a new flow using the visual editor
3. Add components (LLMs, prompts, tools, etc.)
4. Connect components into a workflow
5. Test your flow in the Playground

[Langflow Quickstart Guide](https://docs.langflow.org/get-started-quickstart)

### Exporting Flows

Click "Export" then "Download JSON" and save in `flows/` directory.

API Endpoint format:

```
https://your-langflow.com/api/v1/run/<flow-id>
```

---

## Configuring API Keys

Generate an API key via Settings > API Keys > "Generate New Key".
Copy it immediately and store securely.

Use in proxy's `.env`:

```env
LANGFLOW_API_KEY=lf-your-api-key-here
```

---

## Security Best Practices

- Always use HTTPS in production
- Store keys in environment variables or secret managers
- Enable authentication in Langflow
- Restrict access with network rules
- Rotate API keys regularly
- Monitor logs

[Security Documentation](https://docs.langflow.org)

---

## Database Configuration

### Default: SQLite

Langflow uses SQLite for development by default.

### PostgreSQL Setup (Production)

```env
LANGFLOW_DATABASE_URL=postgresql://user:password@host:5432/langflow
```

In Docker Compose:

```yaml
environment:
  - LANGFLOW_DATABASE_URL=postgresql://user:password@postgres:5432/langflow
```

---

## Environment Variables Reference

```env
LANGFLOW_AUTO_LOGIN=False
LANGFLOW_SAVE_DB_IN_CONFIG_DIR=True
LANGFLOW_DATABASE_URL=sqlite:///./langflow.db
LANGFLOW_BASE_URL=http://0.0.0.0:7860
LANGFLOW_HOST=0.0.0.0
LANGFLOW_PORT=7860
LANGFLOW_COMPONENTS_PATH=/app/components
LANGFLOW_LOAD_FLOWS_PATH=/app/flows
LANGFLOW_LOG_ENV=container
LANGFLOW_LOG_LEVEL=INFO
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key
```

---

## Testing Your Langflow Instance

### Using curl

```bash
curl https://your-langflow-instance.com/health

curl -X POST https://your-langflow-instance.com/api/v1/run/FLOW_ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{
    "input_value": "Test message",
    "input_type": "chat",
    "output_type": "chat",
    "session_id": "test-session"
  }'
```

### Using Python

```python
import httpx

async def test_langflow():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://your-langflow-instance.com/api/v1/run/FLOW_ID",
            json={
                "input_value": "Test message",
                "input_type": "chat",
                "output_type": "chat",
                "session_id": "test-session"
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": "your-api-key"
            }
        )
        print(response.json())
```

---

## Monitoring and Logging

Set log level:

```env
LANGFLOW_LOG_LEVEL=DEBUG
```

View logs:

- **Docker**: `docker logs -f <container-id>`
- **Kubernetes**: `kubectl logs -f deployment/langflow`  

---

## Troubleshooting

### Can't Connect

- Check container or pod is running (`docker ps`, `kubectl get pods`)
- Verify port 7860 is open and mapped
- Confirm proxy to Langflow network connectivity

### Authentication Failures

- Ensure API key and `x-api-key` header are correct
- Check authentication is enabled in Langflow

### Flows Not Loading

- Validate JSONs in `/app/flows`
- Confirm `LANGFLOW_LOAD_FLOWS_PATH` is set correctly

---

## Additional Resources

- [Official Langflow Documentation](https://docs.langflow.org)
- [Langflow GitHub](https://github.com/langflow-ai/langflow)
- [LangChain Documentation](https://python.langchain.com)
- [Docker Documentation](https://docs.docker.com)
- [Kubernetes Documentation](https://kubernetes.io/docs)

---

## Next Steps

After setup:

1. Return to the [Getting Started Guide](GETTING_STARTED.md)
2. Configure proxy to Langflow instance
3. Review [FastAPI Guide](FASTAPI_GUIDE.md)
4. Deploy to production with [Deployment Guide](DEPLOYMENT.md)
