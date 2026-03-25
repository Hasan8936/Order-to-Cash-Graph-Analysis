"""
Validation script to check graph edges for referential integrity.
Run from project root: python scripts/validate_graph.py
"""
import sqlite3
import sys
from pathlib import Path

def validate_graph(db_path: str = "backend/o2c.db"):
    """
    Validate that all graph edges have valid referential integrity.
    """
    if not Path(db_path).exists():
        print(f"Database not found: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    validation_queries = [
        {
            "name": "Sales Orders → Customers",
            "query": "SELECT COUNT(*) FROM sales_order_headers soh WHERE soh.soldToParty NOT IN (SELECT customer FROM business_partners WHERE customer IS NOT NULL)"
        },
        {
            "name": "Sales Order Items → Products",
            "query": "SELECT COUNT(*) FROM sales_order_items soi WHERE soi.material NOT IN (SELECT product FROM product_descriptions WHERE product IS NOT NULL)"
        },
        {
            "name": "Billing Documents → Customers",
            "query": "SELECT COUNT(*) FROM billing_document_headers bdh WHERE bdh.soldToParty NOT IN (SELECT customer FROM business_partners WHERE customer IS NOT NULL)"
        },
        {
            "name": "Journal Entries → Billing",
            "query": "SELECT COUNT(*) FROM journal_entry_items_accounts_receivable je WHERE je.referenceDocument NOT IN (SELECT accountingDocument FROM billing_document_headers WHERE accountingDocument IS NOT NULL) AND je.referenceDocument IS NOT NULL"
        },
    ]
    
    all_valid = True
    for check in validation_queries:
        try:
            cursor.execute(check["query"])
            result = cursor.fetchone()[0]
            if result > 0:
                print(f"❌ {check['name']}: {result} orphaned records found")
                all_valid = False
            else:
                print(f"✓ {check['name']}: Valid")
        except Exception as e:
            print(f"⚠ {check['name']}: Error - {e}")
    
    conn.close()
    return all_valid


if __name__ == "__main__":
    is_valid = validate_graph()
    sys.exit(0 if is_valid else 1)
