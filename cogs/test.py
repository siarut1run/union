from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("hello!")

async def setup(bot):
    await bot.add_cog(Test(bot))