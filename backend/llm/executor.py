"""
SQL executor and result formatter.
"""
import sqlite3
from typing import List, Dict, Any
from ..db.connection import get_db_path
from .guardrails import validate_sql


def execute_sql(sql: str, db_path: str = None) -> dict:
    """
    Execute a SQL query safely.
    Returns: {success: bool, rows: list, error: str, row_count: int}
    """
    if db_path is None:
        db_path = get_db_path()
    
    # Validate SQL is safe
    validation = validate_sql(sql)
    if not validation["valid"]:
        return {
            "success": False,
            "rows": [],
            "error": validation["message"],
            "row_count": 0
        }
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Execute query with timeout
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        result_rows = [dict(row) for row in rows]
        
        conn.close()
        
        return {
            "success": True,
            "rows": result_rows,
            "error": None,
            "row_count": len(result_rows)
        }
    
    except sqlite3.OperationalError as e:
        return {
            "success": False,
            "rows": [],
            "error": f"Database error: {str(e)}",
            "row_count": 0
        }
    except Exception as e:
        return {
            "success": False,
            "rows": [],
            "error": f"Execution error: {str(e)}",
            "row_count": 0
        }


def format_results(rows: List[Dict[str, Any]], sql: str, explanation: str) -> str:
    """
    Format SQL results into a natural language response.
    Returns formatted text summarizing the results.
    """
    if not rows:
        return f"No results found.\n\n**Query:** `{sql}`\n\n**Explanation:** {explanation}"
    
    # Build summary
    summary_lines = [
        f"**Found {len(rows)} result(s):**\n",
        f"**Explanation:** {explanation}\n",
    ]
    
    # Show first few rows in a readable format
    max_rows_to_display = 10
    for i, row in enumerate(rows[:max_rows_to_display]):
        summary_lines.append(f"\n**Result {i+1}:**")
        for key, value in row.items():
            summary_lines.append(f"  • {key}: {value}")
    
    if len(rows) > max_rows_to_display:
        summary_lines.append(f"\n... and {len(rows) - max_rows_to_display} more results")
    
    summary_lines.append(f"\n**Query:** `{sql}`")
    
    return "\n".join(summary_lines)


def extract_node_ids(rows: List[Dict[str, Any]]) -> List[str]:
    """
    Extract graph node IDs from query results for highlighting.
    Maps common database IDs to graph node types.
    """
    nodes = set()
    
    for row in rows:
        # Check for various ID columns and map to node types
        if "salesOrder" in row and row["salesOrder"]:
            nodes.add(f"SalesOrder:{row['salesOrder']}")
        
        if "billingDocument" in row and row["billingDocument"]:
            nodes.add(f"BillingDocument:{row['billingDocument']}")
        
        if "deliveryDocument" in row and row["deliveryDocument"]:
            nodes.add(f"Delivery:{row['deliveryDocument']}")
        
        if "customer" in row and row["customer"]:
            nodes.add(f"Customer:{row['customer']}")
        
        if "accountingDocument" in row and row["accountingDocument"]:
            account_item = row.get("accountingDocumentItem", "")
            nodes.add(f"JournalEntry:{row['accountingDocument']}|{account_item}")
        
        if "product" in row and row["product"]:
            nodes.add(f"Product:{row['product']}")
        
        if "plant" in row and row["plant"]:
            nodes.add(f"Plant:{row['plant']}")
    
    return list(nodes)
