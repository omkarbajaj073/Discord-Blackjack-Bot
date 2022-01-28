import discord
from game import Game
from dotenv import load_dotenv
from utils import help_msg
import os

'''
To run the bot, go to www.discord.com/developers and create a new application.
Copy the token and store it in a .env file.
'''
load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()

# server variables
games: dict[str, Game] = {}
default_bet: int = 500
default_start_balance: int = 10000

# decorator to wrap game functions
def commands(func):
    async def wrapper(name: str, channel: discord.channel):
        if name in games:
            game = games[name]
            if game.active:
                await func(game)
            else:
                await channel.send(f"You don't have an active game {name}.")
        else:
            await channel.send(f"You don't have an active game {name}")
            
    return wrapper


async def start_game(name: str, channel: discord.channel, bet: int = default_bet):
    
    if name in games: # check if user already has a game
        game = games[name]
        if game.active:
            await channel.send("You already have an active game " + name)
            return
        else: 
            game.channel = channel
    
    else: # create new game is user does not have a game account
        game = Game(channel, name, default_start_balance)
        games[name] = game
        await channel.send("Creating BJ account - starting balance is 10000 coins.")
    
    if game.balance < bet:
        await channel.send(f"Sorry, you don't have enough money to bet {bet} coins")
    else:
        await game.start_game(bet)  

@commands
async def hit(game: Game):
    await game.hit(game.cur)

@commands
async def stay(game: Game):
    await game.stay()
    
@commands
async def surrender(game: Game):
    await game.surrender()
    
@commands
async def split(game: Game):
    await game.split()
    
@commands
async def cont(game: Game):
    await game.cont()

async def balance(name: str, channel: discord.channel):
    if name in games:
        game = games[name]
        await channel.send(f"{name} has a balance of {game.balance}")
    else:
        await channel.send(f"{name} has never played a game on this server.")
        
async def set_option(content: str, channel: discord.channel):
    options = content.split()
    
    if len(options) == 1:
        await channel.send("Please enter a valid option you want to reset.")
    elif len(options) == 2:
        await channel.send("Please enter a valid value to reset the option.")
    elif len(options) > 3:
        await channel.send("Please enter only one value to reset the option.")
    
    else:        
        option = options[1]                
        reset = 0
        try:
            reset = int(options[2])
        except:
            await channel.send("Please enter a valid value to reset the option.")
            return
        
        if option == "stake": 
            global default_bet
            default_bet = reset
            await channel.send(f"Default stake reset to {default_bet}")
    
        elif option == "start-balance":
            global default_start_balance
            default_start_balance = reset
            await channel.send(f"Default starting balance reset to {default_start_balance}")
    
        else:
            await channel.send("Please enter a valid option you want to reset.")  
            
async def view(content: str, channel: discord.channel):
    opt = content.split()
    
    if len(opt) == 1:
        await channel.send("Please enter which default you want to view.")
    elif len(opt) > 2:
        await channel.send("Please enter only one option to view.")
    
    else:
        if opt[1] == "stake":
            await channel.send(f"Default stake - {default_bet}") 
        elif opt[2] == "start-balance":
            await channel.send(f"Default starting balance - {default_start_balance}")
        else:
            await channel.send("Please enter a valid option to view.")

async def reset_acc(name: str, channel: discord.channel):
    
    if name in games:
        game = games[name]
        if game.balance > 100:
            await channel.send(f"You have too much balance to reset your account {name}.")
            return
        
        game.balance = default_start_balance
        await channel.send(f"Your account has been reset. You have {game.balance} coins.")
    
    else:
        await channel.send("You don't have an account to reset.\n!help to find out how to use this bot.")  

    
@client.event
async def on_connect():
    print("Bot connected.")
    

@client.event
async def on_message(message: discord.Message):
    
    content: str = message.content
    channel: discord.channel = message.channel
    name: str = message.author.name
    
    if message.author == client.user:
        return   
    
    if content.startswith("!bj"):
        await channel.send(f"Starting blackjack with {name}.")
        com = content.split()
    
        if len(com) > 2:
            await channel.send("Please enter only one value for the stake.")
        if len(com) == 2:
            bet = int(com[1])
        else:
            bet = default_bet
            
        await start_game(name, channel, bet)
                    
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
        
    elif content.startswith("!set"):
        await set_option(content, channel)
        
    elif content.startswith("!view"):
        await view(content, channel)
        
    elif content == "!reset":
        await reset_acc(name, channel)
          
    elif content == "!help":
        await channel.send(embed=help_msg)
            

client.run(TOKEN)