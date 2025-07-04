import os
from openai import OpenAI
from typing import Dict, List, Any
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        # Load environment variables from .env file if present
        load_dotenv()
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY environment variable not set. Using empty string.")
            api_key = ""
            
        self.openai = OpenAI(api_key=api_key)
    
    def completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4",
        stream: bool = False
    ) -> Any:  # Using Any to simplify type annotations
        try:
            # Convert messages to the format expected by the new OpenAI API
            formatted_messages = []
            for message in messages:
                msg = {
                    "role": message["role"],
                    "content": message["content"]
                }
                if "name" in message:
                    msg["name"] = message["name"]
                formatted_messages.append(msg)
                
            # The OpenAI Python client is synchronous in v1.x
            chat_completion = self.openai.chat.completions.create(
                messages=formatted_messages,
                model=model,
                stream=stream
            )
            return chat_completion
        except Exception as error:
            print(f"Error in OpenAI completion: {error}")
            raise error 