import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

from services.epic_service import link_account

# 🔹 モーダル（EPIC入力）
class EpicModal(Modal, title="EPIC ID認証"):
    epic_id = TextInput(label="EPIC IDを入力", placeholder="例: Player123")

    async def on_submit(self, interaction: discord.Interaction):
        await link_account(interaction.user, self.epic_id.value)
        await interaction.response.send_message(
            f"✅ {self.epic_id.value} で認証完了！",
            ephemeral=True
        )

# 🔹 DM側View（永続）
class DMAuthView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="EPIC IDを入力",
        style=discord.ButtonStyle.green,
        custom_id="auth:open_modal"
    )
    async def open_modal(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(EpicModal())

# 🔹 サーバー側View（永続）
class AuthPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="認証する",
        style=discord.ButtonStyle.blurple,
        custom_id="auth:send_dm"
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

    # 起動時に永続View登録
    async def cog_load(self):
        self.bot.add_view(AuthPanelView())
        self.bot.add_view(DMAuthView())

    # 管理者用：パネル設置（1回だけ使う）
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_auth(self, ctx):
        embed = discord.Embed(
            title="🔐 認証パネル",
            description="ボタンを押して認証してください",
            color=0x3498db
        )
        await ctx.send(embed=embed, view=AuthPanelView())

async def setup(bot):
    await bot.add_cog(Auth(bot))
