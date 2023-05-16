# The commands here will not be in the final runing of the bot
# Some commands are either not funtioning or are just for the sily
import asyncio
import os
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("dev")

@plugin.command
@lightbulb.command('test',
                   'test')
@lightbulb.implements(lightbulb.SlashCommand)
async def test(ctx):
    await ctx.respond("Test")
    
#/cute-checkrr command for playing around with Kohvi hehe
@plugin.command
@lightbulb.command('cute-checkrr',
                   'checks if you cute')
@lightbulb.implements(lightbulb.SlashCommand)
async def cute(ctx):
    user_ran = f"<@{ctx.author.id}>"
    if ctx.author.id == 1103121815838146684:
        await ctx.respond(f'Cmon {user_ran} we both know you are~')
    elif ctx.author.id == 592732403546587323:
        await ctx.respond(f'ewew nasty {user_ran} you nasty >~>')
    else:
        print("banana")
        
#supposted be to /interact violence but here is /violence. 
#currently doesn't work...
@plugin.command
@lightbulb.option('user',
                  'Who shall suffer?', required=True)
@lightbulb.command('violence',
                   "commit an act of violence to another user >:}")
@lightbulb.implements(lightbulb.SlashCommand)
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