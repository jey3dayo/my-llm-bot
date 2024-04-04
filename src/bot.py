import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from utils import slack_utils, openai_utils
from utils.constants import (
    LOGGING_LEVEL,
    SLACK_APP_TOKEN,
    SLACK_BOT_TOKEN,
)

app = App(token=SLACK_BOT_TOKEN)
logging.basicConfig(encoding="utf-8", level=LOGGING_LEVEL)


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
    send_message = slack_utils.get_thread_text(event)

    channel = event.get("channel")
    active_llm = openai_utils.get_active_llm(channel)
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
        send_message = slack_utils.get_thread_text(event)
        response_message = openai_utils.get_chat_response(send_message, openai_utils.llm)
        if response_message.strip():
            say(text=response_message, channel=event["channel"], thread_ts=event["ts"])


@app.command("/imagine")
def imagine_command(ack, respond, command):
    try:
        ack()
        respond(response_type="ephemeral", text="loading...")
    except Exception as e:
        logging.error(f"Error generating images: {e}")
        respond(response_type="ephemeral", text="Error generating images. Please try again later.")

    if command["text"] == "":
        respond(response_type="ephemeral", text="please specify a prompt and try again.", replace_original=True)
        return

    response_blocks = openai_utils.create_image_response(command["text"])
    respond(
        response_type="in_channel", blocks=response_blocks, unfurl_media=True, unfurl_links=True, delete_original=True
    )


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
