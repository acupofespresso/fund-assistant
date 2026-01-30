"""Entry point for running fund_assistant as a module.

Usage: python -m fund_assistant <command> [args]
"""

from fund_assistant.cli import app

if __name__ == "__main__":
    app()
