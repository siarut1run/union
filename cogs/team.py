from discord.ext import commands

class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createteam(self, ctx, name):
        guild = ctx.guild

        role = await guild.create_role(name=name)
        category = await guild.create_category(name)

        await guild.create_text_channel("chat", category=category)
        await guild.create_voice_channel("vc", category=category)

        await ctx.send(f"{name} を作成しました")

async def setup(bot):
    await bot.add_cog(Team(bot))