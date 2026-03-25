"""
Chat API endpoint for natural language queries.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os

from ..llm.guardrails import classify_intent
from ..llm.client import LLMClient, parse_llm_response
from ..llm.executor import execute_sql, format_results, extract_node_ids
from ..llm.prompts import SYSTEM_PROMPT

router = APIRouter()
DB_PATH = os.getenv("DB_PATH", "backend/o2c.db")


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    answer: str
    sql: Optional[str] = None
    sql_success: bool = False
    highlighted_nodes: List[str] = []
    error: Optional[str] = None


@router.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Process a natural language query about the O2C dataset.
    
    Flow:
    1. Guardrail check (keyword classification)
    2. LLM call to generate SQL
    3. Execute SQL safely
    4. Extract node IDs for graph highlighting
    5. Return formatted answer
    """
    user_message = req.message.strip()
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Step 1: Guardrail check
    intent = classify_intent(user_message)
    if not intent["allowed"]:
        return ChatResponse(
            answer=intent.get("response", "This question is outside the scope of this system."),
            sql=None,
            sql_success=False,
            highlighted_nodes=[]
        )
    
    # Step 2: Call LLM to generate SQL
    llm_client = LLMClient()
    history_dicts = [{"role": m.role, "content": m.content} for m in (req.history or [])]
    
    llm_result = llm_client.call(user_message, history_dicts)
    if not llm_result["success"]:
        return ChatResponse(
            answer=f"Sorry, I encountered an error: {llm_result['error']}",
            sql=None,
            sql_success=False,
            highlighted_nodes=[],
            error=llm_result["error"]
        )
    
    # Step 3: Parse LLM response to extract SQL
    parsed = parse_llm_response(llm_result["response"])
    
    if not parsed.get("is_valid") or not parsed.get("sql"):
        return ChatResponse(
            answer=parsed.get("explanation", "I couldn't generate a valid query for your question."),
            sql=parsed.get("sql"),
            sql_success=False,
            highlighted_nodes=[]
        )
    
    # Step 4: Execute SQL
    sql = parsed.get("sql")
    execution_result = execute_sql(sql, DB_PATH)
    
    if not execution_result["success"]:
        return ChatResponse(
            answer=f"Error executing query: {execution_result['error']}",
            sql=sql,
            sql_success=False,
            highlighted_nodes=[],
            error=execution_result["error"]
        )
    
    # Step 5: Format results and extract nodes
    rows = execution_result["rows"]
    explanation = parsed.get("explanation", "")
    formatted_answer = format_results(rows, sql, explanation)
    
    # Extract node IDs for highlighting
    node_ids = extract_node_ids(rows)
    
    return ChatResponse(
        answer=formatted_answer,
        sql=sql,
        sql_success=True,
        highlighted_nodes=node_ids
    )


@router.get("/api/chat/history")
async def get_chat_history():
    """
    Placeholder for retrieving chat history.
    In production, this would query a message store.
    """
    return {
        "messages": []
    }
