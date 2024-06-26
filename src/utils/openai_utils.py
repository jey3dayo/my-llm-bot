import asyncio
import logging
import os
import io
import requests
from typing import Dict, Union
import slack_sdk.errors
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import AsyncOpenAI
from pydantic.v1 import SecretStr
from .constants import (
    DEFAULT_EMOTIONS,
    OPENAI_DEFAULT_IMAGE_MODEL,
    OPENAI_DEFAULT_MODEL,
    OPENAI_EXTRA_MODEL,
    MULTIPLIER_PATTERN,
    GPT4_ROOM_ID,
    OPENAI_IMAGE_QUORITY,
)
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
    model=OPENAI_DEFAULT_MODEL,
    temperature=0.9,
)

extra_llm = ChatOpenAI(
    api_key=api_key,
    model=OPENAI_EXTRA_MODEL,
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


def get_active_llm(channel):
    """Get the active language model based on the channel."""
    active_llm = llm
    if channel and GPT4_ROOM_ID != "" and channel == GPT4_ROOM_ID:
        active_llm = extra_llm
    return active_llm


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
        logging.error(f"Slack API error adding reaction {emotion}: {e.response['error']}")


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


async def generate_images(prompt: str, quantity: int):
    async with AsyncOpenAI() as client:
        image_params: Dict[str, Union[str, int]] = {
            "model": OPENAI_DEFAULT_IMAGE_MODEL,
            "quality": "standard",
            "n": quantity,
            "size": OPENAI_IMAGE_QUORITY,
            "prompt": prompt,
        }
        res = await client.images.generate(**image_params)
        return res.data


def create_image_response(client, channel, prompt: str):
    blocks = []
    count = 1
    prompt_list = prompt.split(" ")[0]
    multiplier = prompt_list[0]
    if MULTIPLIER_PATTERN.match(multiplier):
        value = int(multiplier[1:])
        if 0 < value < 11:
            count = value
        prompt = "".join(prompt_list[1:])

    logging.info(f"Generating images for prompt: {prompt}")
    images = asyncio.run(generate_images(prompt, count))

    for image in images:
        # 画像をSlackにアップロード
        response = client.files_upload_v2(
            channels=channel,
            initial_comment=prompt,
            file=io.BytesIO(requests.get(image.url).content),
            filename=f"{prompt}.png",
        )
        image_block = {
            "type": "image",
            "title": {"type": "plain_text", "text": prompt, "emoji": True},
            "image_url": response["file"]["url_private"],
            "alt_text": prompt,
        }
        blocks.append(image_block)
    return blocks
