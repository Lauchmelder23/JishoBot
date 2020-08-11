import discord
from discord.ext import commands
from utils import jisho

class JishoKanjiObject():
    def __init__(self, query, owner):
        self.response = jisho.JishoKanji(query)
        self.total_pages = self.response.entries
        self.page = 0
        self.owner = owner

    def prev(self):
        self.page -= 1
        if self.page < 0:
            self.page = self.total_pages - 1

    def next(self):
        self.page += 1
        if self.page >= self.total_pages:
            self.page = 0


class Kanji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activeObject = None
        self.latestMessage = 0

    async def createEmbed(self):
        response = self.activeObject.response
        node = response.nodes[self.activeObject.page]

        embed = discord.Embed(
            title = node.kanji,
            url = node.url,
            description = node.meaning,
            colour = 0x56d926
        )

        if node.kun:
            embed.add_field(name="Kun", value=", ".join(node.kun), inline=False)
        if node.on:
            embed.add_field(name="On", value=", ".join(node.on), inline=False)

        embed.set_footer(text=f"{self.activeObject.page + 1}/{self.activeObject.total_pages}")

        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if message.id != self.latestMessage:
            return

        if user == self.bot.user:
            return

        if user.id != self.activeObject.owner:
            return

        if reaction.me:
            if reaction.emoji == "⬅️":
                self.activeObject.prev()
                await reaction.remove(user)

            if reaction.emoji == "➡️":
                self.activeObject.next()
                await reaction.remove(user)

        embed = await self.createEmbed()
        await message.edit(embed=embed)

    @commands.command(name="kanji", description="Performs a Kanji search", usage="<kanji>", aliases=["k"])
    @commands.cooldown(1, 5)
    async def kanji(self, ctx, *, kanji: str = None):
        if kanji is None:
            return 

        self.activeObject = JishoKanjiObject(kanji, ctx.author.id)
        embed = await self.createEmbed()
        message = await ctx.send(embed=embed)
        self.latestMessage = message.id

        if self.activeObject.total_pages > 1:
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")

def setup(bot):
    bot.add_cog(Kanji(bot))