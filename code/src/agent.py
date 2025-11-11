"""NL2SQL Agent implementation using OpenAI API"""

import logging
from typing import Dict, Any, Optional
import json
from openai import OpenAI

from .db_handler import DatabaseHandler
from . import config

logger = logging.getLogger(__name__)


class NL2SQLAgent:
    """Natural Language to SQL Agent using OpenAI"""

    def __init__(self, db_path: str = config.DB_PATH):
        """
        Initialize the NL2SQL Agent.

        Args:
            db_path: Path to the SQLite database
        """
        self.db_handler = DatabaseHandler(db_path)
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.schema = self._load_schema()
        # Load optional user-provided additional context for the LLM
        # This file lives outside the source tree and can be edited by users.
        self.additional_context = self._load_additional_context()

    def _load_schema(self) -> str:
        """Load database schema once during initialization"""
        try:
            schema = self.db_handler.get_schema()
            logger.info("Database schema loaded successfully")
            return schema
        except Exception as e:
            logger.error(f"Failed to load schema: {e}")
            raise

    def _load_additional_context(self) -> str:
        """
        Load additional user-provided context from a text file outside the
        source tree. The path is provided by `config.get_llm_context_file()`.

        Returns an empty string if the file does not exist or cannot be read.
        """
        try:
            context_path = config.get_llm_context_file()
            if not context_path:
                return ""

            from pathlib import Path

            p = Path(context_path)
            if not p.exists() or not p.is_file():
                logger.debug(f"No additional context file found at: {context_path}")
                return ""

            text = p.read_text(encoding="utf-8")

            # Split into lines and remove commented lines (starting with #)
            # and blank lines. Preserve ordering of non-comment lines.
            lines = []
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                lines.append(line)

            text = "\n".join(lines)

            # Truncate to configured max chars to avoid huge prompts
            max_chars = getattr(config, "LLM_CONTEXT_MAX_CHARS", None)
            if max_chars:
                text = text[: int(max_chars)]

            text = text.strip()
            logger.info(f"Loaded additional LLM context from: {context_path}")
            return text
        except Exception as e:
            logger.warning(f"Failed to load additional context: {e}")
            return ""

    def _create_prompt(self, natural_language_query: str) -> str:
        """
        Create a prompt for Claude to generate SQL.

        Args:
            natural_language_query: User's question in natural language

        Returns:
            Formatted prompt for Claude
        """
        # If an additional context file was provided and contains content,
        # include it at the top of the prompt so the model can apply business
        # logic or extra instructions when generating the SQL.
        context_block = ""
        if getattr(self, "additional_context", None):
            context_block = f"Additional Context:\n{self.additional_context}\n\n"

        return (
            f"""You are an expert SQL developer. Convert the following natural language question into a SQL SELECT query.

{context_block}Database Schema:
{self.schema}

Rules:
1. Only generate SELECT queries
2. Return ONLY the SQL query, no explanations
3. Use proper SQL syntax
4. If the question is ambiguous, make reasonable assumptions
5. Always use LIMIT to prevent returning too many rows
6. Format the query clearly

Natural Language Question: {natural_language_query}

Generate the SQL query:"""
        )

    def _extract_sql_from_response(self, response: str) -> Optional[str]:
        """
        Extract SQL query from response, handling markdown code fences.

        Args:
            response: Response text that may contain markdown

        Returns:
            Extracted SQL query or None
        """
        # Remove markdown code fences
        text = response.replace("```sql", "").replace("```", "").strip()
        
        # Split by newlines and find the SQL
        lines = text.split("\n")
        
        sql_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Start collecting when we see SELECT or WITH
            if line.upper().startswith(("SELECT", "WITH")):
                sql_lines.append(line)
            elif sql_lines:
                # Continue collecting SQL lines
                sql_lines.append(line)
        
        sql_query = " ".join(sql_lines).strip().rstrip(";").strip()
        
        # Handle multiple statements separated by semicolon
        if ";" in sql_query:
            sql_query = sql_query.split(";")[0].strip()
        
        logger.debug(f"Extracted SQL: {sql_query}")
        
        if sql_query and sql_query.upper().startswith("SELECT"):
            return sql_query
        
        return None

    def query(self, natural_language_query: str) -> Dict[str, Any]:
        """
        Process a natural language query and return results.

        Args:
            natural_language_query: User's question in natural language

        Returns:
            Dictionary with results or error information
        """
        try:
            logger.info(f"Processing query: {natural_language_query}")

            # Create prompt for OpenAI
            prompt = self._create_prompt(natural_language_query)

            # Call OpenAI API
            message = self.client.chat.completions.create(
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract SQL from response
            response_text = message.choices[0].message.content
            sql_query = self._extract_sql_from_response(response_text)

            if not sql_query:
                logger.warning("Failed to extract SQL from response")
                return {
                    "success": False,
                    "error": "Failed to generate valid SQL query",
                    "natural_language_query": natural_language_query,
                }

            logger.debug(f"Generated SQL: {sql_query}")

            # Validate query
            if not self.db_handler.validate_query(sql_query):
                logger.warning(f"Invalid query generated: {sql_query}")
                return {
                    "success": False,
                    "error": "Generated query failed validation",
                    "query": sql_query,
                    "natural_language_query": natural_language_query,
                }

            # Execute query
            result = self.db_handler.execute_query(
                sql_query, max_rows=config.MAX_ROWS_RETURN
            )

            # Enhance result with original query
            result["natural_language_query"] = natural_language_query

            return result

        except Exception as e:
            logger.error(f"API error: {e}")
            return {
                "success": False,
                "error": f"API error: {str(e)}",
                "natural_language_query": natural_language_query,
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "natural_language_query": natural_language_query,
            }

    def format_results(self, result: Dict[str, Any]) -> str:
        """
        Format query results for display.

        Args:
            result: Result dictionary from query()

        Returns:
            Formatted string for display
        """
        if not result["success"]:
            return f"Error: {result.get('error', 'Unknown error')}"

        data = result.get("data", [])
        if not data:
            return "No results found."

        # Format as table
        output = f"\nFound {result.get('row_count', 0)} results:\n"
        output += "-" * 80 + "\n"

        # Get column names from first row
        if data:
            columns = list(data[0].keys())
            output += " | ".join(columns) + "\n"
            output += "-" * 80 + "\n"

            # Add rows
            for row in data[:10]:  # Show first 10 rows
                values = [str(row[col]) for col in columns]
                output += " | ".join(values) + "\n"

            if len(data) > 10:
                output += f"\n... and {len(data) - 10} more rows\n"

        return output
