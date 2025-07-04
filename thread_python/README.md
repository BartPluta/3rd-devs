# Thread Python

This is a Python implementation of the Thread application originally written in TypeScript. The application provides a simple API for chat conversations with memory through summarization.

## Features

- Chat API endpoint with conversation memory
- Demo endpoint to test the conversation flow
- Automatic conversation summarization using OpenAI

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Set your OpenAI API key as an environment variable:
```
# On Windows
set OPENAI_API_KEY=your_api_key_here

# On Linux/macOS
export OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```
python app.py
```

2. Send a POST request to `/api/chat` with the following JSON body:
```json
{
  "message": {
    "role": "user",
    "content": "Hello, how are you?"
  }
}
```

3. Or run the demo endpoint with a POST request to `/api/demo`


## API Endpoints

- `POST /api/chat` - Chat with the assistant
- `POST /api/demo` - Run a demo conversation

## Components

- `app.py` - FastAPI application with API endpoints
- `openai_service.py` - Service for interacting with OpenAI API 