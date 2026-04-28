from discord.ext import commands
from services.epic_service import link_account

class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def link(self, ctx, epic_id):
        await link_account(ctx.author, epic_id)
        await ctx.send(f"{epic_id} で連携しました")

async def setup(bot):
    await bot.add_cog(Auth(bot))