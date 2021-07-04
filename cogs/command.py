import discord

from utils import loadConfig, user
from discord.ext import commands
from parse import overview, match

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = loadConfig.load("config.json")

    @commands.command()
    async def hello(self, ctx):
        """ Prints a hello message """
        await ctx.send(f"Hello {ctx.author.nick}")

    @commands.command()
    async def ping(self, ctx):
        """ Replies to you if online """
        await ctx.send("Pong! If a command doesn't work, it's probably broken :)")

    @commands.command()
    async def register(self, ctx, valID):
        """
            Usage: `register user#1234
        """
        noSpaces = valID.replace(" ", "")
        formatted = noSpaces.replace("#", "%23")
        if user.add(str(ctx.author.id), formatted):
            await ctx.send("Registered successfully!")
        else:
            await ctx.send("User already registered!")


    @commands.command()
    async def top(self, ctx, discordUser: discord.Member=None):
        """ Displays your top weapons """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result = overview.getTopWeapons(valTag)

            embed = discord.Embed(title="Top Weapons", description="Displaying your top weapons statistics")
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            for elem in result:
                embed.add_field(name=elem[0], value="Kills: " + str(elem[2]) + "    HS: " + str(elem[1][0]), inline=False)
            embed.set_footer(text="All stats calculated from Unrated matches")
            await ctx.send(embed=embed)


    @commands.command()
    async def rank(self, ctx, discordUser: discord.Member=None):
        """ Kinda self-explanatory tbh """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            await ctx.send(overview.getRank(valTag))

    @commands.command(aliases=['lu'])
    async def lastUnrated(self, ctx, discordUser: discord.Member=None):
        """ Gets data about your most recent unrated match """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            displayMessage = ""
            match = overview.getRecentUnrated(valTag)
            if match.getResult():
                displayMessage = "Match Won!"
            else:
                displayMessage = "Match Lost!"

            embed = discord.Embed(description=displayMessage)
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            embed.add_field(name="Map", value=match.getMap(), inline=True)
            embed.add_field(name="Agent Played", value=match.getAgent(), inline=True)
            embed.add_field(name="Score", value=match.getScore(), inline=True)
            embed.add_field(name="K/D/A", value=match.getKDA(), inline=True)
            embed.add_field(name="Avg. Damage", value=match.getADR(), inline=True)
            embed.add_field(name="Headshot %", value=match.getHS(), inline=True)
            embed.set_footer(text=discordUser.nick + "'s most recent match")
            await ctx.send(embed=embed)

    @commands.command(aliases=['lc'])
    async def lastComp(self, ctx, discordUser: discord.Member=None):
        """ Gets data about your most recent competitive match """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            displayMessage = ""
            match = overview.getRecentComp(valTag)
            if match.getResult():
                displayMessage = "Match Won!"
            else:
                displayMessage = "Match Lost!"

            embed = discord.Embed(description=displayMessage)
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            embed.add_field(name="Map", value=match.getMap(), inline=True)
            embed.add_field(name="Agent Played", value=match.getAgent(), inline=True)
            embed.add_field(name="Score", value=match.getScore(), inline=True)
            embed.add_field(name="K/D/A", value=match.getKDA(), inline=True)
            embed.add_field(name="Avg. Damage", value=match.getADR(), inline=True)
            embed.add_field(name="Headshot %", value=match.getHS(), inline=True)
            embed.set_footer(text=discordUser.nick + "'s most recent match")
            await ctx.send(embed=embed)


    @commands.command(aliases=['f'])
    async def friends(self, ctx, discordUser: discord.Member=None):
        """ Displays list of most played with people """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result, totalTime = overview.getTeammates(valTag)

            embed = discord.Embed(title="Most played with")
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            for elem in result:
                embed.add_field(name=elem[0], value=str(elem[1]) + " Win Rate: " + str(elem[2]),
                                inline=False)
            # embed.set_footer(text="All stats calculated from Unrated matches")
            embed.set_footer(text="Execution time: " + str(totalTime))
            await ctx.send(embed=embed)


    @commands.command(aliases=['cf'])
    async def compfriends(self, ctx, discordUser: discord.Member = None):
        """ Displays list of most played with people """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result, totalTime = overview.getTeammates(valTag, True)

            embed = discord.Embed(title="Most played with")
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            for elem in result:
                embed.add_field(name=elem[0], value=str(elem[1]) + " Win Rate: " + str(elem[2]),
                                inline=False)
            # embed.set_footer(text="All stats calculated from Competitive matches")
            embed.set_footer(text="Execution time: " + str(totalTime))
            await ctx.send(embed=embed)


    @commands.command(aliases=['r5u'])
    async def recent5u(self, ctx, discordUser: discord.Member=None):
        """ Displays last five games win streak """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result = overview.getFiveUnrated(valTag)
            embed = discord.Embed(description="Win Streak")
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            embed.add_field(name="Last 5:", value=str(result))
            embed.set_footer(text="All stats calculated from Unrated matches")
            await ctx.send(embed=embed)

    @commands.command(aliases=['r5c'])
    async def recent5c(self, ctx, discordUser: discord.Member=None):
        """ Displays last five games win streak """
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result = overview.getFiveCompetitve(valTag)
            embed = discord.Embed(description="Win Streak")
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            embed.add_field(name="Last 5:", value=str(result))
            embed.set_footer(text="All stats calculated from Competitive matches")
            await ctx.send(embed=embed)


    @commands.command()
    async def maps(self, ctx, discordUser: discord.Member=None):
        discordUser = discordUser or ctx.author
        valTag = user.getValTag(str(discordUser.id))
        if valTag is None:
            await ctx.send("User is not registered yet!")
        else:
            result = overview.bestMaps(valTag)
            embed = discord.Embed(title="Top Maps")
            embed.set_author(name=discordUser, icon_url=discordUser.avatar_url)
            for elem in result:
                embed.add_field(name=elem[0], value="Matches Played: " + elem[1] + " Win Rate: " + elem[2],
                                inline=False)
            embed.set_footer(text="All stats calculated from Unrated matches")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(command(bot))