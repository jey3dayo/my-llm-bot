# My LLM Bot

特定キーワードに反応してエモーションをつけたり、DMをすると返答するBotです。また、`/imagine`コマンドを使って画像生成もできます。

# how to run

```
poetry install
poetry run task start-bot
```

# Features

- 特定のキーワード（懇親会、飲み会、女子会、パーティ）に反応してエモーションを付けます。
- DMを送ると、適切な返答をします。
- `/imagine`コマンドを使って、指定したプロンプトに基づいて画像を生成します。
  - プロンプトの先頭に`x`と数字（1〜10）を付けると、生成する画像の枚数を指定できます。例：`x3 a cat riding a bicycle`

# screenshot

![image](https://github.com/jey3dayo/my-llm-bot/assets/16203828/57c2afe7-d723-4475-b6c7-2036adc0dc61)
![image](https://github.com/jey3dayo/my-llm-bot/assets/16203828/b117da80-7abd-4f24-907d-901f43a65e63)

# /imagine command

`/imagine`コマンドを使って、指定したプロンプトに基づいて画像を生成できます。

Usage:
/imagine [prompt]

```
Examples:
/imagine a cat riding a bicycle
/imagine x3 a dog playing football
```

![image](https://github.com/jey3dayo/my-llm-bot/assets/16203828/da687e49-00b4-4df2-8ef8-da328931aba3)
