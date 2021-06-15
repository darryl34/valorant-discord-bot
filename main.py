import os

from utils import loadConfig
from discord.ext import commands

config = loadConfig.load("config.json")

bot = commands.Bot(
    command_prefix=config["prefix"]
)

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(config["token"])