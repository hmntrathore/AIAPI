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
    provider = os.getenv("AI_PROVIDER", "azure").upper()
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8001"))
    
    print("🚀 Starting AI API Service...")
    print(f"🔧 Provider: {provider}")
    
    # Display provider-specific info
    if provider == "DIGITALOCEAN":
        endpoint = os.getenv("DIGITALOCEAN_INFERENCE_ENDPOINT", "Not configured")
        model = os.getenv("DIGITALOCEAN_MODEL", "Not configured")
        print(f"📍 Endpoint: {endpoint}")
        print(f"🤖 Model: {model}")
    else:  # Azure
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "Not configured")
        model = os.getenv("AZURE_OPENAI_MODEL", "Not configured")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "Not configured")
        print(f"📍 Endpoint: {endpoint}")
        print(f"🤖 Model: {model}")
        print(f"📋 API Version: {api_version}")
    
    print(f"\n🌐 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🎮 Playground: http://{host}:{port}/docs#/")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print("\n⚙️  Configuration loaded from .env file")
    print("💡 Tip: Change AI_PROVIDER in .env to switch between 'azure' and 'digitalocean'")
    print("Press CTRL+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level="info"
    )
