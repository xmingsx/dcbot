import os
import random
import traceback
import discord

from datetime import datetime
from discord.ext import commands
from discord import app_commands

from keep_alive import keep_alive
from database import init_db

import sqlite3

# =========================
# INIT
# =========================

keep_alive()
init_db()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="?", intents=intents)

MINORI = "<:Minori_Hehehe:1509935548863742002>"

DB_NAME = "bot.db"

# =========================
# DATABASE FUNCTIONS
# =========================

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    uid = str(user_id)

    c.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
    data = c.fetchone()

    if data is None:
        c.execute("""
        INSERT INTO users (user_id)
        VALUES (?)
        """, (uid,))
        conn.commit()

        c.execute("SELECT * FROM users WHERE user_id = ?", (uid,))
        data = c.fetchone()

    conn.close()

    return {
        "user_id": data[0],
        "gems": data[1],
        "daily": data[2],
        "solo_count": data[3],
        "clear_count": data[4],
        "fail_count": data[5],
    }


def update_user(user):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    UPDATE users
    SET gems = ?,
        daily = ?,
        solo_count = ?,
        clear_count = ?,
        fail_count = ?
    WHERE user_id = ?
    """, (
        user["gems"],
        user["daily"],
        user["solo_count"],
        user["clear_count"],
        user["fail_count"],
        user["user_id"]
    ))

    conn.commit()
    conn.close()

# =========================
# DATA
# =========================

CHARACTERS = {
    "minori": {
        "name": "🌼 Minori",
        "info": "Idol MORE MORE JUMP!",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/d0/Happy_Birthday%21%21_2025_%28Minori%29.png"
    }
}

SONGS = {
    "tell_your_world": {
        "name": "Tell Your World",
        "levels": {
            "easy": 5,
            "normal": 10,
            "hard": 16,
            "expert": 22,
            "master": 26,
            "append": 25
        }
    }
}

# =========================
# READY
# =========================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot ready:", bot.user)

# =========================
# PING
# =========================

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"{MINORI} {round(bot.latency * 1000)}ms"
    )

# =========================
# PROFILE
# =========================

@bot.tree.command(name="profile")
async def profile(interaction: discord.Interaction):

    user = get_user(interaction.user.id)

    embed = discord.Embed(
        title=f"Profile {interaction.user.name}",
        color=0xF0B85A
    )

    embed.add_field(name="💎 Gems", value=user["gems"])
    embed.add_field(name="🎵 Solo", value=user["solo_count"])
    embed.add_field(name="✅ Clear", value=user["clear_count"])
    embed.add_field(name="❌ Fail", value=user["fail_count"])

    await interaction.response.send_message(embed=embed)

# =========================
# DAILY
# =========================

@bot.tree.command(name="daily")
async def daily(interaction: discord.Interaction):

    user = get_user(interaction.user.id)

    today = datetime.now().strftime("%Y-%m-%d")

    if user["daily"] == today:
        await interaction.response.send_message("❌ Đã nhận rồi!")
        return

    reward = random.randint(300, 1000)

    user["gems"] += reward
    user["daily"] = today

    update_user(user)

    await interaction.response.send_message(f"🎁 +{reward} gems")

# =========================
# PLAY SOLO
# =========================

@bot.tree.command(name="play_solo")
@app_commands.choices(
    song=[app_commands.Choice(name="Tell Your World", value="tell_your_world")],
    difficulty=[
        app_commands.Choice(name="Easy", value="easy"),
        app_commands.Choice(name="Normal", value="normal"),
        app_commands.Choice(name="Hard", value="hard"),
        app_commands.Choice(name="Expert", value="expert"),
        app_commands.Choice(name="Master", value="master"),
        app_commands.Choice(name="Append", value="append"),
    ]
)
async def play_solo(interaction: discord.Interaction,
                     song: app_commands.Choice[str],
                     difficulty: app_commands.Choice[str]):

    user = get_user(interaction.user.id)

    level = SONGS[song.value]["levels"][difficulty.value]

    reward_table = {
        "easy": 10,
        "normal": 20,
        "hard": 30,
        "expert": 40,
        "master": 50,
        "append": 60
    }

    reward = reward_table[difficulty.value]

    is_clear = random.random() < 0.75

    user["solo_count"] += 1

    if is_clear:
        user["clear_count"] += 1
        user["gems"] += reward

        embed = discord.Embed(
            title="🎵 CLEAR",
            description=f"{song.name} ({difficulty.name})",
            color=0x57F287
        )

        embed.add_field(name="💎 +Gems", value=reward)

    else:
        user["fail_count"] += 1

        loss_rate = random.uniform(5, 25)
        lost = int(user["gems"] * loss_rate / 100)

        user["gems"] = max(0, user["gems"] - lost)

        embed = discord.Embed(
            title="💀 FAIL",
            description=f"{song.name} ({difficulty.name})",
            color=0xED4245
        )

        embed.add_field(name="❌ Lost", value=f"-{lost}")
        embed.add_field(name="📉 Rate", value=f"{loss_rate:.2f}%")

    update_user(user)

    embed.add_field(name="🎚 Level", value=level)
    embed.add_field(name="💰 Gems", value=user["gems"])

    await interaction.response.send_message(embed=embed)

# =========================
# ERROR HANDLER
# =========================

@bot.tree.error
async def error_handler(interaction: discord.Interaction, error):
    print("ERROR:")
    traceback.print_exception(type(error), error, error.__traceback__)

    try:
        await interaction.response.send_message("❌ Error xảy ra!", ephemeral=True)
    except:
        pass

# =========================
# RUN BOT
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Missing DISCORD_TOKEN")

bot.run(TOKEN)
