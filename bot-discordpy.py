import random
import time
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN") 



intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("ToastBot has successfully started!\nIf you have unauthorised access to this bot, fuck you! <<<333")
    
client.run(TOKEN)