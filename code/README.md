# NL2SQL Agent - Learnium Database Query Tool

A simple Natural Language to SQL (NL2SQL) agent that allows you to query the `learnium.db` SQLite database using plain English. The agent uses OpenAI's GPT-4 to convert natural language questions into SQL queries.

## Features

- **Natural Language Interface**: Ask questions in English instead of writing SQL
- **SQLite Integration**: Direct integration with `learnium.db` database
- **OpenAI Powered**: Uses GPT-4 for intelligent SQL generation
- **Error Handling**: Graceful error handling for invalid queries
- **Query Validation**: Validates generated SQL before execution

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

## Usage

### Command Line Interface

```bash
python src/main.py
```

Then enter your questions:
```
You: What courses are available?
Agent: [Executes SQL and returns results]

You: How many students are enrolled?
Agent: [Executes SQL and returns results]
```

### As a Python Module

```python
from src.agent import NL2SQLAgent

agent = NL2SQLAgent(db_path="learnium.db")
result = agent.query("What are the top 5 courses?")
print(result)
```

## Configuration

Edit `src/config.py` to customize:
- Database path
- Model parameters
- Query timeout settings
- Logging level

## Examples

- "Show me all students"
- "How many courses are there?"
- "List students enrolled in Python course"
- "What's the average enrollment per course?"
- "Find courses with less than 10 students"

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
- Limited to schema of learnium.db
- Requires valid OpenAI API key
- Performance depends on database size and query complexity

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
