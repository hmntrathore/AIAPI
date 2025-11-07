"""
Startup script - loads configuration from .env file
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "Not configured")
    model = os.getenv("AZURE_OPENAI_MODEL", "Not configured")
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8001"))
    
    print("🚀 Starting Azure OpenAI API...")
    print(f"📍 Endpoint: {endpoint}")
    print(f"🤖 Model: {model}")
    print(f"🌐 Server: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"💚 Health: http://{host}:{port}/health")
    print("\n⚙️  All configuration loaded from .env file")
    print("Press CTRL+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level="info"
    )
