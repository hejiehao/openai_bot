from khl import Bot, Message, Cert
import openai
from utils.open_json import *

# 打开config.json
config = open_json('./config/config.json')

# 初始化机器人
bot = Bot(token=config['token'])  # 默认采用 websocket
"""main bot"""
if not config['using_ws']:  # webhook
    # 当配置文件中'using_ws'键值为false时，代表不使用websocket
    # 此时采用webhook方式初始化机器人
    print(f"[BOT] using webhook at port {config['webhook_port']}")
    bot = Bot(cert=Cert(token=config['token'],
                        verify_token=config['verify_token'],
                        encrypt_key=config['encrypt_token']),
              port=config['webhook_port'])

# ChatGPT
openai.api_key = config['openai_key']
GPTmessage = []

@bot.command(regex=r'.*?.*')
async def chatgpt(msg:Message):
    GPTmessage.append(
        {
            "role": "user",
            "content": msg.content
        }
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=GPTmessage
    )

    # 机器人以回复的形式发送消息
    await msg.reply(completion.choices[0].message.content)

bot.run()