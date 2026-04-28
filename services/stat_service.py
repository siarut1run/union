import aiosqlite

DB_PATH = "data.db"

async def get_stats(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT pr, earnings FROM users WHERE discord_id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()

    if row:
        return {
            "pr": row[0],
            "earnings": row[1]
        }
    else:
        return {
            "pr": 0,
            "earnings": 0
        }
