import asyncio
import random
import time

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("interact")

# ----> '/interact' setup, note that the decription is not being used here, despite being added


@plugin.command
@lightbulb.command("interact",
                   "interact with other users!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def interact(ctx):
    pass

@interact.child
@lightbulb.option('dodge',
                  "dodge another user's action")
@lightbulb.command('violence',
                   "today you chose violence")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def violence(ctx):
    dodge_result = "dodge"
    return dodge_result

@interact.child
@lightbulb.option('user',
                  'Who shall suffer?')
@lightbulb.command('violence',
                   "today you chose violence")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def violence(ctx):
    user_ran = f"<@{ctx.author.id}>"
    user_hurt = ctx.options.user

    action = [f"{user_ran} decided to throw a stone at {user_hurt}"]
    action_end = [f"{user_ran} gave {user_hurt} a concussion"]
    action_dodged = [f"{user_hurt} dodged {user_ran}'s rock"]
    action_randm = random.randint(0, len(action)-1)
    dodge_randm = [random.randint(0, 2)]
    dodge_randm = 1

    await ctx.respond(action[action_randm])

    if dodge_randm == 1:
        await ctx.respond(f"{user_hurt} you have a chance to dodge it!" +
                          "quick! respond with `/interact dodge to dodge` the attack!")
        t1_start = time.perf_counter()
        async def dodge_get():
            active= True
            while active:
                print(time.perf_counter()-t1_start)
                if (time.perf_counter() - t1_start) >= 3:
                    if dodge_result.lower() == "dodge":
                        active = False
                        return True
                    else:
                        active = False
                        return False
                else:
                    dodge_result = hikari.events.message_events.GuildMessageCreateEvent
        #TODO: Listen to message for "dodge" from user_hurt
        dodge_result = await dodge_get()
        if dodge_result == True:
            await ctx.respond(action_dodged[action_randm])
        else:
            await ctx.respond("You failed to dodge ;-;")
            await ctx.respond(action_end[action_randm])
    else:
        await ctx.respond("they're not able to dodge this time")
        time.sleep(0.5)
        await ctx.edit_last_response("they're not able to dodge this time.")
        time.sleep(0.5)
        await ctx.edit_last_response("they're not able to dodge this time..")
        time.sleep(0.5)
        await ctx.edit_last_response("they're not able to dodge this time...")
        time.sleep(1)
        await ctx.respond(action_end[action_randm])


def load(bot):
    bot.add_plugin(plugin)
