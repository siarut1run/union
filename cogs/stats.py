from discord.ext import commands
from discord import app_commands
from services.stat_service import get_stats

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="成績を見る")
    async def stats(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            data = await get_stats(interaction.user.id)

            msg = (
                f"📊 あなたの成績\n"
                f"PR: {data['pr']}\n"
                f"アーニング: ${data['earnings']}"
            )

            await interaction.followup.send(msg)

        except Exception as e:
            print("stats error:", e)
            await interaction.followup.send("❌ 取得に失敗しました")

async def setup(bot):
    await bot.add_cog(Stats(bot))
