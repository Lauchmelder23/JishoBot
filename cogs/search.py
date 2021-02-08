from inspect import currentframe
import discord
from discord.ext import commands
from utils import jisho, interactive

class SearchEmbed(interactive.InteractiveEmbed):
    REACTIONS = {
        "prev_page": "⬅️",
        "next_page": "➡️"
    }

    def __init__(self, parent, ctx, response):
        super(SearchEmbed, self).__init__(parent.bot, ctx, 60.0)
        self.parent = parent
        self.owner = self.ctx.author
        self.response = response

        self.current_page = 0

    def prev_page(self):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = self.response.size - 1

    def next_page(self):
        self.current_page += 1
        if self.current_page >= self.response.size:
            self.current_page = 0

    async def on_reaction(self, reaction, user):
        if reaction.emoji == SearchEmbed.REACTIONS["prev_page"]:
            self.prev_page()
            await reaction.remove(user)

        if reaction.emoji == SearchEmbed.REACTIONS["next_page"]:
            self.next_page()
            await reaction.remove(user)

    async def add_navigation(self, message):
        await message.add_reaction(SearchEmbed.REACTIONS["prev_page"])
        await message.add_reaction(SearchEmbed.REACTIONS["next_page"])

    def make_embed(self):
        node = self.response.nodes[self.current_page]
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
            text = f"{node.ftags} \t\t {self.current_page + 1}/{self.response.size}"
        )

        return embed

    async def on_close(self):
        self.parent.activeObjects.pop(self.ctx.channel.id)

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.activeObjects = {}

    @commands.command(name="search", description="Searches Jisho", usage="<query>", aliases=["s"])
    @commands.cooldown(1, 5)
    async def search(self, ctx: commands.Context, *, query: str = None):
        if query is None:
            embed = discord.Embed(
                title = "No search results",
                description = "The search returned nothing. Did you make a typo?",
                colour = 0x56d926
            )
            await ctx.send(embed=embed)
            return
        
        result = jisho.JishoResponse(query)
        if result.size == 0:
            embed = discord.Embed(
                title = "No search results",
                description = "The search returned nothing. Did you make a typo?",
                colour = 0x56d926
            )
            await ctx.send(embed=embed)
            return

        self.activeObjects[ctx.channel.id] = SearchEmbed(self, ctx, result)
        await self.activeObjects[ctx.channel.id].show_embed()

    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return # Suppress that annoying exception everytime someone is on cooldown
        
        raise error
    

def setup(bot: commands.Bot):
    bot.add_cog(Search(bot))