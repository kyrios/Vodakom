# NL2SQL Agent - Natural Language Database Query Tool

A simple Natural Language to SQL (NL2SQL) agent that converts plain language questions into SQL queries. The agent uses OpenAI's GPT-4 to generate and execute SQL against a SQLite database, supporting queries in English, German, and other languages.

## Features

- **Natural Language Interface**: Ask questions in any language instead of writing SQL
- **SQLite Integration**: Query any SQLite database
- **OpenAI Powered**: Uses GPT-4 for intelligent SQL generation
- **Error Handling**: Graceful error handling for invalid queries
- **Contextual Awareness**: Can be configured with domain-specific context to improve query accuracy

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── agent.py             # NL2SQL Agent implementation
│   ├── db_handler.py        # Database connection and query execution
│   └── config.py            # Configuration settings
├── tests/
│   ├── __init__.py
│   └── test_agent.py        # Unit tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- SQLite3 (usually included with Python)
- OpenAI API key (for GPT-4)

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Quick Start

Start the agent from the command line:

```bash
python src/main.py
```

The agent will launch an interactive prompt. Enter your question in natural language and press Enter. The agent will:
1. Parse your question
2. Generate an appropriate SQL query
3. Execute it against the database
4. Return the results

Example session:
```
Starting NL2SQL Agent...
> Show me all data from the first table
[Agent generates SQL and returns results]

> How many rows are in the database?
[Agent generates SQL and returns count]

> Exit or press Ctrl+C to quit
```

## Usage

### Command Line Interface

```bash
python src/main.py
```

Then enter your questions in natural language. The agent will generate the appropriate SQL query and return results.

### As a Python Module

```python
from src.agent import NL2SQLAgent

agent = NL2SQLAgent(db_path="learnium.db")
result = agent.query("Show me all data from the first table")
print(result)
```

## Configuration
Configuration is controlled via environment variables. Create a `.env` file from the provided
`.env.example` and adjust values. The project uses `python-dotenv` to load variables.

Important variables:

- `OPENAI_API_KEY` - your OpenAI API key (required)
- `LLM_CONTEXT_FILE` - path to an optional additional context file (for example guidance or
   company-specific knowledge). This file is read and supplied to the LLM when building prompts.
   The code ships with an example `context.txt` in `examples/Vodakom/` and the `.env.example` files
   point to that path by default. You can set an absolute path or a path relative to the `.env` file.
- `LLM_CONTEXT_MAX_CHARS` - optional, maximum chars of the context file to include in prompts.

You can still edit `src/config.py` for other advanced settings (database path, timeouts, logging),
but prefer overriding behavior with environment variables so you don't need to change source code.

## Examples

- "Show me all records from the main table"
- "How many rows are in the database?"
- "Get all unique values from column X"
- "Count records by category"
- "Find records matching specific criteria"

## Error Handling

The agent includes built-in error handling for:
- Invalid SQL queries
- Database connection issues
- Rate limiting from API
- Malformed responses

## Testing

Run tests with:
```bash
pytest tests/
```

## Limitations

- Only reads from database (no INSERT/UPDATE/DELETE operations)
- Performance depends on database size and query complexity
- Requires valid OpenAI API key

## Future Improvements

- Multi-turn conversations for clarification
- Query caching for frequently asked questions
- Support for more complex analytical queries
- Web UI interface
- Query result visualization

## License

MIT

## Support

For issues or questions, please check the agent logs or review the test cases in `tests/test_agent.py`.
