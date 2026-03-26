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
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    def call(self, user_message: str, history: list = None) -> dict:
        """
        Call the LLM with a message and optional history.
        Returns: {success: bool, response: str, error: str}
        """
        if not self.gemini_key and not self.groq_key:
            return {
                "success": False,
                "response": None,
                "error": "No LLM API key configured. Set GEMINI_API_KEY or GROQ_API_KEY"
            }
        
        if self.provider == "gemini" and self.gemini_key:
            return self._call_gemini(user_message, history)
        elif self.provider == "groq" and self.groq_key:
            return self._call_groq(user_message, history)
        else:
            return {
                "success": False,
                "response": None,
                "error": f"LLM provider '{self.provider}' not configured"
            }
    
    def _call_gemini(self, user_message: str, history: list = None) -> dict:
        """Call Google Gemini API."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-1.5")
            model = genai.GenerativeModel(model_name)
            
            # Build conversation history
            messages = [{"role": "user", "parts": SYSTEM_PROMPT}, {"role": "model", "parts": "I understand. I will help with SQL queries for the O2C dataset."}]
            if history:
                for msg in history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "parts": msg.get("content", "")
                    })
            
            messages.append({
                "role": "user",
                "parts": user_message
            })
            
            # Make the API call
            response = model.generate_content(contents=messages)

            # Normalize the response text for downstream parsing/debugging
            try:
                response_text = response.text
            except Exception:
                try:
                    response_text = str(response)
                except Exception:
                    response_text = ""

            return {
                "success": True,
                "response": response_text,
                "error": None
            }
        
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "error": (
                    f"Gemini API error: {str(e)}. "
                    "Check GEMINI_MODEL and GEMINI_API_KEY, or call ListModels to see supported models. "
                )
            }
    
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
