"""Unit tests for NL2SQL Agent"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db_handler import DatabaseHandler
from src.agent import NL2SQLAgent


class TestDatabaseHandler:
    """Test DatabaseHandler class"""

    def test_validate_query_select(self):
        """Test that SELECT queries are validated as safe"""
        handler = DatabaseHandler(":memory:")
        assert handler.validate_query("SELECT * FROM users")
        assert handler.validate_query("  SELECT id FROM courses  ")

    def test_validate_query_dangerous(self):
        """Test that dangerous queries are rejected"""
        handler = DatabaseHandler(":memory:")

        dangerous_queries = [
            "INSERT INTO users VALUES (1, 'test')",
            "UPDATE users SET name='test'",
            "DELETE FROM users",
            "DROP TABLE users",
            "ALTER TABLE users ADD COLUMN age INT",
            "CREATE TABLE new_table (id INT)",
        ]

        for query in dangerous_queries:
            assert not handler.validate_query(query)

    def test_validate_query_no_select(self):
        """Test that non-SELECT queries are rejected"""
        handler = DatabaseHandler(":memory:")
        assert not handler.validate_query("SHOW TABLES")
        assert not handler.validate_query("PRAGMA table_info(users)")


class TestNL2SQLAgent:
    """Test NL2SQLAgent class"""

    @patch("src.agent.OpenAI")
    def test_agent_initialization(self, mock_anthropic):
        """Test agent initialization"""
        # Mock the database
        with patch.object(DatabaseHandler, "get_schema") as mock_schema:
            mock_schema.return_value = "Table: users\n  - id: INT\n  - name: TEXT\n"

            with patch.object(
                DatabaseHandler, "get_connection"
            ) as mock_conn:
                agent = NL2SQLAgent(db_path=":memory:")
                assert agent.db_handler is not None
                assert "users" in agent.schema

    def test_extract_sql_from_response(self):
        """Test SQL extraction from Claude response"""
        with patch.object(DatabaseHandler, "get_schema") as mock_schema:
            mock_schema.return_value = "Table: users\n  - id: INT\n"

            with patch.object(DatabaseHandler, "get_connection"):
                agent = NL2SQLAgent(db_path=":memory:")

                response = (
                    "Here's the SQL query:\n\nSELECT * FROM users LIMIT 10"
                )
                sql = agent._extract_sql_from_response(response)
                assert sql is not None
                assert "SELECT" in sql

    def test_extract_sql_invalid(self):
        """Test that non-SQL responses are handled"""
        with patch.object(DatabaseHandler, "get_schema") as mock_schema:
            mock_schema.return_value = "Table: users\n  - id: INT\n"

            with patch.object(DatabaseHandler, "get_connection"):
                agent = NL2SQLAgent(db_path=":memory:")

                response = "I'm sorry, I cannot generate SQL for that query."
                sql = agent._extract_sql_from_response(response)
                assert sql is None

    def test_format_results_success(self):
        """Test result formatting for successful queries"""
        with patch.object(DatabaseHandler, "get_schema") as mock_schema:
            mock_schema.return_value = "Table: users\n  - id: INT\n"

            with patch.object(DatabaseHandler, "get_connection"):
                agent = NL2SQLAgent(db_path=":memory:")

                result = {
                    "success": True,
                    "data": [
                        {"id": 1, "name": "John"},
                        {"id": 2, "name": "Jane"},
                    ],
                    "row_count": 2,
                }

                formatted = agent.format_results(result)
                assert "2 results" in formatted
                assert "John" in formatted
                assert "Jane" in formatted

    def test_format_results_error(self):
        """Test result formatting for error cases"""
        with patch.object(DatabaseHandler, "get_schema") as mock_schema:
            mock_schema.return_value = "Table: users\n  - id: INT\n"

            with patch.object(DatabaseHandler, "get_connection"):
                agent = NL2SQLAgent(db_path=":memory:")

                result = {"success": False, "error": "Query failed"}

                formatted = agent.format_results(result)
                assert "Error: Query failed" in formatted

    def test_format_results_empty(self):
        """Test result formatting for empty result sets"""
        with patch.object(DatabaseHandler, "get_schema") as mock_schema:
            mock_schema.return_value = "Table: users\n  - id: INT\n"

            with patch.object(DatabaseHandler, "get_connection"):
                agent = NL2SQLAgent(db_path=":memory:")

                result = {"success": True, "data": [], "row_count": 0}

                formatted = agent.format_results(result)
                assert "No results found" in formatted


def test_load_additional_context(tmp_path, monkeypatch):
    """Test that agent loads additional context file when provided"""
    # Create a temporary context file
    ctx_file = tmp_path / "ctx.txt"
    # Include a commented line and a real instruction line; commented lines
    # (starting with '#') should be ignored by the loader.
    ctx_file.write_text("# This is a comment\nPrefer active users by default.\n# Another comment")

    # Point the config to the temporary file via env var
    monkeypatch.setenv("LLM_CONTEXT_FILE", str(ctx_file))

    with patch.object(DatabaseHandler, "get_schema") as mock_schema:
        mock_schema.return_value = "Table: users\n  - id: INT\n"

        with patch.object(DatabaseHandler, "get_connection"):
            # config.get_llm_context_file() reads env at runtime, so we can
            # instantiate the agent and expect it to load the file
            agent = NL2SQLAgent(db_path=":memory:")

            assert hasattr(agent, "additional_context")
            # Commented lines should not appear
            assert "This is a comment" not in agent.additional_context
            assert "Prefer active users" in agent.additional_context


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
