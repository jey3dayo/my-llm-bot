from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from utils import openai_utils
from utils.constants import SLACK_APP_TOKEN, SLACK_BOT_TOKEN

# [OAuth Token]読み込み
app = App(token=SLACK_BOT_TOKEN)


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
    response_message = openai_utils.get_chat_simple_response(event["text"])
    if not response_message.strip() == "":
        say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


# DMに反応
@app.event("message")
def direct_message_handler(body, say):
    event = body["event"]

    # メッセージがDMから来たものかどうかをチェック
    if event["channel_type"] == "im":
        print(f"DMが送られました: {event['text']}")
        response_message = openai_utils.get_chat_simple_response(event["text"])
        if not response_message.strip() == "":
            say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
