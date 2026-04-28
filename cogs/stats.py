from discord.ext import commands
from services.stat_service import get_stats

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        data = await get_stats(ctx.author.id)

        msg = (
            f"📊 あなたの成績\n"
            f"PR: {data['pr']}\n"
            f"アーニング: ${data['earnings']}"
        )

        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Stats(bot))
