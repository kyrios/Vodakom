"""Database handler for SQLite operations"""

import sqlite3
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseHandler:
    """Handles SQLite database connections and queries"""

    def __init__(self, db_path: str, timeout: int = 30):
        """
        Initialize database handler.

        Args:
            db_path: Path to SQLite database file
            timeout: Connection timeout in seconds
        """
        self.db_path = db_path
        self.timeout = timeout

    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=self.timeout)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def get_schema(self) -> str:
        """
        Retrieve the database schema.

        Returns:
            String containing all table names and their schemas
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Get all table names
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = cursor.fetchall()

            schema = ""
            for (table_name,) in tables:
                schema += f"\nTable: {table_name}\n"

                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    schema += f"  - {col_name}: {col_type}\n"

            conn.close()
            return schema
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve schema: {e}")
            raise

    def execute_query(
        self, query: str, max_rows: int = 100
    ) -> Dict[str, Any]:
        """
        Execute a SELECT query safely.

        Args:
            query: SQL SELECT query to execute
            max_rows: Maximum number of rows to return

        Returns:
            Dictionary with results and metadata
        """
        try:
            # Validate query is SELECT only
            query_upper = query.strip().upper()
            if not query_upper.startswith("SELECT"):
                return {
                    "success": False,
                    "error": "Only SELECT queries are allowed",
                    "data": [],
                }

            # Extract only the first statement (remove trailing semicolons and extra statements)
            query = query.strip().rstrip(";")
            if ";" in query:
                query = query.split(";")[0].strip()

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(query)
            rows = cursor.fetchall()

            # Limit rows returned
            if len(rows) > max_rows:
                logger.warning(
                    f"Query returned {len(rows)} rows, limiting to {max_rows}"
                )
                rows = rows[:max_rows]

            # Convert rows to dictionaries
            data = [dict(row) for row in rows]

            conn.close()

            return {
                "success": True,
                "data": data,
                "row_count": len(data),
                "query": query,
            }

        except sqlite3.Error as e:
            logger.error(f"Query execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "query": query,
            }
        except Exception as e:
            logger.error(f"Unexpected error during query execution: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "data": [],
                "query": query,
            }
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "data": [],
                "query": query,
            }

    def validate_query(self, query: str) -> bool:
        """
        Validate that a query is safe to execute.

        Args:
            query: SQL query to validate

        Returns:
            True if query is safe, False otherwise
        """
        logging.debug(f"Validating query: {query}")
        query_upper = query.strip().upper()

        # Only allow SELECT queries
        if not query_upper.startswith("SELECT"):
            return False

        # Prevent dangerous operations
        dangerous_keywords = [
            "INSERT",
            "UPDATE",
            "DELETE",
            "DROP",
            "ALTER",
            "CREATE",
            "PRAGMA",
            "ATTACH",
            "DETACH",
        ]

        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False

        return True
