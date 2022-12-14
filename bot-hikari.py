#/#/#/#/#/#/#/#/# ------> Imports
import random
import time
import os
import hikari
import lightbulb
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = lightbulb.BotApp(token=TOKEN)

@bot.listen(hikari.StartedEvent)#--------> When bot has started
async def startup(event):
    print("ToastBot has successfully started!\nIf you have unauthorised access to this bot, fuck you! <<<333")
     
#@bot.listen(hikari.GuildJoinEvent)#--------> When a user joins [UNFINISHED]
#async def memberjoin(event):
#    await event.respond("test")

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/-----> all cmds
@bot.command#-------------------> /[Exapmple]
@lightbulb.command('example',
                   'this is just an example of for /commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def example(ctx):

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
#============================================> /fun
@bot.command
@lightbulb.command("fun",
                   "Do all the **fun** stuff :D")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def fun(ctx):
    pass

@fun.child#----------------------------> /fun example
@lightbulb.command('example',
                   'example description')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def groupexample(ctx):
    print("This is just and example template for the /fun command group")

@fun.child#----------------------------> /fun toast-insults
@lightbulb.command('toast-insults',
                   'Make ToastBot reply with a toast-related insult')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toastinsult(ctx):
    my_file = open("strangeinsults.txt", "r",encoding="utf-8")
    content_list = my_file.readlines()
    await ctx.respond(str(content_list[random.randint(0,len(content_list)-1)]))


    
bot.run()
