@interact.child
@lightbulb.option('dodge',
                  "dodge another user's action")
@lightbulb.command('violence',
                   "today you chose violence")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def violence(ctx):
    dodge_result = "dodge"
    return dodge_result


#THIS FILE IS USED TO TEST A BUNCH OF RANDOM STUFF