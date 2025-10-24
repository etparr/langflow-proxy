# Deployment Guide

This guide covers deploying the Langflow Proxy Server to production environments.

## Pre-Deployment Checklist

Before deploying to production:

- [ ] Test thoroughly in development environment
- [ ] Configure all environment variables
- [ ] Set up secure API key management
- [ ] Configure CORS appropriately
- [ ] Set up monitoring and logging
- [ ] Plan for scaling and high availability
- [ ] Configure health checks
- [ ] Set up SSL/TLS certificates
- [ ] Review security settings
- [ ] Document your deployment architecture

## Deployment Options

### Option 1: Docker Deployment

#### Build the Docker Image

Create a `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application code
COPY app ./app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and test:

```bash
# Build
docker build -t langflow-proxy:latest .

# Test locally
docker run -p 8000:8000 \
  -e LANGFLOW_API_KEY=your_key_here \
  langflow-proxy:latest
```

#### Docker Compose Setup

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  langflow-proxy:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LANGFLOW_API_KEY=${LANGFLOW_API_KEY}
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
      - HTTP_MAX_CONNECTIONS=25
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Deploy:

```bash
docker-compose up -d
```

### Option 2: Azure Deployment

#### Azure Container Apps

1. **Create Container Registry:**

```bash
# Create resource group
az group create --name langflow-proxy-rg --location eastus

# Create container registry
az acr create \
  --resource-group langflow-proxy-rg \
  --name langflowproxyacr \
  --sku Basic
```

2. **Build and Push Image:**

```bash
# Login to ACR
az acr login --name langflowproxyacr

# Build and push
docker build -t langflowproxyacr.azurecr.io/langflow-proxy:latest .
docker push langflowproxyacr.azurecr.io/langflow-proxy:latest
```

3. **Create Container App:**

```bash
# Create Container Apps environment
az containerapp env create \
  --name langflow-proxy-env \
  --resource-group langflow-proxy-rg \
  --location eastus

# Deploy container app
az containerapp create \
  --name langflow-proxy \
  --resource-group langflow-proxy-rg \
  --environment langflow-proxy-env \
  --image langflowproxyacr.azurecr.io/langflow-proxy:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    LANGFLOW_API_KEY=secretref:langflow-api-key \
    ENVIRONMENT=production \
  --min-replicas 1 \
  --max-replicas 10
```

4. **Set Secrets:**

```bash
az containerapp secret set \
  --name langflow-proxy \
  --resource-group langflow-proxy-rg \
  --secrets langflow-api-key=your_actual_key_here
```

#### Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name langflow-proxy-plan \
  --resource-group langflow-proxy-rg \
  --is-linux \
  --sku B1

# Create web app
az webapp create \
  --resource-group langflow-proxy-rg \
  --plan langflow-proxy-plan \
  --name langflow-proxy-app \
  --deployment-container-image-name langflowproxyacr.azurecr.io/langflow-proxy:latest

# Configure app settings
az webapp config appsettings set \
  --resource-group langflow-proxy-rg \
  --name langflow-proxy-app \
  --settings \
    LANGFLOW_API_KEY=your_key_here \
    ENVIRONMENT=production \
    WEBSITES_PORT=8000
```

### Option 3: AWS Deployment

#### AWS ECS with Fargate

1. **Create ECR Repository:**

```bash
aws ecr create-repository --repository-name langflow-proxy
```

2. **Build and Push:**

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t langflow-proxy .
docker tag langflow-proxy:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/langflow-proxy:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/langflow-proxy:latest
```

3. **Create ECS Task Definition:**

```json
{
  "family": "langflow-proxy",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "langflow-proxy",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/langflow-proxy:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "LANGFLOW_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:langflow-api-key"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

4. **Create ECS Service with Load Balancer**

Use AWS Console or CLI to create:
- Application Load Balancer
- Target Group
- ECS Cluster
- ECS Service

### Option 4: Google Cloud Run

```bash
# Build and submit to Cloud Build
gcloud builds submit --tag gcr.io/PROJECT-ID/langflow-proxy

# Deploy to Cloud Run
gcloud run deploy langflow-proxy \
  --image gcr.io/PROJECT-ID/langflow-proxy \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=production \
  --set-secrets LANGFLOW_API_KEY=langflow-api-key:latest \
  --min-instances 1 \
  --max-instances 10 \
  --port 8000
```

### Option 5: Kubernetes Deployment

#### Create Kubernetes Manifests

`k8s/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: langflow-proxy
```

`k8s/secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: langflow-proxy-secrets
  namespace: langflow-proxy
type: Opaque
stringData:
  LANGFLOW_API_KEY: "your_api_key_here"
```

`k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: langflow-proxy-config
  namespace: langflow-proxy
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  HTTP_MAX_CONNECTIONS: "25"
  DEFAULT_REQUEST_TIMEOUT: "90.0"
```

`k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langflow-proxy
  namespace: langflow-proxy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: langflow-proxy
  template:
    metadata:
      labels:
        app: langflow-proxy
    spec:
      containers:
      - name: langflow-proxy
        image: your-registry/langflow-proxy:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: langflow-proxy-config
        - secretRef:
            name: langflow-proxy-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

`k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: langflow-proxy
  namespace: langflow-proxy
spec:
  selector:
    app: langflow-proxy
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

`k8s/hpa.yaml` (Horizontal Pod Autoscaler):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: langflow-proxy
  namespace: langflow-proxy
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: langflow-proxy
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Deploy:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

## SSL/TLS Configuration

### Using Nginx as Reverse Proxy

`nginx.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### Using Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already set up by certbot)
sudo certbot renew --dry-run
```

## Monitoring and Logging

### Application Logging

Configure centralized logging:

```python
# In app/main.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/langflow-proxy.log',
    maxBytes=10000000,
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logging.getLogger().addHandler(handler)
```

### Health Monitoring

Set up monitoring with your preferred tool:

**Uptime Robot:**
- Monitor: `https://your-domain.com/health`
- Check interval: 5 minutes

**Datadog:**
```yaml
# datadog-agent.yaml
logs:
  - type: docker
    source: langflow-proxy
    service: langflow-proxy
```

**Prometheus:**
```python
# Add to requirements
pip install prometheus-fastapi-instrumentator

# In app/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### Error Tracking

**Sentry Integration:**

```bash
pip install sentry-sdk[fastapi]
```

```python
# In app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment=settings.ENVIRONMENT,
)
```

## Scaling Strategies

### Vertical Scaling

Increase resources per instance:

```yaml
# Kubernetes
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

### Horizontal Scaling

Add more instances:

```bash
# Docker Compose
docker-compose up --scale langflow-proxy=3

# Kubernetes (manual)
kubectl scale deployment langflow-proxy --replicas=5

# Kubernetes (auto with HPA)
# Already configured in k8s/hpa.yaml
```

### Load Balancing

Use a load balancer to distribute traffic:

- **Cloud Load Balancers:** AWS ALB, Azure Load Balancer, GCP Load Balancer
- **Nginx:** Upstream configuration
- **HAProxy:** Backend configuration

Nginx example:

```nginx
upstream langflow_proxy {
    least_conn;
    server proxy1:8000;
    server proxy2:8000;
    server proxy3:8000;
}

server {
    location / {
        proxy_pass http://langflow_proxy;
    }
}
```

## Backup and Disaster Recovery

### Configuration Backup

```bash
# Backup environment configuration
cp .env .env.backup-$(date +%Y%m%d)

# Backup agent configurations
git commit -am "Backup agent configs $(date +%Y%m%d)"
git push
```

### Database Backup

If using a database for session storage:

```bash
# PostgreSQL backup
pg_dump -U username langflow_proxy > backup.sql

# Restore
psql -U username langflow_proxy < backup.sql
```

## Security Best Practices

1. **Use Secrets Management:**
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
   - HashiCorp Vault

2. **Enable Rate Limiting:**
   ```python
   from fastapi_limiter import FastAPILimiter
   from fastapi_limiter.depends import RateLimiter
   ```

3. **Add Authentication:**
   ```python
   from fastapi.security import HTTPBearer
   security = HTTPBearer()
   ```

4. **Use HTTPS Only:**
   - Configure SSL/TLS certificates
   - Redirect HTTP to HTTPS

5. **Regular Updates:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## Performance Optimization

1. **Connection Pooling:** Already implemented
2. **HTTP/2:** Enabled by default
3. **Caching:** Add Redis for response caching
4. **CDN:** Use CloudFlare or similar for static assets
5. **Compression:** Enable gzip in reverse proxy

## Troubleshooting

### Check Logs

```bash
# Docker
docker logs -f langflow-proxy

# Kubernetes
kubectl logs -f deployment/langflow-proxy -n langflow-proxy

# Direct
tail -f logs/langflow-proxy.log
```

### Test Connectivity

```bash
# Test health endpoint
curl https://your-domain.com/health

# Test with verbose output
curl -v https://your-domain.com/api/solutions

# Check DNS
nslookup your-domain.com

# Check SSL
openssl s_client -connect your-domain.com:443
```

### Common Issues

**Issue: 502 Bad Gateway**
- Check if proxy is running
- Verify Langflow connectivity
- Check firewall rules

**Issue: High latency**
- Increase timeout settings
- Scale horizontally
- Check Langflow performance

**Issue: Connection refused**
- Verify port configuration
- Check network security groups
- Verify service is running

## Rollback Procedures

### Docker

```bash
# Rollback to previous image
docker pull your-registry/langflow-proxy:previous-tag
docker-compose down
docker-compose up -d
```

### Kubernetes

```bash
# Rollback deployment
kubectl rollout undo deployment/langflow-proxy -n langflow-proxy

# Check rollout status
kubectl rollout status deployment/langflow-proxy -n langflow-proxy
```

### Cloud Platforms

Use platform-specific rollback commands or console UI.

## Next Steps

- Set up monitoring and alerting
- Configure automated backups
- Implement CI/CD pipeline
- Review [Configuration Guide](CONFIGURATION.md) for tuning
- Check [API Reference](API_REFERENCE.md) for usage
