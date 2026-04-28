import aiosqlite

DB_PATH = "data.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            discord_id INTEGER PRIMARY KEY,
            epic_id TEXT,
            current_name TEXT,
            pr INTEGER DEFAULT 0,
            earnings INTEGER DEFAULT 0
        )
        """)

        await db.commit()
