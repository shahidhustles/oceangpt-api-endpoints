# 🌊 OceanGPT Server

A powerful marine science AI assistant built with **OceanGPT-7B** model, deployed on Modal for scalable GPU inference and wrapped with a FastAPI server for easy frontend integration.

## 🏗️ Architecture Overview

```
Frontend (React/JS) → FastAPI Server (app.py) → Modal GPU Deployment (oceangpt_modal.py) → OceanGPT-7B Model
```

- **OceanGPT-7B Model**: Specialized LLM for marine science questions
- **Modal Deployment**: GPU-powered serverless inference
- **FastAPI Wrapper**: RESTful API for frontend integration
- **CORS Enabled**: Ready for web applications

## 📁 Project Structure

```
oceanGPT-server/
├── oceangpt_modal.py      # Modal deployment with GPU inference
├── app.py                 # FastAPI server for frontend API
├── requirements.txt       # Python dependencies
└── README.md             # This documentation
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to project
cd oceanGPT-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Deploy to Modal

```bash
# Deploy the GPU-powered inference function
modal deploy oceangpt_modal.py
```

**Note**: Make sure you have Modal CLI installed and authenticated.

### 3. Start FastAPI Server

```bash
# Start the API server
python app.py
# OR
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

The server will be available at: `http://localhost:8001`

## 🔧 API Endpoints

### Health Check

```http
GET /
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "OceanGPT Frontend API",
  "version": "1.0.0"
}
```

### Query Endpoint

```http
POST /query
```

**Request Body:**

```json
{
  "prompt": "Explain how tides affect marine ecosystems.",
  "max_tokens": 200, // Optional, default: 1000
  "temperature": 0.7 // Optional, default: 0.7
}
```

**Response:**

```json
{
  "response": "Tides significantly impact marine ecosystems by...",
  "status": "success"
}
```

### Chat Endpoint (Conversational)

```http
POST /chat
```

**Request Body:**

```json
{
  "prompt": "How do coral reefs form?",
  "max_tokens": 200,
  "temperature": 0.7
}
```

**Response:**

```json
{
  "response": "Coral reefs form through a fascinating process...",
  "status": "success"
}
```

## 📋 Usage Examples

### cURL Examples

```bash
# Basic query
curl -X POST "http://localhost:8001/query" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What causes ocean currents?"}'

# Chat format (better for conversational AI)
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explain bioluminescence in marine life"}'

# Health check
curl http://localhost:8001/health
```

### JavaScript/Fetch

```javascript
async function queryOceanGPT(prompt) {
  try {
    const response = await fetch("http://localhost:8001/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: prompt,
        max_tokens: 300,
        temperature: 0.8,
      }),
    });

    const result = await response.json();
    console.log("AI Response:", result.response);
    return result;
  } catch (error) {
    console.error("Error:", error);
  }
}

// Usage
queryOceanGPT("How do whales navigate in the ocean?");
```

### React Component Example

```jsx
import React, { useState } from "react";

function OceanGPTChat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8001/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: query }),
      });

      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      console.error("Error:", error);
      setResponse("Sorry, there was an error processing your request.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about marine science..."
          rows={4}
          cols={50}
        />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Ask OceanGPT"}
        </button>
      </form>

      {response && (
        <div>
          <h3>OceanGPT Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default OceanGPTChat;
```

### Python Requests

```python
import requests

def query_oceangpt(prompt, endpoint="chat"):
    url = f"http://localhost:8001/{endpoint}"
    payload = {"prompt": prompt}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Usage
result = query_oceangpt("How do deep-sea creatures survive extreme pressure?")
if result:
    print("AI Response:", result['response'])
```

## 🔧 Configuration

### Modal Configuration (`oceangpt_modal.py`)

- **GPU**: A100 (40GB) - Sufficient for OceanGPT-7B with 8-bit quantization
- **Model**: `zjunlp/OceanGPT-basic-7B-v0.1`
- **Timeout**: 600 seconds (10 minutes)
- **Quantization**: 8-bit loading for memory efficiency

### FastAPI Configuration (`app.py`)

- **CORS**: Enabled for all origins (configure for production)
- **Timeout**: 120 seconds for Modal requests
- **Port**: 8001 (configurable)

## 📊 API Documentation

When the FastAPI server is running, visit:

- **Interactive Docs**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

## 🚨 Error Handling

The API handles various error scenarios:

```json
// Timeout Error (504)
{
  "error": "Request timeout - the AI model is taking too long to respond",
  "status": "error"
}

// Connection Error (503)
{
  "error": "Failed to connect to AI model: Connection failed",
  "status": "error"
}

// Server Error (500)
{
  "error": "Internal server error: Unexpected error occurred",
  "status": "error"
}
```

## 🎯 Sample Marine Science Questions

Try these example prompts:

- "How do coral reefs form and what threatens them?"
- "Explain the role of phytoplankton in ocean ecosystems"
- "What causes different ocean zones and their characteristics?"
- "How do marine animals adapt to deep-sea pressure?"
- "Describe the process of ocean acidification"
- "What are the effects of El Niño on marine life?"
- "How do whales communicate across long distances?"
- "Explain bioluminescence in deep-sea creatures"

## 🔒 Production Considerations

### Security

```python
# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### Environment Variables

```bash
# Set Modal endpoint URL
export MODAL_ENDPOINT_URL="your-modal-endpoint-url"
export API_PORT=8001
export API_HOST="0.0.0.0"
```

### Rate Limiting

Consider adding rate limiting for production use:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

## 📈 Performance

- **Cold Start**: ~2-3 minutes (model loading)
- **Warm Requests**: ~10-30 seconds (inference time)
- **Concurrent Requests**: Supported via Modal's auto-scaling
- **Token Generation**: ~200 tokens in 10-15 seconds

## 🛠️ Development

### Local Testing

```bash
# Test Modal endpoint directly
curl -X POST "https://your-modal-url" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Test prompt"}'

# Test FastAPI server
curl -X POST "http://localhost:8001/query" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Test prompt"}'
```

### Debugging

```python
# Add logging to app.py
import logging
logging.basicConfig(level=logging.INFO)

# Log requests and responses
logger = logging.getLogger(__name__)
logger.info(f"Received query: {request.prompt}")
```

## 📝 License

This project is part of a hackathon implementation. Please check the respective licenses for:

- OceanGPT model: [zjunlp/OceanGPT-basic-7B-v0.1](https://huggingface.co/zjunlp/OceanGPT-basic-7B-v0.1)
- Modal: [Modal License](https://modal.com/terms)
- FastAPI: [MIT License](https://github.com/tiangolo/fastapi/blob/master/LICENSE)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Built with ❤️ for marine science education and research**
