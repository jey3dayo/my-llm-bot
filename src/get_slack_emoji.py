import os

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
# OAuth Token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# App-Level Token
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# Slackクライアントの初期化
client = WebClient(token=SLACK_BOT_TOKEN)

try:
    # 絵文字リストの取得
    response = client.emoji_list()
    emoji_list = response["emoji"]

    # 絵文字リストをテキストファイルに保存
    with open("emoji_list.txt", "w") as f:
        for name, url in emoji_list.items():
            f.write(f"{name}: {url}\n")

except SlackApiError as e:
    print(f"Error: {e.response['error']}")
