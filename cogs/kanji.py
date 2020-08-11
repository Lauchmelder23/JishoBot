import discord
from discord.ext import commands
from utils import jisho

class Kanji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kanji", description="Performs a Kanji search", usage="<kanji>", aliases=["k"])
    @commands.cooldown(1, 5)
    async def kanji(self, ctx, *, kanji: str = None):
        if kanji is None:
            return 

        response = jisho.JishoKanji(kanji)
        await ctx.send(response.entries)

def setup(bot):
    bot.add_cog(Kanji(bot))