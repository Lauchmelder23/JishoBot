import discord
from discord.ext import commands
from utils import config

bot = commands.Bot(config.get("prefix"))

bot.run(config.get("token"))