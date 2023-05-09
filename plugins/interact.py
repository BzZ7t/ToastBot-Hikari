import asyncio
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("interact")

#---> Common Varibles 
global ddg
dgg = False
#---> Common Functions
#TODO: UserFunc for simple commands with a gif #####################################################################################
async def simple_action(ctx):
    user_ran = f"<@{ctx.author.id}>"
    user_interact = ctx.options.user
    
    #TODO: File open when fstring found: open("./plugins/assets/interact/hug_list.txt", "r").read().split("\n")
    boop_list = [f"{user_ran} test1 for {user_interact}",
              f"{user_ran} test2 for {user_interact}"]
    boop_list_gif = open("./plugins/assets/interact/boop_list_gif.txt", "r").read().split("\n")
    
    if ctx.options.gif == "y" or ctx.options.gif.lower() == "yes":
        await ctx.respond(f"{boop_list[random.randint(0,len(boop_list))]} \n {boop_list_gif[random.randint(0,len(boop_list_gif))]}")
    else:
        await ctx.respond({boop_list[random.randint(0,len(boop_list))]})
#####################################################################################################################################


# ----> '/interact' setup, note that the decription is not being used here, despite being added
@plugin.command
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def interact():
    pass

#---------------------------------> /interact violence user:
@interact.child
@lightbulb.option('user',
                  'Who shall suffer?')
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
    
                    
    #TODO: Fix this goddamn button: wont return ddg = True

    class dodge_btn(miru.View): 
            @miru.button(label='Dodge!', style=hikari.ButtonStyle.PRIMARY)
            async def btn_dodge(self, button: miru.button, ctx: miru.context) -> None:
                global ddg
                ddg = True
                await ctx.respond(action_dodged[action_randm])
                
                
                
                
    await ctx.respond(action[action_randm])
    if dodge_randm == 1:
        view = dodge_btn(timeout=4)
        message = await ctx.respond(f"{user_interact} you have a chance to dodge it!\n" +
                    "quick! press the button below to dodge the attack!", components=view.build())
        
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
        await ctx.respond(action_end[action_randm])

#---------------------------------> /interact hug 
@interact.child
@lightbulb.option('gif',
                  "add a gif to the message? ('Yes/No' or 'y/n')")
@lightbulb.option('user',
                  'Who would you like to hug?')
@lightbulb.command('hug',
                   'give another user a hug!')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hug(ctx):
    user_ran = f"<@{ctx.author.id}>"
    user_interact = ctx.options.user
    #TODO: File open when fstring found: open("./plugins/assets/interact/hug_list.txt", "r").read().split("\n")
    hug_list = [f"{user_ran} test1 for {user_interact}",
              f"{user_ran} test2 for {user_interact}"]
    hug_list_gif = open("./plugins/assets/interact/hug_list_gif.txt", "r").read().split("\n")
    
    if ctx.options.gif == "y" or ctx.options.gif.lower() == "yes":
        await ctx.respond(f"{hug_list[random.randint(0,len(hug_list))]} \n {hug_list_gif[random.randint(0,len(hug_list_gif))]}")
    else:
        await ctx.respond({hug_list[random.randint(0,len(hug_list))]})
        
@interact.child
@lightbulb.option('gif',
                  "add a gif to the message? ('Yes/No' or 'y/n')")
@lightbulb.option('user',
                  'Who would you like to boop?')
@lightbulb.command('boop',
                   'boop another user.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def hug(ctx):
    user_ran = f"<@{ctx.author.id}>"
    user_interact = ctx.options.user
    #TODO: File open when fstring found: open("./plugins/assets/interact/hug_list.txt", "r").read().split("\n")
    boop_list = [f"{user_ran} test1 for {user_interact}",
              f"{user_ran} test2 for {user_interact}"]
    boop_list_gif = open("./plugins/assets/interact/boop_list_gif.txt", "r").read().split("\n")
    
    if ctx.options.gif == "y" or ctx.options.gif.lower() == "yes":
        await ctx.respond(f"{boop_list[random.randint(0,len(boop_list))]} \n {boop_list_gif[random.randint(0,len(boop_list_gif))]}")
    else:
        await ctx.respond({boop_list[random.randint(0,len(boop_list))]})
        

def load(bot):
    bot.add_plugin(plugin)
