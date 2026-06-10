import os
import random
import traceback
import discord
import json

from datetime import datetime
from discord.ext import commands
from discord import app_commands

from keep_alive import keep_alive

keep_alive()

# =========================
# BOT CONFIG
# =========================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="?", intents=intents)

MINORI = "<:Minori_Hehehe:1509935548863742002>"

# =========================
# CHARACTERS
# =========================

CHARACTERS = {
    "minori": {
        "name": "🌼 Minori Hanasato",
        "info": "Học sinh năm hai...\nThành viên MORE MORE JUMP!",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/d0/Happy_Birthday%21%21_2025_%28Minori%29.png"
    },
    "haruka": {
        "name": "🐧 Haruka Kiritani",
        "info": "Idol cũ, thành viên MORE MORE JUMP!",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/dc/Happy_Birthday%21%21_2024_%28Haruka%29.png"
    },
    "airi": {
        "name": "🍑 Airi Momoi",
        "info": "Năng động và vui vẻ",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/7/70/Happy_Birthday%21%21_2025_%28Airi%29.png"
    },
    "hinomori": {
        "name": "💧 Shizuku Hinomori",
        "info": "Người chị dịu dàng",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/3/39/Happy_Birthday%21%21_2024_%28Shizuku%29.png"
    },
    "saki": {
        "name": "⭐ Saki Tenma",
        "info": "Luôn vui vẻ",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/e8/Happy_Birthday%21%21_2025_%28Saki%29.png"
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
# USER SYSTEM FIXED
# =========================

USER_FILE = "users.json"


def load_users():
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_users(data):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ✅ FIX: return user + database
def get_user(user_id):
    users = load_users()
    uid = str(user_id)

    if uid not in users:
        users[uid] = {
            "gems": 0,
            "daily": "",
            "solo_count": 0,
            "clear_count": 0,
            "fail_count": 0
        }
        save_users(users)

    return users[uid], users


# =========================
# READY EVENT
# =========================

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.CustomActivity("💖 Sắp thi rồi, cố gắng nhé!")
    )

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print("Sync error:", e)

    print(f"Bot ready: {bot.user}")


# =========================
# PING
# =========================

@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"{MINORI} Ping: {round(bot.latency * 1000)}ms"
    )


# =========================
# GIOI THIEU
# =========================

@bot.tree.command(name="gioi_thieu")
async def intro(interaction: discord.Interaction):

    embed = discord.Embed(
        title=f"{MINORI} Minori Bot",
        description="Hello!",
        color=0xF0B85A
    )

    await interaction.response.send_message(embed=embed)


# =========================
# NHAN VAT
# =========================

@bot.tree.command(name="nhan_vat")
@app_commands.choices(
    nhan_vat=[
        app_commands.Choice(name="Minori", value="minori"),
        app_commands.Choice(name="Haruka", value="haruka"),
        app_commands.Choice(name="Airi", value="airi"),
        app_commands.Choice(name="Shizuku", value="hinomori"),
        app_commands.Choice(name="Saki", value="saki")
    ]
)
async def nhan_vat(interaction: discord.Interaction, nhan_vat: app_commands.Choice[str]):

    c = CHARACTERS[nhan_vat.value]

    embed = discord.Embed(title=c["name"], description=c["info"])
    embed.set_image(url=c["image"])

    await interaction.response.send_message(embed=embed)


# =========================
# PROFILE (FIXED)
# =========================

@bot.tree.command(name="profile")
async def profile(interaction: discord.Interaction):

    user, users = get_user(interaction.user.id)

    embed = discord.Embed(
        title=f"Profile {interaction.user.display_name}",
        color=0xF0B85A
    )

    embed.add_field(name="💎 Gems", value=user["gems"])
    embed.add_field(name="🎵 Solo", value=user["solo_count"])
    embed.add_field(name="✅ Clear", value=user["clear_count"])
    embed.add_field(name="❌ Fail", value=user["fail_count"])

    await interaction.response.send_message(embed=embed)


# =========================
# DAILY (FIXED)
# =========================

@bot.tree.command(name="daily")
async def daily(interaction: discord.Interaction):

    user, users = get_user(interaction.user.id)
    uid = str(interaction.user.id)

    today = datetime.now().strftime("%Y-%m-%d")

    if user["daily"] == today:
        await interaction.response.send_message("❌ Bạn đã nhận hôm nay!")
        return

    reward = random.randint(300, 1000)

    user["gems"] += reward
    user["daily"] = today

    save_users(users)

    await interaction.response.send_message(
        f"🎁 Bạn nhận {reward} gems!"
    )


# =========================
# PLAY SOLO (FIXED FULL)
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
async def play_solo(
    interaction: discord.Interaction,
    song: app_commands.Choice[str],
    difficulty: app_commands.Choice[str]
):

    user, users = get_user(interaction.user.id)

    level = SONGS[song.value]["levels"][difficulty.value]

    rewards = {
        "easy": 10,
        "normal": 20,
        "hard": 30,
        "expert": 40,
        "master": 50,
        "append": 55
    }

    reward = rewards[difficulty.value]

    is_clear = random.random() < 0.75

    user["solo_count"] += 1

    if is_clear:
        user["clear_count"] += 1
        user["gems"] += reward

        embed = discord.Embed(
            title="🎵 CLEAR!",
            description=f"{song.name} ({difficulty.name})",
            color=0x57F287
        )

        embed.add_field(name="💎 Reward", value=f"+{reward}")

    else:
        user["fail_count"] += 1

        percent = random.uniform(5, 25)
        lost = int(user["gems"] * percent / 100)

        user["gems"] = max(0, user["gems"] - lost)

        embed = discord.Embed(
            title="💀 FAIL",
            description=f"{song.name} ({difficulty.name})",
            color=0xED4245
        )

        embed.add_field(name="❌ Lost", value=f"-{lost}")
        embed.add_field(name="📉 Rate", value=f"{percent:.2f}%")

    save_users(users)

    embed.add_field(name="🎚 Level", value=str(level))
    embed.add_field(name="💰 Total Gems", value=str(user["gems"]))

    await interaction.response.send_message(embed=embed)


# =========================
# ERROR HANDLER (FIXED)
# =========================

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):

    print("ERROR:")
    traceback.print_exception(type(error), error, error.__traceback__)

    try:
        await interaction.response.send_message(
            "❌ Đã xảy ra lỗi!",
            ephemeral=True
        )
    except:
        pass


# =========================
# RUN BOT
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Missing DISCORD_TOKEN")

bot.run(TOKEN)
