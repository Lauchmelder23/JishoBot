import discord
from discord.ext import commands
from utils import config
import os

bot = commands.Bot(config.get("prefix"))

@bot.event
async def on_ready():
    print("Loading cogs...", end=" ", flush=True)
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")
    print("Done!")
    
bot.run(config.get("token"))