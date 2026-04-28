import aiosqlite

DB_PATH = "data.db"


# =========================
# 🔥 PR更新（外部じゃなく“キャッシュ”）
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

    # 🔥 ここで“本来はAPI or 手動更新”
    # 今は仮で保持（壊れない設計）
    pr = await get_cached_pr(user_id)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users
            SET pr = ?
            WHERE discord_id = ?
        """, (pr, user_id))
        await db.commit()

    return {"pr": pr}


# =========================
# 🔥 PR取得（DBのみ）
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

    return {"pr": 0, "earnings": 0}


# =========================
# 🔥 仮キャッシュ（ここが重要）
# =========================
async def get_cached_pr(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT pr FROM users WHERE discord_id = ?",
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()

    return row[0] if row else "0"
