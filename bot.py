#/#/#/#/#/#/#/#/# ------> Imports
import asyncio
import json
import os
import time
from io import BytesIO

import hikari
import lightbulb
import miru
import requests
from dotenv import load_dotenv
from PIL import Image

print("Fix your code")
load_dotenv()
TOKEN = os.getenv("TOASTBOT")

bot = lightbulb.BotApp(token=TOKEN, default_enabled_guilds=(1011278408770146374,1105527442468253789))
miru.install(bot)

def get_welcome(ctx):
    server = ctx.get_guild().id
    with open(f'server_save/{server}/welcome.json', 'r', encoding='utf-8') as json_file:
        jsn_welcome = json.load(json_file)
    return jsn_welcome

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
    
@bot.listen(hikari.MemberCreateEvent)
async def welcome_join(ctx):
    try:
        file = get_welcome(ctx)
        await bot.rest.create_message(file['welcome_channel'], file['welcome_txt'])
        
    except FileNotFoundError:
        pass
    

@bot.command#\--------> /ping
@lightbulb.command('ping',
                   'Says "pong!" followed by bot latency')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f"Pong!\nLatency: {ctx.bot.heartbeat_latency * 1000:,.0f}ms")

@bot.command
@lightbulb.command('help',
                   'Get a list of all commands')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx):
    help_file = open('README.md', 'r', encoding='utf-8').read()
    await ctx.respond(help_file, flags=hikari.MessageFlag.SUPPRESS_EMBEDS)

@bot.command
@lightbulb.command("donate",
                   "Get my creator's Ko-Fi page!")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx):
    await ctx.respond("Keep these projects free without a premium subcription by supporting me on Ko-Fi! \nhttps://ko-fi.com/bzz7t\n\nthe /cat command uses Cat As A Service (https://cataas.com/#/) please check them out as well,\nhttps://www.buymeacoffee.com/kevinbalicot")

@bot.command
@lightbulb.command("toaster",
                   "Toast bread (not Toast) into Toast")
@lightbulb.implements(lightbulb.SlashCommand)
async def toaster(ctx):
    pass #TODO: What can I do here that would actually be interesting?

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
                  'send a cat gif?',
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
    try:
        response = requests.get(cat_url, stream=True, timeout=5)
        response.raise_for_status()
        with Image.open(BytesIO(response.content)) as im:
            im.thumbnail((1024, 1024))
            im.save("temp_cat." + fmat_type, save_all=True)

        await ctx.respond(hikari.File(f"temp_cat.{fmat_type}"))
        
    except requests.exceptions.ConnectionError:
        await ctx.respond('Nuuuuu\nCat as a Service is down right now... ;-;\nHelp support its creator!\nhttps://www.buymeacoffee.com/kevinbalicot', flags=hikari.MessageFlag.EPHEMERAL)

@bot.command
@lightbulb.option('text',
                  'type the feedback/suggestion',
                  required=True)
@lightbulb.command('suggest',
                   'give some feedback and/or suggestions to my creator!')
@lightbulb.implements(lightbulb.SlashCommand)
async def suggest(ctx):
    user = ctx.author.id
    username = ctx.author
    sugg = ctx.options.text
    try:
        file = open(f'feedbacksuggestions/{user}_feedback.txt', 'r', encoding='utf-8')
        await ctx.respond('You have already made a suggestion,\nplease let Zed know if you made a mistake with your suggestion', flags=hikari.MessageFlag.EPHEMERAL)
        print(f'Possible suggest error by {username}')
        
    except FileNotFoundError:
        file = open(f'feedbacksuggestions/{user}_feedback.txt', 'w', encoding='utf-8')
        file.write(f'{sugg}\nby {username}')
        await ctx.respond(f"Thank you for your suggestion {username.mention}!\nIt's greatly appriciated :>\n```{sugg}```")
        

# Any plugin with the extention .py.off will not be implemented
# the .off has no particular funtion, lightbulb just doesn't recognise it
bot.load_extensions_from("./plugins")
bot.run()
