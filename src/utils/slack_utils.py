import re
import slack_sdk
from .constants import SLACK_BOT_TOKEN

# Initialize the Slack client
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)


def get_thread_text(event):
    """Retrieve all messages from a thread."""
    text = event.get("text", "")
    thread_ts = event.get("thread_ts")
    if thread_ts:
        response = slack_client.conversations_replies(channel=event["channel"], ts=thread_ts)
        messages = response.get("messages", [])

        pattern = re.compile("<.*?> ")
        text = ",".join([pattern.sub("", message["text"]) for message in messages])

    text = re.sub("<.*?> ", "", text)
    return text
