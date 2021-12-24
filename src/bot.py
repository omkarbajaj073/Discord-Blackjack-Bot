import discord
import firebase_admin
from firebase_admin import db, credentials
from card import Card


'''
THIS IS THE MAIN FILE FOR THE BOT
'''

# Reference to database where user data is stored
cred_obj = credentials.Certificate('./discord-casino-bot-firebase-adminsdk-xctx7-e413fd8a52.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	    'databaseURL':'https://discord-casino-bot-default-rtdb.asia-southeast1.firebasedatabase.app/'
	})
ref = db.reference('/')

client = discord.Client()
TOKEN = "OTEwMTkxOTY4NDMxMjQ3NDQw.YZPQUw.8lobqubSVdeeVL9OCWeL5BhKjfE"

help_message = "Work in Progress."

@client.event
async def on_connect():
    print("Connected.")
    

@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await message.channel.send(help_message)

client.run(TOKEN)
