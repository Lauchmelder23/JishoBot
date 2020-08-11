import discord
from discord.ext import commands
from utils import jisho

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="search", description="Searches Jisho", usage="<query>", aliases=["s"])
    @commands.cooldown(1, 5)
    async def search(self, ctx: commands.Context, *, query: str = None):
        if query == None:
            return
        
        response = jisho.query(query)
        await ctx.send(response["data"][0]["slug"])

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass # Suppress that annoying exception everytime someone is on cooldown
        
    

def setup(bot: commands.Bot):
    bot.add_cog(Search(bot))