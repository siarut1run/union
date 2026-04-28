import aiohttp
from bs4 import BeautifulSoup
import aiosqlite

DB_PATH = "data.db"

# 🔹 FortniteTrackerから取得
async def fetch_stats(epic_id):
    url = f"https://fortnitetracker.com/profile/all/{epic_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            html = await res.text()

    soup = BeautifulSoup(html, "html.parser")

    try:
        pr = soup.select_one(".trn-defstat__value").text.strip()
    except:
        pr = "0"

    return {
        "pr": pr,
        "earnings": "0"
    }

# 🔥 ← これが足りなかった
async def update_user_stats(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT epic_id FROM users WHERE discord_id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()

    if not row:
        return None

    epic_id = row[0]

    stats = await fetch_stats(epic_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET pr = ?, earnings = ? WHERE discord_id = ?",
            (stats["pr"], stats["earnings"], user_id)
        )
        await db.commit()

    return stats

# 🔹 表示用
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

    return {"pr": 0, "earnings": 0}
