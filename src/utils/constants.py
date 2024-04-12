import os
import re
from dotenv import load_dotenv

load_dotenv()

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# OpenAI
OPENAI_DEFAULT_MODEL = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")
OPENAI_EXTRA_MODEL = os.getenv("OPENAI_EXTRA_MODEL", "gpt-4-turbo-preview")
OPENAI_DEFAULT_IMAGE_MODEL = os.getenv("OPENAI_DEFAULT_IMAGE_MODEL", "dall-e-3")
OPENAI_IMAGE_QUORITY = "1024x1024"

# Logging
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

# Emotions
DEFAULT_EMOTIONS = ["thumbsup"]

# GPT-4
GPT4_ROOM_ID = os.getenv("GPT4_ROOM_ID", "")

# Utility
LOADING_STATE = "loading..."
MULTIPLIER_PATTERN = re.compile(r"\Ax[1-9][0-9]*")
