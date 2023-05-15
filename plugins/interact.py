import asyncio
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("interact")

#---> Common Varibles 
dgg = False
#---> Common Functions
#TODO: UserFunc for simple commands with a gif #####################################################################################
async def simple_interaction(ctx, interaction):
    user_ran = f"<@{ctx.author.id}>"
    user_interact = ctx.options.user
    #TODO: File open when fstring found: open("./plugins/assets/interact/hug_list.txt", "r").read().split("\n")
    list = open(f"./plugins/assets/interact/{interaction}_list.txt", "r").read().split("\n")
    list_gif = open(f"./plugins/assets/interact/{interaction}_list_gif.txt", "r").read().split("\n")
    
    if ctx.options.gif == True:
        await ctx.respond(f"{list[random.randint(0,len(list))]}\n{list_gif[random.randint(0,len(list_gif))]}".format(user_ran = user_ran, user_interact = user_interact),
                          user_mentions=True)
    else:
        await ctx.respond({list[random.randint(0,len(list))]})
#####################################################################################################################################


# ----> '/interact' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def interact():
    pass

#---------------------------------> /interact hug 
@interact.child
@lightbulb.option('gif',
                  "add a gif to the message?", required=False, default=False,
                  choices=[hikari.CommandChoice(name='Yes', value=True),
                           hikari.CommandChoice(name='No', value=False)],
                  type=bool)
@lightbulb.option('user',
                  'Who would you like to hug?', required=True)
@lightbulb.command('hug',
                   'give another user a hug!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hug(ctx):
    await simple_interaction(ctx, interaction='hug')
        
@interact.child
@lightbulb.option('gif',
                  "add a gif to the message? ('Yes/No' or 'y/n')", required=False, default=False,
                  choices=[hikari.CommandChoice(name='Yes', value=True),
                           hikari.CommandChoice(name='No', value=False)],
                  type=bool)
@lightbulb.option('user',
                  'Who would you like to boop?')
@lightbulb.command('boop',
                   'boop another user.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def boop(ctx):
    simple_interaction(ctx, interaction='boop')
        
#-----------> More complex interactions,
#---------------------------------> /interact violence user:
@interact.child
@lightbulb.option('user',
                  'Who shall suffer?', required=True)
@lightbulb.command('violence',
                   "commit an act of violence to another user >:}")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def violence(ctx):
    user_ran = f"<@{ctx.author.id}>"
    user_interact = ctx.options.user
    action = [f"{user_ran} decided to throw a stone at {user_interact}"]
    action_end = [f"{user_ran} gave {user_interact} a concussion"]
    action_dodged = [f"{user_interact} dodged {user_ran}'s rock"]
    action_randm = random.randint(0, len(action)-1)
    dodge_randm = [random.randint(0, 2)]
    dodge_randm = 1
    
                    
    #TODO: Fix this goddamn button

    class dodge_btn(miru.View): 
            @miru.button(label='Dodge!', style=hikari.ButtonStyle.PRIMARY)
            async def btn_dodge(self, button: miru.button, ctx: miru.context) -> None:
                global ddg
                ddg = True
                await ctx.respond(action_dodged[action_randm],user_mentions=True)
                
                
                
                
    await ctx.respond(action[action_randm])
    if dodge_randm == 1:
        view = dodge_btn(timeout=4)
        message = await ctx.respond(f"{user_interact} you have a chance to dodge it!\n" +
                    "quick! press the button below to dodge the attack!", components=view.build(), user_mentions=True)
        
        t1_start = time.perf_counter()
        active = True
        view.start(message)
        while active:
            print(time.perf_counter()-t1_start)
            if ddg == True:
                active = False
            elif (time.perf_counter() - t1_start) >= 3:
                active = False
                await ctx.edit_last_response(f"{user_interact} had a chance to dodge but failed ;-;")
                await ctx.respond(action_end[action_randm])
            
        
        
    else:
        await ctx.respond("they're not able to dodge this time")
        asyncio.sleep(0.5)
        await ctx.edit_last_response("they're not able to dodge this time.")
        asyncio.sleep(0.5)
        await ctx.edit_last_response("they're not able to dodge this time..")
        asyncio.sleep(0.5)
        await ctx.edit_last_response("they're not able to dodge this time...")
        asyncio.sleep(1)
        await ctx.respond(action_end[action_randm], user_mentions=True)

def load(bot):
    bot.add_plugin(plugin)
