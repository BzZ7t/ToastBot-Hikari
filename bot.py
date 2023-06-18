#/#/#/#/#/#/#/#/# ---> Imports
import asyncio
import json
import os
import random
from io import BytesIO
from time import time

import hikari
import lightbulb
import miru
import requests
from dotenv import load_dotenv
from PIL import Image

#/#/#/#/#/#/#/#/#/#/#/#/# ---> Loading the bot
if os.name != 'nt':
    import uvloop
    uvloop.install()
    os.system('clear')
    
else:
    os.system('cls')

print("Fix your code")
load_dotenv()
TOKEN = os.getenv("TOASTBOT")
bot = lightbulb.BotApp(token=TOKEN,
                       intents=hikari.Intents.ALL,
                       ignore_bots=True)
miru.install(bot)

#/#/#/#/#/#/#/# ---> Varibles
global dev_mode
dev_mode = False
toastbot_log = 1114676105312489554

#/#/#/#/#/#/#/#/#/#/#/# ---> Functions
async def get_json(server, key):
    with open(f'server_save/{server}.json', 'r', encoding='utf-8') as json_file:
        jsn = json.load(json_file)
    return jsn[key]

#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/#/# ---> Listeners

# When bot is starting
@bot.listen(hikari.StartingEvent)
async def startingup(event):
    await bot.rest.create_message(toastbot_log, "ToastBot is starting up....")

# When bot has started
@bot.listen(hikari.StartedEvent)
async def startup(event):
    await bot.rest.create_message(toastbot_log, "ToastBot is online!\nGood morning!")
    print('''                                   

            🍞🍞████████╗░█████╗░░█████╗░░██████╗████████╗██████╗░░█████╗░████████╗🍞🍞
            🍞🍞╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝🍞🍞
            🍞🍞░░░██║░░░██║░░██║███████║╚█████╗░░░░██║░░░██████╦╝██║░░██║░░░██║░░░🍞🍞
            🍞🍞░░░██║░░░██║░░██║██╔══██║░╚═══██╗░░░██║░░░██╔══██╗██║░░██║░░░██║░░░🍞🍞
            🍞🍞░░░██║░░░╚█████╔╝██║░░██║██████╔╝░░░██║░░░██████╦╝╚█████╔╝░░░██║░░░🍞🍞
            🍞🍞░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═════╝░░╚════╝░░░░╚═╝░░░🍞🍞
                                                                                        
''')
  
# When bot is powering down
@bot.listen(hikari.StoppingEvent)
async def poweringdown(event):
    await bot.rest.create_message(toastbot_log, "ToastBot is starting to powerdown...")
    await bot.rest.create_message(toastbot_log, "Powered down..\nGoodnight<3")

# When bot has powered down
@bot.listen(hikari.StoppedEvent)
async def powereddown(event):
    pass

# When an a command error has occured 
#TODO: I hate this, oh god how I hate this. YANDEV GET OUT MY HEEEAAAAADDDDD  
@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    print(event.exception)
    if isinstance(event.exception, lightbulb.errors.CommandNotFound):
        return None

    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond("Some arguments are missing: "+ ", ".join(event.exception.missing_options),
                                           flags=hikari.MessageFlag.EPHEMERAL)
        
    if isinstance(event.exception, lightbulb.errors.NotEnoughArguments):
        return await event.context.respond("Too many arguments were passed.",
                                           flags=hikari.MessageFlag.EPHEMERAL)

    if isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        return await event.context.respond(f"Hey! You gotta wait a bit before you do this command again!\nPlease wait {event.exception.retry_after:.0f} second/s before trying again.",
                                           flags=hikari.MessageFlag.EPHEMERAL)

    if isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
        return await event.context.respond(f"Hey! You don't have the permissions to do this here!\nPermission/s: `{event.exception.missing_perms}`",
                                           flags=hikari.MessageFlag.EPHEMERAL)

    if isinstance(event.exception, lightbulb.errors.BotMissingRequiredPermission):
        return await event.context.respond(f"I don't have the permissions to do that ^^'\nPermission/s: {event.exception.missing_perms}",
                                           flags=hikari.MessageFlag.EPHEMERAL)

    if isinstance(event.exception.__cause__, hikari.ForbiddenError):
        await event.context.respond("Something is missing perms or missed ids.\n this message will always show up no matter the error and I don't have a flying shit why\nIf you used a /mod command, you don't have the correct permissions -Zed",
                                    flags=hikari.MessageFlag.EPHEMERAL)
        raise event.exception

    if isinstance(event.exception, lightbulb.errors.CheckFailure):
        return None
    
    else:
        await event.context.respond("Ohhh no.. some error has happend and I'm not sure what it is o.o\nit might be something the following:\n - The command no workie.\n - The command is under maintenance (Goddamit Zed).\n - You didn't use the command correctly (/help to view command stuffs)",
                                        flags=hikari.MessageFlag.EPHEMERAL)
        raise event.exception

# When a member has joined a guild
@bot.listen(hikari.MemberCreateEvent)
async def welcome_join(event: hikari.MemberCreateEvent) -> None:
    user = event.member.mention
    try:
        await get_json(event.guild_id,'welcome_channel')
    
    except FileNotFoundError or KeyError:
        pass
    
    else:
        channel = await get_json(event.guild_id,'welcome_channel')
        txt = await get_json(event.guild_id,'welcome_txt')
        
        if isinstance(txt, list):
            txt = txt(random.randint(0,len(txt)-1))
            
        await bot.rest.create_message(channel, txt.format(user=user),
                                      user_mentions=True)

# When a member has left the guild       
@bot.listen(hikari.MemberDeleteEvent)
async def welcome_join(event: hikari.MemberDeleteEvent) -> None:
    user = event.user.mention
    try:
       await get_json(event.guild_id,'goodbye_channel')
        
    except FileNotFoundError or KeyError:
        pass
    
    else:
        channel = await get_json(event.guild_id,'goodbye_channel')
        txt = await get_json(event.guild_id,'goodbye_txt')
        
        if isinstance(txt, list):
            txt = txt(random.randint(0,len(txt)-1))
        
        await bot.rest.create_message(channel, txt.format(user=user),
                                      user_mentions=True)
            
        
# /ping
# Says "pong!" followed by bot latency
@bot.command
@lightbulb.command('ping',
                   'Says "pong!" followed by bot latency')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond(f"Pong!\nLatency: {ctx.bot.heartbeat_latency * 1000:,.0f}ms")

# /about
# Get info about ToastBot
@bot.command
@lightbulb.command('about',
                   'Get info about ToastBot')
@lightbulb.implements(lightbulb.SlashCommand)
async def help(ctx: lightbulb.Context):
    help_file = open('README.md', 'r', encoding='utf-8').read()
    await ctx.respond(help_file, flags=hikari.MessageFlag.SUPPRESS_EMBEDS)

# /donate
# Get my creator's Ko-Fi page!
@bot.command
@lightbulb.command("donate",
                   "Get my creator's Ko-Fi page!")
@lightbulb.implements(lightbulb.SlashCommand)
async def donate(ctx: lightbulb.Context):
    await ctx.respond("Keep these projects free without a premium subcription by supporting me on Ko-Fi! \nhttps://ko-fi.com/bzz7t\n\nthe /cat command uses Cat As A Service (https://cataas.com/#/) please check them out as well,\nhttps://www.buymeacoffee.com/kevinbalicot")

# /toaster
# Toast bread (not Toast) into Toast
@bot.command
@lightbulb.command("toaster",
                   "Toast bread (not Toast) into Toast")
@lightbulb.implements(lightbulb.SlashCommand)
async def toaster(ctx: lightbulb.Context):
    pass #TODO: What can I do here that would actually be interesting?

# /cat <gif[Yes,No]> <text> <filter[blur,mono,sepia,negative,paint,pixel]>
# get a random cat image from https://cataas.com/#/
@bot.command
@lightbulb.option('filter',
                  "add a filter (Keep in mind, some don't work with gifs)",
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
async def cat(ctx: lightbulb.Context):
    cat_filter = f'?filter={ctx.options.filter}'
    text = f"/says/{ctx.options.text}"
    gif = f"{ctx.options.gif}"
    fmat_type = "png"
    if ctx.options.text == "":
        text = ""
    if ctx.options.gif != "":
        fmat_type = "gif"
    cat_url = f"https://cataas.com/cat{gif}{text}{cat_filter}"
        
    await ctx.respond('Getting catto...')
    
    try:
        
        response = requests.get(cat_url, stream=True, timeout=5)
        response.raise_for_status()
        with Image.open(BytesIO(response.content)) as im:
            im.thumbnail((1024, 1024))
            im.save("temp_cat." + fmat_type, save_all=True)

        await ctx.edit_last_response(hikari.File(f"temp_cat.{fmat_type}", 'cat.png'))
        await ctx.edit_last_response(' ')
        
        if dev_mode != True:
            os.remove(f"temp_cat.{fmat_type}")
        
    except requests.exceptions.HTTPError:
        cat_url = f"https://cataas.com/cat{text}{cat_filter}"
        response = requests.get(cat_url, stream=True, timeout=5)
        response.raise_for_status()
        with Image.open(BytesIO(response.content)) as im:
            im.thumbnail((1024, 1024))
            im.save("temp_cat." + fmat_type, save_all=True)

        await ctx.edit_last_response(hikari.File(f"temp_cat.{fmat_type}", 'cat.png'))
        await ctx.edit_last_response(' ')

        await ctx.respond("You can't use this filter with a gif!\nI've given a still image instead",
                          flags=hikari.MessageFlag.EPHEMERAL)
        
    except requests.exceptions.ConnectionError:
        await ctx.respond('Nuuuuu\nCat as a Service is down right now... ;-;\nHelp support its creator!\nhttps://www.buymeacoffee.com/kevinbalicot')
    
        

# /suggest <text>
# give some feedback and/or suggestions to my creator!
@bot.command
@lightbulb.option('text',
                  'type the feedback/suggestion',
                  required=True)
@lightbulb.command('suggest',
                   'give some feedback and/or suggestions to my creator!')
@lightbulb.implements(lightbulb.SlashCommand)
async def suggest(ctx: lightbulb.Context):
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
# the .off has no particular funtion, lightbulb just doesn't recognise it haha
bot.load_extensions_from("./plugins")
bot.run()
