"""Main entry point for NL2SQL Agent"""

import logging
import sys
from pathlib import Path

from .agent import NL2SQLAgent
from . import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def check_database(db_path: str) -> bool:
    """Check if database exists"""
    db_file = Path(db_path)
    if not db_file.exists():
        logger.error(f"Database not found: {db_path}")
        print(f"Error: Database file '{db_path}' not found.")
        print(
            f"Please ensure the database is located at: {db_file.absolute()}"
        )
        return False
    return True


def main():
    """Main function to run the NL2SQL Agent"""
    print("\n" + "=" * 80)
    print("NL2SQL Agent - Learnium Database Query Tool")
    print("=" * 80)
    print("Ask questions in English and get SQL results!")
    print("Type 'exit' or 'quit' to stop.\n")

    # Check database exists
    if not check_database(config.DB_PATH):
        sys.exit(1)

    try:
        # Initialize agent
        logger.info("Initializing NL2SQL Agent...")
        agent = NL2SQLAgent(db_path=config.DB_PATH)
        logger.info("Agent initialized successfully")
        print(f"✓ Connected to database: {config.DB_PATH}\n")

    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")
        print(f"Error: Failed to initialize agent: {e}")
        sys.exit(1)

    # Interactive loop
    try:
        while True:
            try:
                # Get user input
                user_query = input("You: ").strip()

                # Check for exit commands
                if user_query.lower() in ["exit", "quit", "bye", "q"]:
                    print("\nGoodbye!")
                    break

                # Skip empty queries
                if not user_query:
                    continue

                # Process query
                print("\nAgent: Processing your query...")
                result = agent.query(user_query)

                # Display results
                formatted_result = agent.format_results(result)
                print(formatted_result)

                # Log if query failed
                if not result.get("success"):
                    logger.warning(f"Query failed: {user_query}")
                else:
                    logger.info(
                        f"Query successful. Returned {result.get('row_count', 0)} rows"
                    )

                print("\n" + "-" * 80 + "\n")

            except KeyboardInterrupt:
                print("\n\nInterrupted by user.")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                print(f"\nError: {str(e)}")
                print("Please try another query.\n")

    except KeyboardInterrupt:
        print("\n\nAgent shutting down...")
    finally:
        logger.info("NL2SQL Agent session ended")


if __name__ == "__main__":
    main()
