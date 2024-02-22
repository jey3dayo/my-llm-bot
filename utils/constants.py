import os

from dotenv import load_dotenv

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

load_dotenv()

# OAuth Token
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# App-Level Token
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")

DEFAULT_EMOTIONS = ["thumbsup"]
