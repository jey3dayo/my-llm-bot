import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# My AI Bot

load_dotenv()

# OAuth Token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# App-Level Token
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# [OAuth Token]読み込み
app = App(token=SLACK_BOT_TOKEN)

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


# 反応する発言内容を記載
@app.message("^hi")
def message_hello(message, say):
    # 発言のあったチャンネルへメッセージを送信する
    say(f"hello <@{message['user']}>!")
