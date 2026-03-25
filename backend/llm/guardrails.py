"""
Guardrails for input validation and intent classification.
Prevents off-topic questions from reaching the LLM.
"""
import re
from .prompts import GUARDRAIL_KEYWORDS, O2C_KEYWORDS

OFF_TOPIC_RESPONSE = (
    "This system is designed to answer questions about the Order-to-Cash dataset only. "
    "Please ask something related to sales orders, deliveries, billing documents, payments, "
    "customers, or products."
)


def is_off_topic(message: str) -> bool:
    """
    Quick keyword-based check for off-topic messages.
    This is a first-layer guardrail (cheap, fast).
    """
    message_lower = message.lower()
    
    # Check for explicit off-topic keywords
    for keyword in GUARDRAIL_KEYWORDS:
        if keyword in message_lower:
            return True
    
    # Check for prompt injection attempts
    injection_patterns = [
        r"forget your.*instruction",
        r"ignore your.*prompt",
        r"act as",
        r"pretend you are",
        r"you are now",
        r"from now on",
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return True
    
    return False


def classify_intent(message: str) -> dict:
    """
    Classify whether a message is O2C-related (domain relevant).
    Returns: {allowed: bool, reason: str}
    """
    message_lower = message.lower()
    
    # Fast off-topic check
    if is_off_topic(message):
        return {
            "allowed": False,
            "reason": "off_topic",
            "response": OFF_TOPIC_RESPONSE
        }
    
    # Check if message contains O2C-relevant terms
    o2c_score = sum(1 for keyword in O2C_KEYWORDS if keyword in message_lower)
    
    # If the message is very short or has no O2C keywords, it might be off-topic
    if len(message) < 10:
        return {
            "allowed": False,
            "reason": "too_short",
            "response": "Please provide more specific details about what you'd like to know about the Order-to-Cash process."
        }
    
    if o2c_score == 0 and not any(word in message_lower for word in ["show", "find", "list", "get", "what", "how", "which", "tell"]):
        return {
            "allowed": False,
            "reason": "unclear_domain",
            "response": OFF_TOPIC_RESPONSE
        }
    
    # Message appears to be O2C-related
    return {
        "allowed": True,
        "reason": "domain_relevant"
    }


def validate_sql(sql: str) -> dict:
    """
    Validate that SQL is safe to execute (read-only).
    Returns: {valid: bool, reason: str}
    """
    sql_upper = sql.upper().strip()
    
    # Only allow SELECT queries
    if not sql_upper.startswith("SELECT"):
        return {
            "valid": False,
            "reason": "not_select",
            "message": "Only SELECT queries are allowed"
        }
    
    # Disallow dangerous operations
    dangerous_keywords = ["DROP", "DELETE", "INSERT", "UPDATE", "PRAGMA", "ATTACH", "DETACH"]
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return {
                "valid": False,
                "reason": "dangerous_operation",
                "message": f"Operation '{keyword}' is not allowed"
            }
    
    # Check for comment-based injection
    if "--" in sql or "/*" in sql:
        # Comments are okay in SELECT, but we should be careful
        pass
    
    return {
        "valid": True,
        "reason": "safe"
    }
