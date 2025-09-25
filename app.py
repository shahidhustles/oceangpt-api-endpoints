from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import Optional

app = FastAPI(
    title="OceanGPT API",
    description="Frontend API for OceanGPT - Marine AI Assistant",
    version="1.0.0",
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class QueryRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 200
    temperature: Optional[float] = 0.7


class QueryResponse(BaseModel):
    response: str
    status: str = "success"


class ErrorResponse(BaseModel):
    error: str
    status: str = "error"


# Your Modal endpoint URL
MODAL_ENDPOINT_URL = "https://shahidhustles--oceangpt-7b-app-api-endpoint.modal.run"


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "OceanGPT API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {"status": "healthy", "service": "OceanGPT Frontend API", "version": "1.0.0"}


@app.post("/query", response_model=QueryResponse)
async def query_oceangpt(request: QueryRequest):
    """
    Send a query to OceanGPT model

    - **prompt**: The question or prompt to send to the AI model
    - **max_tokens**: Maximum number of tokens to generate (optional, default: 200)
    - **temperature**: Sampling temperature for creativity (optional, default: 0.7)
    """
    try:
        # Prepare the payload for Modal endpoint
        modal_payload = {"prompt": request.prompt}

        # Make request to Modal endpoint (5 minute timeout for cold starts)
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                MODAL_ENDPOINT_URL,
                json=modal_payload,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                result = response.json()
                return QueryResponse(response=result.get("response", ""))
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Modal endpoint error: {response.text}",
                )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request timeout - the AI model is initializing (first request can take 2-3 minutes). Please try again in a moment.",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Failed to connect to AI model: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/chat", response_model=QueryResponse)
async def chat_with_oceangpt(request: QueryRequest):
    """
    Alternative endpoint for chat-style interactions
    Formats the prompt with a more conversational context
    """
    try:
        # Add conversational context to the prompt
        formatted_prompt = f"You are OceanGPT, a marine science expert. Please answer the following question about marine science or ocean-related topics:\n\nQuestion: {request.prompt}\n\nAnswer:"

        modal_payload = {"prompt": formatted_prompt}

        # Make request to Modal endpoint (5 minute timeout for cold starts)
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                MODAL_ENDPOINT_URL,
                json=modal_payload,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                result = response.json()
                # Clean up the response by removing the original prompt if it's included
                ai_response = result.get("response", "")
                if formatted_prompt in ai_response:
                    ai_response = ai_response.replace(formatted_prompt, "").strip()

                return QueryResponse(response=ai_response)
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Modal endpoint error: {response.text}",
                )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request timeout - the AI model is initializing (first request can take 2-3 minutes). Please try again in a moment.",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Failed to connect to AI model: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
