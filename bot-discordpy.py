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
            🍞🍞░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═════╝░░╚════╝░░░░╚═╝░░░🍞🍞
            ''')
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
        
@bot.tree.command(name="ping", 
                  description = 'Says "Pong!" with the amount of time(ms) it took!')
async def ping(Interaction: discord.Interaction):
    await Interaction.response.send_message(f"Pong!\nThat took `{round(bot.latency * 1000)}ms` for me to respond!")
    
@bot.tree.command(name="toast-insults", 
                  description = 'Make ToastBot reply with a toast-related insult')
async def toastinsults(Interaction: discord.Interaction):
    my_file = open("strangeinsults.txt", "r",encoding="utf-8")
    content_list = my_file.readlines()
    await Interaction.response.send_message(str(content_list[random.randint(0,len(content_list)-1)]))
    
@bot.tree.command(name="time", 
                  description = 'Says the current time (Currently in uk)')
async def timecmd(Interaction: discord.Interaction):
    t = time.localtime()
    time_get = time.strftime("%I:%M %p", t)
    time_hour = time.strftime("%I", t)
    time_aftrm = time.strftime("%p", t)
    await Interaction.response.send_message("The current time in the UK is: "+time_get)
    if int(time_hour) >= 12 and time_aftrm == "PM":
        await Interaction.response.send_message("<@592732403546587323>! GO TO SLEEP!")
    
bot.run(TOKEN)
