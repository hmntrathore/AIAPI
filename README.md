# Azure OpenAI FastAPI Service

A modular, production-ready FastAPI application for interacting with Azure OpenAI services. This API provides easy-to-use endpoints for chat completions and text generation, with full Docker support and configurable settings.

## Features

- 🚀 **FastAPI Framework** - High-performance, modern Python API
- 🤖 **Azure OpenAI Integration** - Seamless connection to Azure OpenAI services
- 🔧 **Highly Configurable** - Easy configuration via environment variables
- 🐳 **Docker Support** - Containerized deployment with Docker and Docker Compose
- 📝 **Custom System Prompts** - Configurable system prompts at both deployment and request level
- 🔒 **Secure** - Non-root Docker user, environment-based secrets
- 📊 **Interactive API Docs** - Auto-generated Swagger UI documentation
- ✅ **Health Checks** - Built-in health monitoring endpoints

## Prerequisites

- Python 3.11+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- Azure OpenAI Service account with API key and endpoint

## Quick Start with Docker (Recommended)

### 1. Clone and Navigate to Project

```bash
cd AIAPI
```

### 2. Configure Environment Variables

Copy the example environment file and update with your Azure OpenAI credentials:

```bash
cp .env.example .env
```

Edit `.env` file with your values:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_MODEL=your-deployment-name
```

**Important:** `AZURE_OPENAI_MODEL` should be your **deployment name** (found in Azure OpenAI Studio > Deployments), not the model name.

### 3. Build and Run with Docker Compose

```bash
docker compose up -d
```

The API will be available at `http://localhost:8001`

### 4. Access API Documentation

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Local Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Update the `.env` file with your Azure OpenAI credentials.

### 4. Run the Application

```bash
python start.py
```

Or directly with uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001
```

The API will be available at `http://localhost:8001`

## API Endpoints

### Health Check

**GET** `/health`

Returns the health status and configuration of the service.

```bash
curl http://localhost:8000/health
```

### Chat Completion

**POST** `/api/chat`

Send a multi-turn conversation to the AI.

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is the capital of France?"
    }
  ],
  "system_prompt": "You are a geography expert.",
  "temperature": 0.7,
  "max_tokens": 800,
  "top_p": 0.95
}
```

**Example with cURL:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Explain quantum computing in simple terms"
      }
    ],
    "system_prompt": "You are a helpful science teacher.",
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "response": "The capital of France is Paris.",
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 8,
    "total_tokens": 23
  }
}
```

### Simple Completion

**POST** `/api/completion`

Send a single prompt to the AI.

**Request Body:**
```json
{
  "prompt": "Write a short poem about the ocean",
  "system_prompt": "You are a creative poet.",
  "temperature": 0.9,
  "max_tokens": 500
}
```

**Example with cURL:**
```bash
curl -X POST http://localhost:8000/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "List 5 benefits of exercise",
    "temperature": 0.5
  }'
```

## Configuration Options

All configuration is managed through environment variables. You can set these in:
- `.env` file (for local development)
- Docker Compose environment section
- Container environment variables

### Available Configuration Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | - | ✅ Yes |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | - | ✅ Yes |
| `AZURE_OPENAI_MODEL` | **Deployment name** (not model name) from Azure | - | ✅ Yes |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2024-02-15-preview` | No |
| `DEFAULT_SYSTEM_PROMPT` | Default system prompt for all requests | `You are a helpful AI assistant.` | No |
| `API_HOST` | Host to bind the server | `0.0.0.0` | No |
| `API_PORT` | Port for the API server | `8001` | No |
| `CORS_ORIGINS` | Allowed CORS origins | `*` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Changing System Prompts

You can customize the AI's behavior in three ways:

1. **Global Default** - Set in `.env` file:
   ```env
   DEFAULT_SYSTEM_PROMPT=You are a helpful customer service agent.
   ```

2. **Per Request** - Override in API request:
   ```json
   {
     "system_prompt": "You are a Python programming expert.",
     "messages": [...]
   }
   ```

3. **Docker Environment** - Set in `docker-compose.yml`:
   ```yaml
   environment:
     - DEFAULT_SYSTEM_PROMPT=You are a technical support specialist.
   ```

## Docker Commands

### Build Image

```bash
docker build -t azure-openai-api .
```

### Run Container

```bash
docker run -d \
  --name azure-openai-api \
  -p 8000:8000 \
  --env-file .env \
  azure-openai-api
```

### View Logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f azure-openai-api
```

### Stop Service

```bash
# Docker Compose
docker-compose down

# Docker
docker stop azure-openai-api
```

### Restart Service

```bash
# Docker Compose
docker-compose restart

# Docker
docker restart azure-openai-api
```

## Example Usage with Python

```python
import requests

url = "http://localhost:8000/api/chat"

payload = {
    "messages": [
        {
            "role": "user",
            "content": "What are the benefits of cloud computing?"
        }
    ],
    "system_prompt": "You are a cloud architecture expert.",
    "temperature": 0.7,
    "max_tokens": 500
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Response: {result['response']}")
print(f"Tokens used: {result['usage']['total_tokens']}")
```

## Example Usage with JavaScript/Node.js

```javascript
const axios = require('axios');

const url = 'http://localhost:8000/api/completion';

const payload = {
  prompt: 'Explain microservices architecture',
  system_prompt: 'You are a software architecture expert.',
  temperature: 0.6,
  max_tokens: 600
};

axios.post(url, payload)
  .then(response => {
    console.log('Response:', response.data.response);
    console.log('Model:', response.data.model);
    console.log('Tokens:', response.data.usage.total_tokens);
  })
  .catch(error => {
    console.error('Error:', error.response?.data || error.message);
  });
```

## Production Deployment Considerations

### Security

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use strong API keys** - Rotate regularly
3. **Restrict CORS origins** - Don't use `*` in production
4. **Use HTTPS** - Deploy behind a reverse proxy (nginx, Traefik)
5. **Network isolation** - Use Docker networks appropriately

### Scaling

1. **Horizontal Scaling** - Run multiple container instances
2. **Load Balancing** - Use nginx or cloud load balancers
3. **Rate Limiting** - Implement API rate limiting
4. **Caching** - Add Redis for response caching

### Monitoring

1. **Health Checks** - Use the `/health` endpoint
2. **Logging** - Configure centralized logging
3. **Metrics** - Add Prometheus/Grafana for monitoring
4. **Alerts** - Set up alerts for errors and downtime

## Troubleshooting

### Container won't start

Check logs:
```bash
docker-compose logs azure-openai-api
```

### Connection refused errors

Ensure environment variables are set correctly:
```bash
docker-compose exec azure-openai-api env | grep AZURE
```

### API returns 500 errors

1. Verify Azure OpenAI endpoint and API key
2. Check model deployment name matches `AZURE_OPENAI_MODEL`
3. Ensure API version is compatible

### Import errors in local development

Make sure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

## Project Structure

```
AIAPI/
├── main.py                 # FastAPI application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Example environment variables
└── README.md            # This file
```

## License

This project is provided as-is for educational and commercial use.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Azure OpenAI documentation
3. Check FastAPI documentation

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All endpoints are documented
- Environment variables are added to `.env.example`
- README is updated with new features
