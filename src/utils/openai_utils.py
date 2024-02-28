import os

import slack_sdk.errors
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1 import SecretStr

from .constants import DEFAULT_EMOTIONS, DEFAULT_MODEL, EXTRA_MODEL
from .csv import parse_csv

# FIXME: RAGで使いたかった
emoji_list = """
:emoji:
"""

api_key_value = os.getenv("OPENAI_API_KEY")
if not api_key_value:
    raise ValueError("環境変数 'OPENAI_API_KEY' が設定されていません。")
api_key = SecretStr(api_key_value)

llm = ChatOpenAI(
    api_key=api_key,
    model=DEFAULT_MODEL,
    temperature=0.9,
)

extra_llm = ChatOpenAI(
    api_key=api_key,
    model=EXTRA_MODEL,
    temperature=0.9,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "あなたのお役立ちボット。slackの発言を理解できます。",
        ),
        ("user", "{input}"),
    ]
)

party_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "飲み会を盛り上げるための発言をするbotです。パリピ発言が特徴です。slackでやりとりをしているので絵文字も上手につけれます。",
        ),
        ("user", "{input}"),
    ]
)


emotion_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "発言に応じて、slackのemotionを必ず1つ返します 例: thumbsup,beers,dancer",
        ),
        ("user", "{input}"),
    ]
)

emotions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            # "発言に応じて、slackのemotionを複数個、csv形式で返します 例: thumbsup, beers, dancer",
            "発言に応じて、slackのemotionを6個、csv形式で返します 例: thumbsup,beers,dancer",
        ),
        ("user", "{input}"),
    ]
)


def get_chat_response(input, llm_model=llm):
    chain = prompt | llm_model
    # TODO: convert safe input
    response = chain.invoke({"input": input})
    return response.content


def add_reactions_to_channel(client, channel, emotion, thread_ts):
    """Add reactions to a channel for each emotion."""
    try:
        client.reactions_add(channel=channel, name=emotion, timestamp=thread_ts)

    except slack_sdk.errors.SlackApiError as e:
        print(f"Slack API error adding reaction {emotion}: {e.response['error']}")


# emotionをつける関数
def get_party_call_response(client, message):
    text = message["text"]
    channel = message["channel"]
    thread_ts = message["ts"]

    chain = party_prompt | llm
    response = chain.invoke({"input": text})
    response_content = response.content

    # csvからemotionを抽出
    chain = emotions_prompt | llm
    emotions_response = chain.invoke({"input": response_content})
    emotions = parse_csv(emotions_response.content, DEFAULT_EMOTIONS)

    # emotionsをループしてreactionをつける
    for emotion in emotions:
        add_reactions_to_channel(client, channel, emotion.strip(), thread_ts)

    return response_content
