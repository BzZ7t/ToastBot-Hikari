#-------------> Imports
import asyncio
import random

import hikari
import lightbulb

plugin = lightbulb.Plugin("fun")

# '/fun' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("fun",
                   "Do all the **fun** stuff :D")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def fun(ctx):
    pass
    
# /fun toast-insults
# Make ToastBot reply with a toast-related insult
@fun.child
@lightbulb.command('toast-insults',
                   'Make ToastBot reply with a toast-related insult')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toastinsult(ctx: lightbulb.Context):
    insult = open("./plugins/assets/fun/toast-insults.txt", "r",encoding='utf-8').read().split("\n")
    await ctx.respond(random.choice(insult))

# /fun diceroll <number>
# Roll a dice (default is 6)
@fun.child 
@lightbulb.option('number',
                  'whats the highest number the dice could roll?', required=False, default=6)
@lightbulb.command('diceroll',
                   'Roll a dice (default is 6)')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def roll(ctx: lightbulb.Context):
    high_no = ctx.options.number
    
    try:
        high_no = int(high_no)
        await ctx.respond("You rolled a")
        await asyncio.sleep(0.25)
        await ctx.edit_last_response("You rolled a.")
        await asyncio.sleep(0.25)
        await ctx.edit_last_response("You rolled a..")
        await asyncio.sleep(0.25)
        await ctx.edit_last_response("You rolled a...")
        await asyncio.sleep(1)
        await ctx.edit_last_response(f"You rolled a **{random.randint(1, high_no)}**!")
    except ValueError:
        await ctx.respond("That is not a number, please try again")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again.")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again..")
        await asyncio.sleep(0.5)
        await ctx.edit_last_response("That is not a number, please try again...")
        await asyncio.sleep(1)
        await ctx.delete_last_response()

# /fun coinflip <guess[Heads,Tails]>
# flip a 50/50 coin!
@fun.child
@lightbulb.option('guess',
                  'Guess if its heads or tails!', required=False, default='None',
                  choices=[hikari.CommandChoice(name='Heads', value='Heads'),hikari.CommandChoice(name='Tails', value='Tails')])
@lightbulb.command('coinflip',
                   'flip a 50/50 coin!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def coinflip(ctx: lightbulb.Context):
    coin = random.choice(['Tails','Heads'])
    guess = ctx.options.guess
    
    await ctx.respond('The coin landed on')
    await asyncio.sleep(0.25)
    await ctx.edit_last_response('The coin landed on.')
    await asyncio.sleep(0.25)
    await ctx.edit_last_response('The coin landed on..')
    await asyncio.sleep(0.25)
    await ctx.edit_last_response('The coin landed on...')
    await asyncio.sleep(1)
    await ctx.edit_last_response(f'The coin landed on **{coin}**!')
    
    if guess != 'None':
        if guess == coin:
            await ctx.edit_last_response(f'The coin landed on **{coin}**!\nYou guessed correctly! (**{guess}**)')
        else:
            await ctx.edit_last_response(f'The coin landed on **{coin}**!\nYou guessed incorrectly (**{guess}**)')

# /fun 8ball <text>
# Shake a unique 8-ball
@fun.child
@lightbulb.option('text',
                  'enter somthing that the 8-ball will respond to',
                  required=True)
@lightbulb.command('8-ball',
                   'Shake a unique 8-ball')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def eightball(ctx: lightbulb.Context):
    user = ctx.author.mention
    message = ctx.options.text
    ball = open("./plugins/assets/fun/8ball.txt", "r",encoding='utf-8').read().split("\n")
    
    await ctx.respond(f"{user}: {message},\n{random.choice(ball)}")
    
# Loads the plugin
def load(bot):
    bot.add_plugin(plugin)
