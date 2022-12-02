#/#/#/#/#/#/#/#/# ------> Imports
import random
import time
import hikari
import lightbulb

bot = lightbulb.BotApp(token='MTA0NjE1NzgwMTgyNDczNTMxMw.GpdOFU.UBb6SSLG8nqfo4FOi4ZKF0MNEO3xKm4avvtl7E')

@bot.listen(hikari.StartedEvent)
async def startup(event):
    print("ToastBot has successfully started!\nIf you have unauthorised access to this bot, fuck you! <<<333")

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/-----> all cmds
@bot.command#--------> info
@lightbulb.command("info",
                   "Get info about the bot!")
@lightbulb.implements(lightbulb.SlashCommand)
async def info(ctx):
    await ctx.respond("This is a *verrry* early version of ToastBot.\nif you somehow have normal access of this, please let my developer Zed (A.K.A BzZ7t) know :3")

@bot.command#---------> /ping
@lightbulb.command('ping',
                   'Says "pong!"')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong!")

@bot.command#------------> /time
@lightbulb.command("get-time",
                   "Says the current time")
@lightbulb.implements(lightbulb.SlashCommand)
async def timehere(ctx):
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)
    await ctx.respond(current_time)
    
#============================================> /fun
@bot.command
@lightbulb.command("fun",
                   "Do all the **fun** stuff :D")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def fun(ctx):
    pass

@fun.child
@lightbulb.command('strange-insults',
                   'Make ToastBot reply with a somewhat strange insult')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def strangeinsult(ctx):
    my_file = open("strangeinsults.txt", "r",encoding="utf-8")
    content_list = my_file.readlines()
    await ctx.respond(str(content_list[random.randint(0,len(content_list)-1)]))

bot.run()
