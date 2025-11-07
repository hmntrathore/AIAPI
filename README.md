# AI API Gateway

A modular, production-ready FastAPI application for interacting with multiple AI providers. Switch between Azure OpenAI and DigitalOcean AI with a single configuration change!

## 🌟 Features

- � **Multi-Provider Support** - Azure OpenAI & DigitalOcean AI (easily extensible)
- �🚀 **FastAPI Framework** - High-performance, modern Python API
- 🎯 **Easy Provider Switching** - Change providers via environment variable
- 🔧 **Highly Configurable** - All settings via environment variables
- 🐳 **Docker Support** - Containerized deployment ready
- 📝 **Custom System Prompts** - Per-request or default system prompts
- 🔒 **Secure** - Environment-based secrets, non-root Docker user
- 📊 **Interactive Docs** - Auto-generated Swagger UI & ReDoc
- ✅ **Health Monitoring** - Built-in health check endpoints
- 🎮 **Playground Ready** - Perfect for demos and testing

## 🎯 Supported Providers

### Azure OpenAI
- Enterprise-grade AI services
- GPT-4, GPT-3.5, and other Azure-hosted models
- Enterprise security and compliance

### DigitalOcean AI
- Cost-effective AI inference
- Multiple models: GPT, Claude, Llama, Mistral
- Simple pricing and setup

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd AIAPI
cp .env.example .env
```

### 2. Choose Your Provider

Edit `.env` and set your provider:

**For DigitalOcean AI:**
```env
AI_PROVIDER=digitalocean
DIGITALOCEAN_API_KEY=your-do-api-key
DIGITALOCEAN_MODEL=llama3.3-70b-instruct
```

**For Azure OpenAI:**
```env
AI_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_MODEL=your-deployment-name
```

### 3. Run the Service

**Option A: Local Development (Python)**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python start.py
```

**Option B: Docker Compose (Recommended)**

*On Linux/Mac:*
```bash
docker compose up -d
```

*On Windows with WSL:*
```powershell
# From PowerShell, run Docker in WSL
wsl -d Ubuntu -e bash -c "cd /mnt/e/Workspace/cncg/AIAPI && sudo docker-compose up -d"

# Or open WSL terminal and run:
# cd /mnt/e/Workspace/cncg/AIAPI
# sudo docker-compose up -d
```

### 4. Access the API

- 🌐 **API Base**: http://localhost:8001
- 📚 **Interactive Docs**: http://localhost:8001/docs
- 🎮 **Playground**: http://localhost:8001/docs#/
- 💚 **Health Check**: http://localhost:8001/health

## 📖 Usage Examples
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

### 💬 Chat Completion (Multi-turn conversation)

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is machine learning?"}
    ],
    "system_prompt": "You are a helpful AI teacher.",
    "temperature": 0.7
  }'
```

**Response:**
```json
{
  "response": "Machine learning is a subset of artificial intelligence...",
  "model": "llama3.3-70b-instruct",
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 150,
    "total_tokens": 175
  }
}
```

### 🎯 Simple Completion

```bash
curl -X POST http://localhost:8001/api/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a haiku about coding",
    "temperature": 0.9
  }'
```

### 💚 Health Check

```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running",
  "configuration": {
    "ai_provider": "digitalocean",
    "endpoint_configured": true,
    "api_key_configured": true,
    "model": "llama3.3-70b-instruct"
  }
}
```

### 🎮 Playground Usage

1. Open http://localhost:8001/docs
2. Click on any endpoint (e.g., `/api/chat`)
3. Click "Try it out"
4. Modify the request body
5. Click "Execute"
6. See the response instantly!

## ⚙️ Configuration

### Provider-Specific Settings

#### DigitalOcean AI Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `AI_PROVIDER` | Set to `digitalocean` | `digitalocean` |
| `DIGITALOCEAN_API_KEY` | Your DO API key | `sk-do-xxx...` |
| `DIGITALOCEAN_MODEL` | Model to use | `llama3.3-70b-instruct` |
| `DIGITALOCEAN_INFERENCE_ENDPOINT` | Endpoint URL | `https://inference.do-ai.run/v1` |

**Available Models:**
- `llama3.3-70b-instruct` - Meta's Llama 3.3 (70B parameters)
- `llama3-8b-instruct` - Meta's Llama 3 (8B parameters)
- `mistral-nemo-instruct-2407` - Mistral's Nemo model
- `openai-gpt-4o` - GPT-4 Optimized (requires higher tier)
- `anthropic-claude-3.5-haiku` - Claude 3.5 Haiku (requires higher tier)

#### Azure OpenAI Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `AI_PROVIDER` | Set to `azure` | `azure` |
| `AZURE_OPENAI_ENDPOINT` | Azure endpoint | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Azure API key | `xxxxx...` |
| `AZURE_OPENAI_MODEL` | **Deployment name** | `gpt-4` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-02-15-preview` |

### General Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_SYSTEM_PROMPT` | Default AI behavior | `You are a helpful AI assistant.` |
| `API_HOST` | Server host | `0.0.0.0` |
| `API_PORT` | Server port | `8001` |
| `CORS_ORIGINS` | Allowed origins | `*` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔄 Switching Providers

### From DigitalOcean to Azure:

1. Edit `.env`:
```env
AI_PROVIDER=azure
```

2. Restart the server:
```bash
python start.py
```

### From Azure to DigitalOcean:

1. Edit `.env`:
```env
AI_PROVIDER=digitalocean
```

2. Restart the server:


You can customize AI behavior in three ways:

**1. Global Default (in `.env`):**
```env
DEFAULT_SYSTEM_PROMPT=You are a helpful customer service agent.
```

**2. Per Request (in API call):**
```json
{
  "system_prompt": "You are a Python expert.",
  "messages": [{"role": "user", "content": "Explain decorators"}]
}
```

**3. Docker Environment:**
```yaml
environment:
  - DEFAULT_SYSTEM_PROMPT=You are a technical support specialist.
```

## 🐳 Docker Deployment

### Standard Docker (Linux/Mac)

**Build and Run:**
```bash
docker compose up -d
```

**View Logs:**
```bash
docker compose logs -f
```

**Stop Service:**
```bash
docker compose down
```

### Docker in WSL (Windows)

#### Prerequisites

1. **Install Docker in WSL Ubuntu:**
   ```bash
   # Open WSL terminal
   wsl -d Ubuntu
   
   # Update packages
   sudo apt-get update
   
   # Install Docker
   sudo apt-get install -y docker.io docker-compose
   
   # Start Docker service
   sudo service docker start
   
   # Enable Docker to start on WSL boot (optional)
   echo "sudo service docker start" >> ~/.bashrc
   ```

2. **Verify Installation:**
   ```bash
   sudo docker --version
   sudo docker-compose --version
   ```

#### Running from PowerShell

Navigate to your project directory in Windows and run commands through WSL:

**Build and Start:**
```powershell
wsl -d Ubuntu -e bash -c "cd /mnt/e/Workspace/cncg/AIAPI && sudo docker-compose up --build -d"
```

**View Logs:**
```powershell
wsl -d Ubuntu -e bash -c "cd /mnt/e/Workspace/cncg/AIAPI && sudo docker-compose logs -f"
```

**Stop Containers:**
```powershell
wsl -d Ubuntu -e bash -c "cd /mnt/e/Workspace/cncg/AIAPI && sudo docker-compose down"
```

**Rebuild After Code Changes:**
```powershell
wsl -d Ubuntu -e bash -c "cd /mnt/e/Workspace/cncg/AIAPI && sudo docker-compose down && sudo docker-compose up --build -d"
```

#### Running from WSL Terminal

Alternatively, open a WSL terminal and run commands directly:

```bash
# Navigate to project (adjust path to match your setup)
cd /mnt/e/Workspace/cncg/AIAPI

# Build and start
sudo docker-compose up --build -d

# View logs
sudo docker-compose logs -f

# Stop containers
sudo docker-compose down
```

#### WSL Path Reference

Windows paths in WSL follow this pattern:
- `C:\` → `/mnt/c/`
- `D:\` → `/mnt/d/`
- `E:\Workspace\cncg\AIAPI` → `/mnt/e/Workspace/cncg/AIAPI`

**Note:** Always use `sudo` with Docker commands in WSL unless you've configured Docker to run without sudo.

### Manual Docker Build
```bash
docker build -t ai-api-gateway .
docker run -d -p 8001:8001 --env-file .env ai-api-gateway
```

## 🏗️ Project Structure

```
AIAPI/
├── main.py              # FastAPI application & endpoints
├── config.py            # Configuration management
├── start.py             # Startup script
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
├── .env               # Environment variables (gitignored)
├── .env.example       # Environment template
└── README.md          # This file
```

## 📝 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/chat` | Multi-turn chat |
| POST | `/api/completion` | Simple completion |

### Request Parameters

**Chat & Completion:**
- `temperature` (0-2): Randomness level (default: 0.7)
- `max_tokens` (1-4000): Response length limit (default: 800)
- `top_p` (0-1): Nucleus sampling (default: 0.95)
- `system_prompt`: Custom system instruction

## 🎯 Use Cases

- **Chatbots** - Customer service, support agents
- **Content Generation** - Blog posts, product descriptions
- **Code Assistance** - Code review, documentation
- **Education** - Tutoring, Q&A systems
- **Research** - Summarization, analysis
- **Prototyping** - Quick AI integration testing

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Keep credentials secure
2. **Use environment variables** - No hardcoded secrets
3. **Restrict CORS** - Set specific origins in production
4. **Rate limiting** - Add rate limiting for production
5. **API authentication** - Add auth layer for public APIs
6. **Monitor usage** - Track token consumption



### Common Issues

**"Model not available for your subscription tier"**
- Solution: Use a different model from your tier (e.g., `llama3.3-70b-instruct` instead of `openai-gpt-4o`)

**"Invalid access token"**
- Check your API key in `.env`
- Verify you're using the correct key for your provider
- For DigitalOcean: ensure you have the API key (not secret key)

**"Port already in use"**
```bash
# Change port in .env
API_PORT=8002
```

**"Connection refused"**
- Verify endpoint URL in `.env`
- Check internet connectivity
- Ensure API credentials are valid

**"CORS errors"**
```env
# Update CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:3000,https://myapp.com
```

### WSL-Specific Issues

**"docker: command not found" in WSL**
```bash
# Install Docker in WSL
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo service docker start
```

**"Cannot connect to Docker daemon"**
```bash
# Start Docker service
sudo service docker start

# Check Docker status
sudo service docker status
```

**"Permission denied" errors**
```bash
# Always use sudo with Docker commands in WSL
sudo docker-compose up -d

# Or add user to docker group (requires logout/login)
sudo usermod -aG docker $USER
```

**"Port 8001 not accessible from Windows"**
- Ensure WSL networking is working: `wsl --shutdown` then restart WSL
- Check Windows Firewall settings
- Verify port mapping in `docker-compose.yml` is `8001:8000`

**"Changes to .env not reflected in Docker"**
```bash
# Rebuild containers to pick up environment changes
sudo docker-compose down
sudo docker-compose up --build -d
```

**"Cannot find project path in WSL"**
```bash
# Windows paths map to WSL as:
# C:\Users\... → /mnt/c/Users/...
# E:\Workspace\... → /mnt/e/Workspace/...

# Navigate using WSL path format
cd /mnt/e/Workspace/cncg/AIAPI
```

## 💻 Example Usage

### Python
```python
import requests

response = requests.post(
    "http://localhost:8001/api/chat",
    json={
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7
    }
)
print(response.json()["response"])
```

### JavaScript/Node.js
```javascript
const response = await fetch('http://localhost:8001/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    messages: [{role: 'user', content: 'Hello!'}],
    temperature: 0.7
  })
});
const data = await response.json();
console.log(data.response);
```

### cURL
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- FastAPI framework
- OpenAI Python SDK
- Azure OpenAI Service
- DigitalOcean AI Platform

---

**Made with ❤️ for developers who love AI**

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
