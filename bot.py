#/#/#/#/#/#/#/#/# ------> Imports
from io import BytesIO
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
    pass #TODO: please make this really fucking complex with some secrets or some shit idk who do you take me for? a wish maker?

#---> /cat,
#-> Uses CAAS API to get a random image of a cat
@bot.command
@lightbulb.option('filter',
                  'add a filter',
                  required=False,
                  default="none",
                  choices=['blur','mono','sepia','negative','paint','pixel'])
@lightbulb.option('text',
                  'add some text to the image',
                  required=False,
                  default="",
                  )
@lightbulb.option('gif', #TODO: gif no workie, just shows first frame ffs
                  'send a cat gif? (does not work at the moment...)',
                  required=False,
                  default="",
                  choices=[hikari.CommandChoice(name="Yes", value="/gif"),
                           hikari.CommandChoice(name="No", value="")])
@lightbulb.command("cat",
                   "get a random cat image from https://cataas.com/#/")
@lightbulb.implements(lightbulb.SlashCommand)
async def cat(ctx):
    cat_filter = f'?filter={ctx.options.filter}'
    text = f"/says/{ctx.options.text}"
    if ctx.options.text == "":
        text = ""
    options = f"{ctx.options.gif}"
    cat_url = f"https://cataas.com/cat{options}{text}{cat_filter}"
    fmat_type = "png"
    if ctx.options.gif != "":
        fmat_type = "gif"

    response = requests.get(cat_url, stream=True, timeout=5)
    response.raise_for_status()

    with Image.open(BytesIO(response.content)) as im:
        im.thumbnail((1024, 1024))
        im.save("temp_cat." + fmat_type, save_all=True)

    await ctx.respond(hikari.File(f"temp_cat.{fmat_type}"))

    

bot.load_extensions_from("./plugins")
bot.run()
