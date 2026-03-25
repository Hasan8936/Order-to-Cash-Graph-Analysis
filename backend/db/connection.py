"""
Database connection and initialization module.
"""
import sqlite3
import os
from pathlib import Path


def get_db_path():
    """Get the database path from environment or use default."""
    return os.getenv("DB_PATH", "backend/o2c.db")


def init_db():
    """Initialize the database with schema."""
    db_path = get_db_path()
    db_file = Path(db_path)
    
    # Create parent directory if needed
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    # Read and execute schema
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "r") as f:
        schema = f.read()
    
    conn.executescript(schema)
    conn.commit()
    conn.close()
    
    print(f"Database initialized at {db_path}")


def get_connection():
    """Get a database connection."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    init_db()
