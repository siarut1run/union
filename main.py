import discord
from discord.ext import commands
import os

from db import init_db
from tasks.updater import start_tasks

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"起動完了: {bot.user}")
    start_tasks(bot)

async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and file != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
                print(f"{file} 読み込み成功")
            except Exception as e:
                print(f"{file} 読み込み失敗: {e}")

async def main():
    async with bot:
        await init_db()
        await load_cogs()
        await bot.start(os.getenv("TOKEN"))

import asyncio
asyncio.run(main())
