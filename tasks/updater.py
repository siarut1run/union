from discord.ext import tasks
import aiosqlite
from services.stat_service import update_user_stats

DB_PATH = "data.db"

def start_tasks(bot):
    update_loop.start(bot)

@tasks.loop(minutes=30)
async def update_loop(bot):
    print("PR自動更新中...")

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT discord_id FROM users") as cursor:
            users = await cursor.fetchall()

    for (user_id,) in users:
        try:
            await update_user_stats(user_id)
        except Exception as e:
            print(f"更新失敗: {e}")
