#/#/#/#/#/#/#/#/# ------> Imports
import asyncio
import os
import time

import hikari
import lightbulb
import miru
import requests
from dotenv import load_dotenv
from PIL import Image

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
    await ctx.respond("Keep these projects free without a premium subcription by supporting me on Ko-Fi! \nhttps://ko-fi.com/bzz7t\n\nthe /cat command uses Cat As A Service (https://cataas.com/#/) please check them out as well,\nhttps://www.buymeacoffee.com/kevinbalicot ")

@bot.command
@lightbulb.command("toaster",
                   "Toast bread (not Toast) into Toast")
@lightbulb.implements(lightbulb.SlashCommand)
async def toaster(ctx):
    channel_id = ctx.message.channel_id
    user_ran = f"<@{ctx.author.id}>"
    toast_list = ["https://www.collinsdictionary.com/images/full/toast_102709511.jpg",
                  ]
    
    await ctx.respond("Toasting bread... Please wait...")
    await asyncio.sleep(3)
    await ctx.respond(f"{user_ran}, Your Toast is ready!", user_mentions=True)
    #await bot.rest.create_message(channel_id, content=toast_list[0]) #TODO: No workie, pls make seperate message without replying to last

#---> /cat,
#-> Uses CAAS API to get a random image of a cat
@bot.command
@lightbulb.option('text',
                  'add some text to the image',
                  required=False,
                  default="",
                  )
@lightbulb.option('gif',
                  'send a cat gif? (unsure if this works...)',
                  required=False,
                  default="",
                  choices=[hikari.CommandChoice(name="Yes", value="/gif"),
                           hikari.CommandChoice(name="No", value="")])
@lightbulb.command("cat",
                   "get a random cat image from https://cataas.com/#/")
@lightbulb.implements(lightbulb.SlashCommand)
async def cat(ctx):
    text = f"/says/{ctx.options.text}"
    if ctx.options.text == "":
        text = ""
    options = f"{ctx.options.gif}"
    cat_url = f"https://cataas.com/cat{options}{text}"
    fmat_type = "png"
    if ctx.options.gif != "":
        fmat_type = "gif"
        
    with Image.open(requests.get(cat_url, stream=True).raw) as im:
        im.thumbnail((1024,1024))
        im.save(f"temp_cat" + "."+fmat_type, fmat_type.upper())
    
    await ctx.respond(hikari.File(f"temp_cat.{fmat_type}"))




bot.load_extensions_from("./plugins")
bot.run()
