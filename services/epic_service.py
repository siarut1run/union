import aiosqlite

DB_PATH = "data.db"

async def link_account(user, epic_id):
    await user.edit(nick=epic_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT OR REPLACE INTO users (discord_id, epic_id, current_name)
        VALUES (?, ?, ?)
        """, (user.id, epic_id, epic_id))
        await db.commit()
