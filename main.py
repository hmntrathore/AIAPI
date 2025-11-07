"""
FastAPI application for Azure OpenAI integration
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from openai import AzureOpenAI
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI API",
    description="Modular FastAPI application for calling AI services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Azure OpenAI client
def get_openai_client():
    """Initialize and return Azure OpenAI client"""
    try:
        client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize AI service"
        )


# Request/Response models
class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (system, user, assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    messages: List[Message] = Field(
        ..., 
        description="List of messages in the conversation"
    )
    system_prompt: Optional[str] = Field(
        None,
        description="Optional system prompt to override default"
    )
    temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0-2)"
    )
    max_tokens: Optional[int] = Field(
        default=800,
        ge=1,
        le=4000,
        description="Maximum tokens to generate"
    )
    top_p: Optional[float] = Field(
        default=0.95,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling parameter"
    )


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI generated response")
    model: str = Field(..., description="Model used for generation")
    usage: Dict[str, Any] = Field(..., description="Token usage information")


class CompletionRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to complete")
    system_prompt: Optional[str] = Field(
        None,
        description="Optional system prompt to override default"
    )
    temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0-2)"
    )
    max_tokens: Optional[int] = Field(
        default=800,
        ge=1,
        le=4000,
        description="Maximum tokens to generate"
    )


class HealthResponse(BaseModel):
    status: str
    message: str
    configuration: Dict[str, Any]


# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Azure OpenAI API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Service is running",
        configuration={
            "endpoint_configured": bool(settings.AZURE_OPENAI_ENDPOINT),
            "api_key_configured": bool(settings.AZURE_OPENAI_API_KEY),
            "model": settings.AZURE_OPENAI_MODEL,
            "api_version": settings.AZURE_OPENAI_API_VERSION
        }
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """
    Send a chat completion request to Azure OpenAI
    
    Args:
        request: ChatRequest containing messages and optional parameters
        
    Returns:
        ChatResponse with AI generated response
    """
    try:
        client = get_openai_client()
        
        # Prepare messages
        messages = []
        
        # Add system prompt (use custom or default)
        system_prompt = request.system_prompt or settings.DEFAULT_SYSTEM_PROMPT
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation messages
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Call Azure OpenAI
        logger.info(f"Calling Azure OpenAI with {len(messages)} messages")
        response = client.chat.completions.create(
            model=settings.AZURE_OPENAI_MODEL,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p
        )
        
        # Extract response
        ai_response = response.choices[0].message.content
        
        return ChatResponse(
            response=ai_response,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
        
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )


@app.post("/api/completion", response_model=ChatResponse)
async def simple_completion(request: CompletionRequest):
    """
    Send a simple completion request to Azure OpenAI
    
    Args:
        request: CompletionRequest containing prompt and optional parameters
        
    Returns:
        ChatResponse with AI generated response
    """
    try:
        client = get_openai_client()
        
        # Prepare messages for chat completion format
        messages = []
        
        # Add system prompt if provided
        system_prompt = request.system_prompt or settings.DEFAULT_SYSTEM_PROMPT
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add user prompt
        messages.append({"role": "user", "content": request.prompt})
        
        # Call Azure OpenAI
        logger.info(f"Calling Azure OpenAI for completion")
        response = client.chat.completions.create(
            model=settings.AZURE_OPENAI_MODEL,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Extract response
        ai_response = response.choices[0].message.content
        
        return ChatResponse(
            response=ai_response,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )
        
    except Exception as e:
        logger.error(f"Error in completion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
