from discord.ext import commands
from discord import app_commands
from services.stat_service import get_stats, update_user_stats

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="成績を見る")
    async def stats(self, interaction: discord.Interaction):
        # 🔥 必ず async関数の中
        await interaction.response.defer()

        await update_user_stats(interaction.user.id)
        data = await get_stats(interaction.user.id)

        msg = (
            f"📊 あなたの成績\n"
            f"PR: {data['pr']}\n"
            f"アーニング: ${data['earnings']}"
        )

        await interaction.followup.send(msg)

async def setup(bot):
    await bot.add_cog(Stats(bot))
