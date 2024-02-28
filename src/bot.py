import logging
import re

import slack_sdk
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from utils import openai_utils
from utils.constants import GPT4_ROOM_ID, LOGGING_LEVEL, SLACK_APP_TOKEN, SLACK_BOT_TOKEN

# Initialize the Slack client
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

# [OAuth Token]読み込み
app = App(token=SLACK_BOT_TOKEN)

logging.basicConfig(encoding="utf-8", level=LOGGING_LEVEL)


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
    logging.debug(f"request: {text}")
    return text


# 反応する発言内容を記載
@app.message("懇親会|飲み会|女子会|パーティ")
def party_handler(body, say, client):
    event = body["event"]

    logging.info("懇親会|飲み会|女子会|パーティが送られました")
    response_message = openai_utils.get_party_call_response(client, event)
    if response_message.strip():
        say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


@app.message("^hi")
def hi_handler(body, say):
    logging.info("hiが送られました")
    event = body["event"]
    say(text=event["text"], channel=event["channel"], thread_ts=event["ts"])


# mentionに反応
@app.event("app_mention")
def mention_handler(body, say):
    event = body["event"]
    logging.info(f"メンションされました: {event['text']}")

    # スレッドの全てのメッセージを取得
    send_message = get_thread_text(event)

    active_llm = openai_utils.llm

    channel = event.get("channel")
    if channel and GPT4_ROOM_ID != "" and channel == GPT4_ROOM_ID:
        active_llm = openai_utils.extra_llm
    response_message = openai_utils.get_chat_response(send_message, active_llm)

    if response_message.strip():
        say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


# DMに反応
@app.event("message")
def direct_message_handler(body, say):
    event = body["event"]

    # メッセージがDMから来たものかどうかをチェック
    if event["channel_type"] == "im":
        logging.info(f"DMが送られました: {event['text']}")

        # スレッドの全てのメッセージを取得
        send_message = get_thread_text(event)
        response_message = openai_utils.get_chat_response(send_message, openai_utils.llm)
        if response_message.strip():
            say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
