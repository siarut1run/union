import aiosqlite

DB_PATH = "data.db"

async def link_account(bot, user, epic_id):
    # 全サーバーで名前変更
    for guild in bot.guilds:
        member = guild.get_member(user.id)
        if member:
            try:
                await member.edit(nick=epic_id)
            except Exception as e:
                print(f"名前変更失敗: {e}")

    # DB保存
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT OR REPLACE INTO users (discord_id, epic_id, current_name)
        VALUES (?, ?, ?)
        """, (user.id, epic_id, epic_id))
        await db.commit()
