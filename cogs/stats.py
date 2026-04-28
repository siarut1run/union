from discord.ext import commands
from discord import app_commands
from services.stat_service import get_stats

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        # 🔥 Cog読み込み時にコマンド登録
        self.bot.tree.add_command(self.stats)

    @app_commands.command(name="stats", description="成績を見る")
    async def stats(self, interaction):
        data = await get_stats(interaction.user.id)

        msg = (
            f"📊 あなたの成績\n"
            f"PR: {data['pr']}\n"
            f"アーニング: ${data['earnings']}"
        )

        await interaction.response.send_message(msg)

async def setup(bot):
    await bot.add_cog(Stats(bot))
