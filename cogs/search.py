import discord
from discord.ext import commands

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="search", description="Searches Jisho", usage="<query>", aliases=["s"])
    @commands.cooldown(1, 5)
    async def search(self, ctx: commands.Context, *, query: str = None):
        if query == None:
            return
        
        await ctx.send(query)
    

def setup(bot: commands.Bot):
    bot.add_cog(Search(bot))