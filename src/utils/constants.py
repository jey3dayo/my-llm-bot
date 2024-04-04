import os
import re

from dotenv import load_dotenv

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

load_dotenv()

# OAuth Token
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# App-Level Token
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")

DEFAULT_IMAGE_MODEL = os.getenv("OPENAI_DEFAULT_IMAGE_MODEL", "dall-e-3")

EXTRA_MODEL = os.getenv("OPENAI_EXTRA_MODEL", "gpt-4-turbo-preview")

DEFAULT_EMOTIONS = ["thumbsup"]

GPT4_ROOM_ID = os.getenv("GPT4_ROOM_ID", "")

LOADING_STATE = "loading..."

MULTIPLIER_PATTERN = re.compile(r"\Ax[1-9][0-9]*")
