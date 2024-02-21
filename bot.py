import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from utils import openai_utils

load_dotenv()

# OAuth Token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# App-Level Token
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# [OAuth Token]読み込み
app = App(token=SLACK_BOT_TOKEN)


# 反応する発言内容を記載
@app.message("懇親会|飲み会|女子会|パーティ")
def message_hello(body, say, client):
    message = body["event"]
    channel = message["channel"]
    thread_ts = message["ts"]

    response_message = openai_utils.get_party_call_response(client, message)
    if response_message.strip():
        say(text=response_message, channel=channel, thread_ts=thread_ts)


# mentionに反応
@app.event("app_mention")
def mention_handler(body, say):
    message = body["event"]
    text = message["text"]
    channel = message["channel"]
    thread_ts = message["ts"]

    print(f"メンションされました: {text}")
    response_message = openai_utils.get_chat_simple_response(text)
    if response_message.strip():
        say(text=response_message, channel=channel, thread_ts=thread_ts)


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
