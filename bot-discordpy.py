import os
import random
import time

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="Toast", intents = discord.Intents.all())
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN") 

@bot.event
async def on_ready():
    print('''
            🍞🍞████████╗░█████╗░░█████╗░░██████╗████████╗██████╗░░█████╗░████████╗🍞🍞
            🍞🍞╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝🍞🍞
            🍞🍞░░░██║░░░██║░░██║███████║╚█████╗░░░░██║░░░██████╦╝██║░░██║░░░██║░░░🍞🍞
            🍞🍞░░░██║░░░██║░░██║██╔══██║░╚═══██╗░░░██║░░░██╔══██╗██║░░██║░░░██║░░░🍞🍞
            🍞🍞░░░██║░░░╚█████╔╝██║░░██║██████╔╝░░░██║░░░██████╦╝╚█████╔╝░░░██║░░░🍞🍞
            🍞🍞░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═════╝░░╚════╝░░░░╚═╝░░░🍞🍞''')
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
        
@bot.tree.command(name="ping", 
                  description = 'Says "Pong!"')
async def ping(Interaction: discord.Interaction):
    await Interaction.response.send_message(f"Pong!")
    
@bot.tree.command(name="strange insults", 
                  description = 'Says "Pon')
async def ping(Interaction: discord.Interaction):
    await Interaction.response.send_message(f"Pong!")
    
bot.run(TOKEN)
