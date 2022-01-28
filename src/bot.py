import discord
from game import Game
from dotenv import load_dotenv
import os


games = {}


load_dotenv()
client = discord.Client()
TOKEN = os.getenv('TOKEN')

@client.event
async def on_connect():
    print("Bot connected.")
    

@client.event
async def on_message(message):
    content = message.content
    channel = message.channel
    name = message.author.name
    if message.author == client.user:
        return
    
    if content == "!bj":
        await channel.send("Starting blackjack with " + name)
        if name in games:
            game = games[name]
            if game.active:
                await channel.send("You already have an active game " + name)
            else:
                game.channel = channel
                await game.start_game()
        else:
            game = Game(channel, name)
            games[name] = game
            await game.start_game()
            
    elif content == "!hit":
        if name in games:
            game = games[name]
            if game.active:
                await game.hit()
            else:
                await channel.send("You don't have an active game " + name)
        else:
            await channel.send("You don't have an active game " + name)
            
    elif content == "!stay":
        if name in games:
            game = games[name]
            if game.active:
                await game.stay()
            else:
                await channel.send("You don't have an active game " + name)
        else:
            await channel.send("You don't have an active game " + name)

    elif content == "!surrender":
        if name in games:
            game = games[name]
            if game.active:
                await game.surrender()
            else:
                await channel.send("You don't have an active game " + name)
        else:
            await channel.send("You don't have an active game " + name)
            
            
client.run(TOKEN)