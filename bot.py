import discord

'''
THIS IS THE MAIN FILE FOR THE BOT
'''

client = discord.Client()
TOKEN = "OTEwMTkxOTY4NDMxMjQ3NDQw.YZPQUw.8lobqubSVdeeVL9OCWeL5BhKjfE"

help_message = "Work in Progress."

@client.event
async def on_connect():
    print("Connected.")
    

@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await client.send_message(message.channel, help_message)

