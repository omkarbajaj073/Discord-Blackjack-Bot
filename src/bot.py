import discord
from game import Game
from utils import play_msg


games = {}


client = discord.Client()
TOKEN = "OTEwMTkxOTY4NDMxMjQ3NDQw.YZPQUw.8lobqubSVdeeVL9OCWeL5BhKjfE"

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
                await game.hit(game.cur)
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
            
    elif content == "!split":
        if name in games:
            game = games[name]
            if game.active:
                await game.split()
            else:
                await channel.send("You don't have an active game " + name)
        else:
            await channel.send("You don't have an active game " + name)
            
    elif content == "!continue":
        if name in games:
            game = games[name]
            if game.active:
                game.can_split = False
                await channel.send("Continuing game with no split\n" + play_msg)
            else:
                await channel.send("You don't have an active game " + name)
        else:
            await channel.send("You don't have an active game " + name)
            
            
client.run(TOKEN)