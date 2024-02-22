import os

import slack_sdk.errors
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .constants import DEFAULT_EMOTIONS, DEFAULT_MODEL
from .csv import parse_csv

# FIXME: RAGで使いたかった
emoji_list = """
:emoji:
"""

llm = ChatOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    model=DEFAULT_MODEL,
    temperature=0.9,
)

prompt = ChatPromptTemplate.from_messages(
    [("system", "あなたのお役立ちボット"), ("user", "{input}")]
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


def get_chat_simple_response(input):
    chain = prompt | llm
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
