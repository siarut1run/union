import aiohttp
from bs4 import BeautifulSoup
import aiosqlite

DB_PATH = "data.db"


# =========================
# 🔥 外部取得（安全版）
# =========================
async def fetch_stats(epic_id):
    url = f"https://fortnitetracker.com/profile/all/{epic_id}"

    timeout = aiohttp.ClientTimeout(total=8)
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as res:
                html = await res.text()
    except:
        return {"pr": "0", "earnings": "0"}

    soup = BeautifulSoup(html, "html.parser")

    try:
        pr = soup.select_one(".trn-defstat__value").text.strip()
    except:
        pr = "0"

    return {
        "pr": pr,
        "earnings": "0"
    }


# =========================
# 🔥 DB更新（裏処理用）
# =========================
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
        await db.execute("""
            UPDATE users
            SET pr = ?, earnings = ?
            WHERE discord_id = ?
        """, (stats["pr"], stats["earnings"], user_id))
        await db.commit()

    return stats


# =========================
# 🔥 表示用（最重要：超軽量）
# =========================
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

    return {
        "pr": "0",
        "earnings": "0"
    }
