#/#/#/#/#/#/#/#/# ------> Imports
import random
import time
import hikari
import lightbulb

bot = lightbulb.BotApp(token='MTA0NjE1NzgwMTgyNDczNTMxMw.GpdOFU.UBb6SSLG8nqfo4FOi4ZKF0MNEO3xKm4avvtl7E')

@bot.listen(hikari.StartedEvent)
async def startup(event):
    print("ToastBot has successfully started!")

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/-----> all cmds
@bot.command#------------> /ping
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
@lightbulb.command('strange-insults',
                   'Make ToastBot reply with a somewhat strange insult')
@lightbulb.implements(lightbulb.SlashCommand)
async def strangeinsult(ctx):
    my_file = open("strangeinsults.txt", "r",encoding="utf-8")
    content_list = my_file.readlines()
    await ctx.respond(str(content_list[random.randint(0,len(content_list)-1)]))

bot.run()
