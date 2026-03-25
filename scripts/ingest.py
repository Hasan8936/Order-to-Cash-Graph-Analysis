"""
Data validation and ingestion script.
Checks dataset structure and loads JSONL files into the database.
Run from project root: python scripts/ingest.py
"""
import json
import sys
from pathlib import Path

def check_dataset_structure(data_dir: str = "data/sap-o2c-data") -> bool:
    """Check if dataset directories exist."""
    required_folders = [
        "sales_order_headers",
        "sales_order_items",
        "billing_document_headers",
        "billing_document_items",
        "business_partners",
        "outbound_delivery_headers",
        "journal_entry_items_accounts_receivable",
        "payments_accounts_receivable",
    ]
    
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return False
    
    missing = []
    for folder in required_folders:
        folder_path = data_path / folder
        if not folder_path.exists():
            missing.append(folder)
    
    if missing:
        print(f"❌ Missing data folders: {', '.join(missing)}")
        return False
    
    print("✓ All required data folders found")
    return True


def ingest_data():
    """
    Main ingestion function.
    """
    print("Starting data ingestion...\n")
    
    # Check dataset structure
    if not check_dataset_structure():
        print("\nPlease ensure all data folders are in place before running ingestion.")
        return False
    
    # Import the seed function
    try:
        from backend.db.seed import seed_database
        seed_database()
        print("\n✓ Data ingestion complete!")
        return True
    except ImportError as e:
        print(f"❌ Error importing seed module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        return False


if __name__ == "__main__":
    success = ingest_data()
    sys.exit(0 if success else 1)
