import discord
from discord import app_commands
from discord.ext import commands


class fun(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        
    @commands.tree.command(name="ping", 
                      description = 'Says "Pong!" with the amount of time(ms) it took!')
    async def ping(Interaction: discord.Interaction):
        await Interaction.response.send_message(f"Pong!\nThat took `{round(bot.latency * 1000)}ms` for me to respond!")
        
def setup(bot):
    bot.add_cog(fun(bot))