import os

from dotenv import load_dotenv

load_dotenv()

# OAuth Token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# App-Level Token
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")

DEFAULT_EMOTIONS = ["thumbsup"]
