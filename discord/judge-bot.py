import discord
import asyncio
import random

channelIds = {
    'bot-test': 696989502153162773
}

client = discord.Client()

@client.event
async def on_ready():
    print('ready:', client.user.name + '(' + str(client.user.id) + ')')
    game = discord.Game("마더 법규를 준수")
    await client.change_presence(status=discord.Status.online, activity=game)
    # 등장 메시지
    botTestChannel = client.get_channel(channelIds['bot-test'])
    await botTestChannel.send('마더 법규를 준수하십씨오')

@client.event
async def on_message(message):
    if not message.author.bot and message.channel.id == channelIds['bot-test']:
        if message.content.startswith("!안녕"):
            await message.channel.send("안녕하세요.")
        else:
            await message.channel.send("정숙해 주시기 바람미따.")
            print(message)
            print(message.author)
            print(message.channel)
        


# def executeCommand(message):
#     if message.content.startswith("!안녕"):
#         await message.channel.send("안녕하세요.")

# def react(message):
#     print(message)
#     print(message.author)
#     print(message.channel)

client.run("newtokenmustbehere")

