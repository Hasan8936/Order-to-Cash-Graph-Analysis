"""
ETL script: Load JSONL data from SAP O2C dataset into SQLite database.
Run from project root: python backend/db/seed.py
"""
import json
import sqlite3
import glob
import pathlib
from datetime import datetime, time
from typing import Any
from .connection import init_db, get_db_path


DATA_DIR = pathlib.Path("data/sap-o2c-data")

# Mapping of folder names to table names
TABLE_MAP = {
    "sales_order_headers": "sales_order_headers",
    "sales_order_items": "sales_order_items",
    "billing_document_headers": "billing_document_headers",
    "billing_document_items": "billing_document_items",
    "billing_document_cancellations": "billing_document_cancellations",
    "outbound_delivery_headers": "outbound_delivery_headers",
    "journal_entry_items_accounts_receivable": "journal_entry_items_accounts_receivable",
    "payments_accounts_receivable": "payments_accounts_receivable",
    "business_partners": "business_partners",
    "customer_company_assignments": "customer_company_assignments",
    "customer_sales_area_assignments": "customer_sales_area_assignments",
    "plants": "plants",
    "product_descriptions": "product_descriptions",
    "product_plants": "product_plants",
    "product_storage_locations": "product_storage_locations",
    "sales_order_schedule_lines": "sales_order_schedule_lines",
}


def flatten(d: dict) -> dict:
    """
    Flatten nested time objects like {hours:x, minutes:y, seconds:z} to string.
    Also handles nested dicts for currency amounts.
    """
    out = {}
    for key, value in d.items():
        if isinstance(value, dict):
            # Check if it's a time object
            if all(k in value for k in ["hours", "minutes", "seconds"]):
                # Format as HH:MM:SS
                h = value.get("hours", 0)
                m = value.get("minutes", 0)
                s = value.get("seconds", 0)
                out[key] = f"{h:02d}:{m:02d}:{s:02d}"
            # Check if it's a currency amount
            elif "currency" in value or "amount" in value:
                # Try to extract numeric value
                if "amount" in value:
                    out[key] = value["amount"]
                elif "value" in value:
                    out[key] = value["value"]
                else:
                    out[key] = str(value)
            else:
                # Recursively flatten
                out.update(flatten(value))
        else:
            out[key] = value
    return out


def load_table(conn: sqlite3.Connection, folder: str, table: str) -> int:
    """
    Load all JSONL files from a folder into the database table.
    Returns the number of rows inserted.
    """
    folder_path = DATA_DIR / folder
    if not folder_path.exists():
        print(f"Folder {folder_path} not found, skipping {table}")
        return 0
    
    jsonl_files = glob.glob(str(folder_path / "*.jsonl"))
    if not jsonl_files:
        print(f"No JSONL files found in {folder_path}, creating empty {table}")
        return 0
    
    records = []
    for filepath in jsonl_files:
        with open(filepath, "r") as f:
            for line_num, line in enumerate(f):
                try:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    # Flatten nested structures
                    record = flatten(record)
                    records.append(record)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON in {filepath}:{line_num}: {e}")
                    continue
    
    if not records:
        print(f"No records loaded for {table}")
        return 0
    
    # Get column names from first record
    columns = list(records[0].keys())
    placeholders = ",".join(["?"] * len(columns))
    insert_sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    
    # Insert all records
    cursor = conn.cursor()
    rows_inserted = 0
    for record in records:
        values = [record.get(col) for col in columns]
        try:
            cursor.execute(insert_sql, values)
            rows_inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"Skipping duplicate or invalid record in {table}: {e}")
            continue
    
    return rows_inserted


def seed_database():
    """Initialize database schema and load all JSONL data."""
    print("Initializing database schema...")
    init_db()
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    
    print("\nLoading data from JSONL files...")
    total_rows = 0
    
    for folder, table in TABLE_MAP.items():
        rows = load_table(conn, folder, table)
        total_rows += rows
        print(f"  {table}: {rows} rows")
    
    conn.commit()
    conn.close()
    
    print(f"\nSeeding complete! Total rows inserted: {total_rows}")


if __name__ == "__main__":
    seed_database()
