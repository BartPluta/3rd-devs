from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import json
from openai_service import OpenAIService
from typing import Dict, List, Any, Optional

# Create FastAPI app
app = FastAPI()
openai_service = OpenAIService()
previous_summarization = ""

# Define models
class ChatRequest(BaseModel):
    message: Dict[str, str]
    model_config = {"extra": "allow"}  # Pydantic v2 syntax

# Function to generate summarization based on the current turn and previous summarization
def generate_summarization(user_message: Dict[str, str], assistant_response: Dict[str, str]) -> str:
    summarization_prompt = {
        "role": "system",
        "content": f"""Please summarize the following conversation in a concise manner, incorporating the previous summary if available:
<previous_summary>{previous_summarization or "No previous summary"}</previous_summary>
<current_turn> User: {user_message.get('content')}
Assistant: {assistant_response.get('content')} </current_turn>
"""
    }

    response = openai_service.completion(
        [summarization_prompt, {"role": "user", "content": "Please create/update our conversation summary."}],
        "gpt-4o-mini",
        False
    )
    
    return response.choices[0].message.content or "No conversation history"

# Function to create system prompt
def create_system_prompt(summarization: str) -> Dict[str, str]:
    content = """You are Alice, a helpful assistant who speaks using as few words as possible. 
    """
    
    if summarization:
        content += f"""
        Here is a summary of the conversation so far: 
        <conversation_summary>
          {summarization}
        </conversation_summary>
        """
    
    content += "Let's chat!"
    
    return {"role": "system", "content": content}

# Chat endpoint POST /api/chat
@app.post("/api/chat")
async def chat(request: Request):
    global previous_summarization
    data = await request.json()
    message = data.get("message")
    
    try:
        system_prompt = create_system_prompt(previous_summarization)
        
        assistant_response = openai_service.completion(
            [system_prompt, message],
            "gpt-4o",
            False
        )
        
        # Generate new summarization
        previous_summarization = generate_summarization(
            message, 
            {"content": assistant_response.choices[0].message.content}
        )
        
        return assistant_response
    except Exception as error:
        print(f"Error in OpenAI completion: {error}")
        return JSONResponse(
            status_code=500,
            content={"error": "An error occurred while processing your request"}
        )

# Demo endpoint POST /api/demo
@app.post("/api/demo")
async def demo():
    global previous_summarization
    
    demo_messages = [
        {"content": "Hi! I'm Adam", "role": "user"},
        {"content": "How are you?", "role": "user"},
        {"content": "Do you know my name?", "role": "user"}
    ]
    
    assistant_response = None
    
    for message in demo_messages:
        print("--- NEXT TURN ---")
        print(f"Adam: {message['content']}")
        
        try:
            system_prompt = create_system_prompt(previous_summarization)
            
            assistant_response = openai_service.completion(
                [system_prompt, message],
                "gpt-4o",
                False
            )
            
            print(f"Alice: {assistant_response.choices[0].message.content}")
            
            # Generate new summarization
            previous_summarization = generate_summarization(
                message,
                {"content": assistant_response.choices[0].message.content}
            )
            
        except Exception as error:
            print(f"Error in OpenAI completion: {error}")
            return JSONResponse(
                status_code=500,
                content={"error": "An error occurred while processing your request"}
            )
    
    return assistant_response

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000) 