import discord
from discord.ext import commands
from utils import jisho, interactive

class KanjiEmbed(interactive.InteractiveEmbed):
    REACTIONS = {
        "prev_kanji": "⬅️",
        "next_kanji": "➡️"
    }

    def __init__(self, parent, ctx, response):
        super(KanjiEmbed, self).__init__(parent.bot, ctx, 60.0)
        self.parent = parent
        self.owner = self.ctx.author
        self.response = response

        self.current_kanji = 0

    def prev_kanji(self):
        self.current_kanji -= 1
        if self.current_kanji < 0:
            self.current_kanji = self.response.entries - 1

    def next_kanji(self):
        self.current_kanji += 1
        if self.current_kanji >= self.response.entries:
            self.current_kanji = 0

    async def on_reaction(self, reaction, user):
        if reaction.emoji == KanjiEmbed.REACTIONS["prev_kanji"]:
            self.prev_kanji()
            await reaction.remove(user)

        if reaction.emoji == KanjiEmbed.REACTIONS["next_kanji"]:
            self.next_kanji()
            await reaction.remove(user)

    async def add_navigation(self, message):
        if self.response.entries > 1:
            await message.add_reaction(KanjiEmbed.REACTIONS["prev_kanji"])
            await message.add_reaction(KanjiEmbed.REACTIONS["next_kanji"])

    def make_embed(self):
        node = self.response.nodes[self.current_kanji]

        embed = discord.Embed(
            title = node.meaning,
            url = node.url,
            description = f"{node.strokes} strokes",
            colour = 0x56d926
        )

        if node.kun:
            embed.add_field(name="Kun", value="、 ".join(node.kun), inline=False)
        if node.on:
            embed.add_field(name="On", value="、 ".join(node.on), inline=False)

        embed.add_field(name=f"Radical: {node.radical[0]}", value=node.radical[1], inline=False)
        embed.set_thumbnail(url=node.image_url)
        embed.set_footer(text=f"Jōyō kanji (Grade {node.grade}) | JLPT level {node.jlpt}\t\t{self.current_kanji + 1}/{self.response.entries}")

        return embed

    async def on_close(self):
        self.parent.activeObjects.pop(self.ctx.channel.id)


class Kanji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activeObjects = {}

    @commands.command(name="kanji", description="Performs a Kanji search", usage="<kanji>", aliases=["k"])
    @commands.cooldown(1, 5)
    async def kanji(self, ctx, *, kanji: str = None):
        if kanji is None:
            embed = discord.Embed(
                title = "No search results",
                description = "The search returned nothing. Did you make a typo?",
                colour = 0x56d926
            )
            await ctx.send(embed=embed)
            return 

        embed = discord.Embed(
            title = "Loading...",
            description = "This might take a few seconds",
            colour = 0x56d926
        )
        message = await ctx.send(embed=embed)

        kanji = kanji[:5]
        response = jisho.JishoKanji(kanji)
        
        if response.entries < 1:
            embed = discord.Embed(
                title = "No search results",
                description = "The search returned nothing. Did you make a typo?",
                colour = 0x56d926
            )
            await message.edit(embed=embed)
            return 

        await message.delete()
        self.activeObjects[ctx.channel.id] = KanjiEmbed(self, ctx, response)
        await self.activeObjects[ctx.channel.id].show_embed()

def setup(bot):
    bot.add_cog(Kanji(bot))