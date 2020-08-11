import discord
from discord.ext import commands
from utils import jisho

class JishoObject():
    def __init__(self, query):
        self.response = jisho.JishoResponse(query)
        self.total_pages = self.response.entries
        self.page = 0

    def prev(self):
        self.page -= 1
        if self.page < 0:
            self.page = self.total_pages - 1

    def next(self):
        self.page += 1
        if self.page >= self.total_pages:
            self.page = 0

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.activeObject = None

    async def createEmbed(self):
        response = self.activeObject.response
        node = response.nodes[self.activeObject.page]
        embed = discord.Embed(
            title = node.japanese[0][0],
            url = f"https://jisho.org/word/{node.slug}",
            description = node.japanese[0][1],
            colour = 0x56d926
        )

        i = 1
        for sense in node.senses:
            embed.add_field(name=f"{i}. {sense.fenglish_definitions}", value=sense.fparts_of_speech, inline=False)
            i += 1

        if len(node.japanese) > 1:
            other = ""
            for word, reading in node.japanese[1:]:
                other += word
                if reading != "":
                    other += f"【{reading}】"
                other += "\n"
            embed.add_field(name="Other forms", value=other)


        embed.set_footer(
            text = f"{node.ftags} \t\t {self.activeObject.page + 1}/{self.activeObject.total_pages}"
        )

        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        if reaction.me:
            if reaction.emoji == "⬅️":
                pass


    @commands.command(name="search", description="Searches Jisho", usage="<query>", aliases=["s"])
    @commands.cooldown(1, 5)
    async def search(self, ctx: commands.Context, *, query: str = None):
        if query == None:
            return
        
        self.activeObject = JishoObject(query)
        embed = await self.createEmbed()
        message = await ctx.send(embed=embed)
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return # Suppress that annoying exception everytime someone is on cooldown
        
        raise error
    

def setup(bot: commands.Bot):
    bot.add_cog(Search(bot))