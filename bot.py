import logging
import re

import slack_sdk
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from utils import openai_utils
from utils.constants import SLACK_APP_TOKEN, SLACK_BOT_TOKEN

# Initialize the Slack client
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

# [OAuth Token]読み込み
app = App(token=SLACK_BOT_TOKEN)


def get_thread_text(event):
    """Retrieve all messages from a thread."""
    if "thread_ts" in event and event["thread_ts"] is not None:
        response = slack_client.conversations_replies(
            channel=event["channel"], ts=event["thread_ts"]
        )
        logging.info(response)
        return ",".join(
            [re.sub("<.*?> ", "", message["text"]) for message in response["messages"]]
        )
    else:
        return re.sub("<.*?> ", "", event["text"])


# 反応する発言内容を記載
@app.message("懇親会|飲み会|女子会|パーティ")
def party_handler(body, say, client):
    event = body["event"]

    print("懇親会|飲み会|女子会|パーティが送られました")
    response_message = openai_utils.get_party_call_response(client, event)
    if response_message.strip():
        say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


@app.message("^hi")
def hi_handler(body, say):
    print("hiが送られました")
    event = body["event"]
    say(text=event["text"], channel=event["channel"], thread_ts=event["ts"])


# mentionに反応
@app.event("app_mention")
def mention_handler(body, say):
    event = body["event"]
    print(f"メンションされました: {event['text']}")

    # スレッドの全てのメッセージを取得
    send_message = get_thread_text(event)
    print(f"request: {send_message}")
    response_message = openai_utils.get_chat_simple_response(send_message)
    if not response_message.strip() == "":
        say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


# DMに反応
@app.event("message")
def direct_message_handler(body, say):
    event = body["event"]

    # メッセージがDMから来たものかどうかをチェック
    if event["channel_type"] == "im":
        print(f"DMが送られました: {event['text']}")

        # スレッドの全てのメッセージを取得
        send_message = get_thread_text(event)
        response_message = openai_utils.get_chat_simple_response(send_message)
        if not response_message.strip() == "":
            say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
