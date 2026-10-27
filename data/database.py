
import sqlite3
from pathlib import Path

# Store the database inside the data folder
DATA_DIR = Path(__file__).resolve().parent
DB_PATH = DATA_DIR / "vulntrack.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the vulnerabilities table if it does not exist."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vuln_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                affected_asset TEXT NOT NULL,
                severity TEXT NOT NULL
                    CHECK (severity IN ('Critical', 'High', 'Medium', 'Low')),
                exploitability INTEGER NOT NULL
                    CHECK (exploitability BETWEEN 1 AND 10),
                impact INTEGER NOT NULL
                    CHECK (impact BETWEEN 1 AND 10),
                asset_criticality INTEGER NOT NULL
                    CHECK (asset_criticality BETWEEN 1 AND 5),
                remediation_hours REAL NOT NULL
                    CHECK (remediation_hours > 0),
                status TEXT NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open', 'In Progress', 'Fixed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


if __name__ == "__main__":
    init_db()
    print("VulnTrack database initialized successfully.")
    print(f"Database location: {DB_PATH}")
