#/#/#/#/#/#/#/#/# ------> Imports
import asyncio
import os
import time

import hikari
import lightbulb
import miru
from dotenv import load_dotenv

print("Fix your code")
load_dotenv()
TOKEN = os.getenv("TOASTBOT")

bot = lightbulb.BotApp(token=TOKEN)
miru.install(bot)


@bot.listen(hikari.StartedEvent)#--------> When bot has started
async def startup(event):
    print('''                                   
                                                                                                     
            🍞🍞████████╗░█████╗░░█████╗░░██████╗████████╗██████╗░░█████╗░████████╗🍞🍞
            🍞🍞╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝🍞🍞
            🍞🍞░░░██║░░░██║░░██║███████║╚█████╗░░░░██║░░░██████╦╝██║░░██║░░░██║░░░🍞🍞
            🍞🍞░░░██║░░░██║░░██║██╔══██║░╚═══██╗░░░██║░░░██╔══██╗██║░░██║░░░██║░░░🍞🍞
            🍞🍞░░░██║░░░╚█████╔╝██║░░██║██████╔╝░░░██║░░░██████╦╝╚█████╔╝░░░██║░░░🍞🍞
            🍞🍞░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═════╝░░╚════╝░░░░╚═╝░░░🍞🍞
                                                                                        ''')
    

@bot.command#\--------> /ping
@lightbulb.command('ping',
                   'Says "pong!" followed by bot latency')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f"Pong!\nLatency: {ctx.bot.heartbeat_latency * 1000:,.0f}ms")

#TODO Unsure wether of not to remove this as it serves no purpose in its current state
@bot.command#----------------> /time
@lightbulb.command("get-time",
                   "Says the current time")
@lightbulb.implements(lightbulb.SlashCommand)
async def timehere(ctx):
    t = time.localtime()
    current_time = time.strftime("%I:%M %p", t)
    current_time_hour = time.strftime("%I", t)
    current_time_aftrm = time.strftime("%p", t)
    await ctx.respond("The current time in the UK is: "+current_time)
    if int(current_time_hour) >= 12 and current_time_aftrm == "PM":
        await ctx.respond("<@592732403546587323>! GO TO SLEEP!")   
        
@bot.command
@lightbulb.command('help',
                   'Get a list of all commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    helptxt = open("./README.md", "r") #TODO: Use this if possible
    print(helptxt)
    await ctx.respond(
'''# Current Commands
```
/fun: Do all the **fun** stuff :D
---> toast-insults: Make ToastBot reply with a toast-related insult
---> roll: Roll a dice

/interact: interact with other users!
---> violence: commit an act of violence to another user >:}
---> hug: give another user a hug!
---> boop: boop another user

/help: Get a list of all commands
/donate: Get my creator's Ko-Fi page!
```''')
        

@bot.command
@lightbulb.command("donate",
                   "Get my creator's Ko-Fi page!")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx):
    await ctx.respond("Keep these projects free without a premium subcription by supporting me on Ko-Fi! \nhttps://ko-fi.com/bzz7t")

bot.load_extensions_from("./plugins")
bot.run()
