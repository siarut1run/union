import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Modal, TextInput

from services.epic_service import link_account

# 🔹 モーダル
class EpicModal(Modal, title="EPIC ID認証"):
    epic_id = TextInput(label="EPIC IDを入力", placeholder="例: Player123")

    async def on_submit(self, interaction: discord.Interaction):
        await link_account(interaction.client, interaction.user, self.epic_id.value)
        await interaction.response.send_message(
            f"✅ {self.epic_id.value} で認証完了！",
            ephemeral=True
        )

# 🔹 DM側View
class DMAuthView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="EPIC IDを入力",
        style=discord.ButtonStyle.green,
        custom_id="auth:modal"
    )
    async def open_modal(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(EpicModal())

# 🔹 サーバー側View
class AuthPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="認証する",
        style=discord.ButtonStyle.blurple,
        custom_id="auth:dm"
    )
    async def send_dm(self, interaction: discord.Interaction, button: Button):
        try:
            dm = await interaction.user.create_dm()

            embed = discord.Embed(
                title="🔐 EPIC ID認証",
                description="下のボタンからEPIC IDを入力してください",
                color=0x00ff00
            )

            await dm.send(embed=embed, view=DMAuthView())

            await interaction.response.send_message(
                "📩 DMを送信しました！確認してください",
                ephemeral=True
            )

        except:
            await interaction.response.send_message(
                "❌ DMが送れません。DMを開放してください",
                ephemeral=True
            )

# 🔹 Cog
class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(AuthPanelView())
        self.bot.add_view(DMAuthView())

    # 🔥 スラッシュコマンド（管理者のみ）

    async def setup_auth(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔐 認証パネル",
            description="ボタンを押して認証してください",
            color=0x3498db
        )

        await interaction.response.send_message(embed=embed, view=AuthPanelView())

async def setup(bot):
    await bot.add_cog(Auth(bot))
