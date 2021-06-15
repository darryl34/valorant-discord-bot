import discord

from utils import loadConfig, user
from discord.ext import commands
from parse import topWeapons

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = loadConfig.load("config.json")

    @commands.command()
    async def hello(self, ctx):
        """ Prints a hello message """
        await ctx.send(f"Hello {ctx.author.nick}")

    @commands.command()
    async def register(self, ctx, valID):
        """ Associates a user with their Valorant ID """
        formatted = valID.replace("#", "%23")
        if user.add(ctx.author.id, formatted):
            await ctx.send("Registered successfully!")

    @commands.command()
    async def top(self, ctx, discordUser: discord.Member=None):
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result = topWeapons.parse(valTag)

            embed = discord.Embed(title="Top Weapons", description="Displaying your top weapons statistics")
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            for elem in result:
                embed.add_field(name=elem[0], value="Kills: " + str(elem[2]) + "\tHS: " + str(elem[1][0]), inline=False)
            embed.set_footer(text="All stats calculated from Unrated matches")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(test(bot))