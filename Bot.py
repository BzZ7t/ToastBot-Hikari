import hikari
import lightbulb
import random

bot = lightbulb.BotApp(token='MTA0NjE1NzgwMTgyNDczNTMxMw.GpdOFU.UBb6SSLG8nqfo4FOi4ZKF0MNEO3xKm4avvtl7E')

@bot.listen(hikari.StartedEvent)
async def startup(event):
    print("ToastBot has successfully started!")

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/-----> all cmds
@bot.command#\--------> /ping
@lightbulb.command('ping', 'Says "pong!"')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond("Pong!")
#============================================> /fun
@bot.command
@lightbulb.command('playful-insults', 'Make ToastBot reply with a funny insult')
@lightbulb.implements(lightbulb.SlashCommand)
async def playfulinsult(ctx):
    playfulinsult = open("playfulinsult.txt", "r")
    await ctx.respond(random.choice(playfulinsult))


bot.run()