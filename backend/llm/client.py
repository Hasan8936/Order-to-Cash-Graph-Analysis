"""
LLM API client for calling Gemini or Groq.
"""
import json
import os
from typing import Optional
import requests
from .prompts import SYSTEM_PROMPT


class LLMClient:
    """Client for calling LLM APIs."""
    
    def __init__(self):
        # Prefer Groq as the default provider. Users may override with
        # `LLM_PROVIDER` but Groq will be used if no provider is set.
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "groq").lower()
    
    def call(self, user_message: str, history: list = None) -> dict:
        """
        Call the LLM with a message and optional history.
        Returns: {success: bool, response: str, error: str}
        """
        # Ensure Groq API key is present for the default provider.
        if self.provider == "groq":
            if not self.groq_key:
                return {
                    "success": False,
                    "response": None,
                    "error": "GROQ_API_KEY not set. Set GROQ_API_KEY to use the Groq provider."
                }
            return self._call_groq(user_message, history)

        return {
            "success": False,
            "response": None,
            "error": f"LLM provider '{self.provider}' not supported in this deployment. Use 'groq'."
        }
    
    # Gemini support removed from this deployment. Groq is the supported
    # LLM provider and is handled by `_call_groq` below.
    
    def _call_groq(self, user_message: str, history: list = None) -> dict:
        """Call Groq API."""
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json"
            }
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            
            if history:
                messages.extend(history)
            
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "response": data["choices"][0]["message"]["content"],
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "response": None,
                    "error": f"Groq API returned {response.status_code}: {response.text}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "error": f"Groq API error: {str(e)}"
            }


def parse_llm_response(response_text: str) -> dict:
    """
    Parse the LLM response to extract SQL and explanation.
    Expects JSON format.
    """
    try:
        # Try to extract JSON from the response
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        
        if start >= 0 and end > start:
            json_str = response_text[start:end]
            return json.loads(json_str)
        else:
            return {
                "sql": None,
                "explanation": response_text,
                "is_valid": False
            }
    except json.JSONDecodeError:
        return {
            "sql": None,
            "explanation": response_text,
            "is_valid": False
        }


if __name__ == "__main__":
    client = LLMClient()
    result = client.call("What is the dataset structure?")
    print(json.dumps(result, indent=2))
