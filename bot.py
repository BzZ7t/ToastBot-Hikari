#/#/#/#/#/#/#/#/# ------> Imports
import asyncio
import os
import time

import hikari
import lightbulb
import miru
from dotenv import load_dotenv

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
                   'Says "pong!"')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong!")

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
@lightbulb.command("donate",
                   "Get my creator's Ko-Fi page!")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx):
    await ctx.respond("Keep these projects free without a premium subcription by supporting me on Ko-Fi! \nhttps://ko-fi.com/bzz7t")

bot.load_extensions_from("./plugins")
bot.run()
