import discord
from game import Game
from dotenv import load_dotenv
from utils import default_bet
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

async def balance(name, channel):
    if name in games:
        game = games[name]
        await channel.send(f"{name} has a balance of {game.balance}")
    else:
        await channel.send(f"{name} has never played a game on this server.")
    
    
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
        com = content.split()
        if len(com) == 2:
            bet = com[1]
        else:
            bet = default_bet
        if name in games:
            game = games[name]
            if game.active:
                await channel.send("You already have an active game " + name)
            else:
                game.channel = channel
        else:
            game = Game(channel, name)
            games[name] = game
            await channel.send("Creating BJ account - starting balance is 10000.")
        if game.balance < bet:
            await channel.send("Sorry, you don't have enough money to bet " + str(bet))
        else:
            await game.start_game(bet)        
                    
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
        
    elif content == "!balance":
        await balance(name, channel)
        
            

client.run(TOKEN)