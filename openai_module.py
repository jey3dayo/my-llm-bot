import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from constants import DEFAULT_MODEL

# FIXME: RAGで使いたかった
emoji_list = """
:emoji:
"""

llm = ChatOpenAI(
    api_key=os.environ["OPENAI_API_KEY"], model=DEFAULT_MODEL, temperature=0.9
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
            # '発言に応じて、slackのemotionを複数個、json形式で返します 例: { "emotion": ["thumbsup", "beers", "dancer" }',
            "発言に応じて、slackのemotionを返します 例: thumbsup, beers, dancer",
        ),
        ("user", "{input}"),
    ]
)


def get_chat_simple_response(input):
    chain = prompt | llm
    response = chain.invoke({"input": input})
    return response.content


# 懇親会を盛り上げる関数
# def get_party_call_response(input):
#     chain = party_prompt | llm
#     response = chain.invoke({"input": input})
#     return response.content


# emotionをつける関数
def get_party_call_response(client, message):
    text = message["text"]
    channel = message["channel"]
    thread_ts = message["ts"]

    chain = party_prompt | llm
    response = chain.invoke({"input": text})
    response_message = response.content

    chain = emotion_prompt | llm
    emotion_response = chain.invoke({"input": response_message})
    emotion_name = emotion_response.content
    print(emotion_response)
    print(f"emotion_name: ${emotion_name}")

    if emotion_name:
        client.reactions_add(channel=channel, name=emotion_name, timestamp=thread_ts)

    return response_message
