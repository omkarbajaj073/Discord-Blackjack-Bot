import discord
from game import Game
from utils import play_msg
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('TOKEN')

games = {}
client = discord.Client()


def commands(func):
    async def wrapper(name, channel):
        if name in games:
            game = games[name]
            if game.active:
                await func(game)
            else:
                await channel.send("You don't have an active game " + name)
        else:
            await channel.send("You don't have an active game " + name)
            
    return wrapper


@commands
async def hit(game):
    await game.hit(game.cur)

@commands
async def stay(game):
    await game.stay()
    
@commands
async def surrender(game):
    await game.surrender()
    
@commands
async def split(game):
    await game.split()
    
@commands
async def cont(game):
    await game.cont()
    
    
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
        await hit(name, channel)
            
    elif content == "!stay":    
        await stay(name, channel)

    elif content == "!surrender":
        await surrender(name, channel)
            
    elif content == "!split":
        await split(name, channel)
            
    elif content == "!continue":
        await cont(name, channel)
            

client.run(TOKEN)