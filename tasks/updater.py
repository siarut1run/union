from discord.ext import tasks
import aiosqlite

DB_PATH = "data.db"

def start_tasks(bot):
    update_loop.start(bot)

@tasks.loop(minutes=10)
async def update_loop(bot):
    print("自動更新中...")

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT discord_id, epic_id FROM users") as cursor:
            users = await cursor.fetchall()

    for user_id, epic_id in users:
        guild = bot.guilds[0] if bot.guilds else None
        if guild:
            member = guild.get_member(user_id)
            if member:
                try:
                    await member.edit(nick=epic_id)
                except:
                    pass
