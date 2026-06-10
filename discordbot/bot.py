import os
import random
import traceback
import discord
import json

from datetime import datetime
from discord.ext import commands
from discord import app_commands

from keep_alive import keep_alive

# =========================
# KHỞI ĐỘNG WEB SERVER
# =========================

keep_alive()

# =========================
# CẤU HÌNH BOT
# =========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="?",
    intents=intents
)

# =========================
# EMOJI
# =========================

MINORI = "<:Minori_Hehehe:1509935548863742002>"

# =========================
# DỮ LIỆU NHÂN VẬT
# =========================

CHARACTERS = {
    "minori": {
        "name": "🌼 Minori Hanasato",
        "info": (
            "Học sinh năm hai tại Miyamasuzaka Girls Academy.\n"
            "Thành viên nhóm idol MORE MORE JUMP!.\n"
            "Là một cô gái luôn cố gắng hết mình để theo đuổi ước mơ."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/d0/Happy_Birthday%21%21_2025_%28Minori%29.png/revision/latest/scale-to-width-down/1000?cb=20250413150129"
    },

    "haruka": {
        "name": "🐧 Haruka Kiritani",
        "info": (
            "Học sinh năm hai tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Từng là một idol nổi tiếng trước khi gia nhập nhóm."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/dc/Happy_Birthday%21%21_2024_%28Haruka%29.png/revision/latest/scale-to-width-down/1000?cb=20241004150010"
    },

    "airi": {
        "name": "🍑 Airi Momoi",
        "info": (
            "Học sinh năm ba tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Luôn năng động và mang lại bầu không khí vui vẻ."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/7/70/Happy_Birthday%21%21_2025_%28Airi%29.png/revision/latest/scale-to-width-down/1000?cb=20250318150009"
    },

    "hinomori": {
        "name": "💧 Shizuku Hinomori",
        "info": (
            "Học sinh năm ba tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Người chị dịu dàng và luôn quan tâm đến mọi người."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/3/39/Happy_Birthday%21%21_2024_%28Shizuku%29.png/revision/latest/scale-to-width-down/1000?cb=20241205150501"
    },

    "saki": {
        "name": "⭐ Saki Tenma",
        "info": (
            "Học sinh năm hai tại Miyamasuzaka Girls Academy.\n"
            "Thành viên Leo/need.\n"
            "Luôn vui vẻ và mang lại năng lượng tích cực."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/e8/Happy_Birthday%21%21_2025_%28Saki%29.png/revision/latest/scale-to-width-down/1000?cb=20250508150430"
    }
}

# =========================
# USER DATA
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

def get_user(user_id):

    users = load_users()

    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "gems": 0,
            "daily": "",
            "solo_count": 0
        }

        save_users(users)

    return users
# =========================
# KHI BOT KHỞI ĐỘNG
# =========================

@bot.event
async def on_ready():

    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.CustomActivity(
            "💖 Sắp thi rồi, cố gắng hết mình nhé!"
        )
    )

    try:
        synced = await bot.tree.sync()
        print(f"Đã đồng bộ {len(synced)} slash command.")
    except Exception as e:
        print("Lỗi sync command:", e)

    print("=" * 40)
    print("BOT ĐÃ SẴN SÀNG")
    print(f"Tên bot: {bot.user}")
    print(f"ID bot: {bot.user.id}")
    print(f"Đang ở {len(bot.guilds)} máy chủ")
    print("=" * 40)

    for guild in bot.guilds:
        print(f"{guild.name} | {guild.id}")

    print("=" * 40)

# =========================
# /PING
# =========================

@bot.tree.command(
    name="ping",
    description="Kiểm tra độ trễ của mình"
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"{MINORI}\nĐộ trễ hiện tại là: {latency}ms nhóoo"
    )

# =========================
# /GIOI_THIEU
# =========================

@bot.tree.command(
    name="gioi_thieu",
    description="Giới thiệu về Minori Bot"
)
async def gioi_thieu(interaction: discord.Interaction):

    embed = discord.Embed(
        title=f"{MINORI} Giới thiệu về mình",
        description="Mina-san konichiwa! Mình là Minori Hanasato nèee!",
        color=0xF0B85A
    )

    embed.add_field(
    name="📖 Các lệnh hiện có",
    value=(
        "• /ping\n"
        "• /loi_chao\n"
        "• /loi_chuc_thi_thpt\n"
        "• /nhan_vat\n"
        "• /profile\n"
        "• /gioi_thieu"
    ),
    inline=False
)

    embed.set_thumbnail(
        url=CHARACTERS["minori"]["image"]
    )

    embed.set_footer(
        text="Cảm ơn bạn đã sử dụng Minori Bot!"
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /LOI_CHAO
# =========================

@bot.tree.command(
    name="loi_chao",
    description="Lời chào từ Minori"
)
async def loi_chao(interaction: discord.Interaction):

    embed = discord.Embed(
        title=f"{MINORI} Ô 2 Ô!",
        description=(
            "Ô ai vậy nè?\n"
            "Dậy đi nào darling, trời sáng rồi nè 💖"
        ),
        color=0xF0B85A
    )

    embed.add_field(
        name="🌼 Lời nhắn từ Minori",
        value=(
            "Hôm nay hãy cố gắng hết sức nhé!\n"
            "Mình sẽ luôn cổ vũ bạn! 💖"
        ),
        inline=False
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /LOI_CHUC_THI_THPT
# =========================

@bot.tree.command(
    name="loi_chuc_thi_thpt",
    description="Nhận lời chúc thi THPT từ Minori"
)
async def loi_chuc_thi_thpt(interaction: discord.Interaction):

    messages = [
        "🌸 Chúc bạn thật bình tĩnh và tự tin trong kỳ thi nhé!",
        "💖 Hãy tin vào những gì bạn đã cố gắng suốt thời gian qua!",
        "⭐ Chúc bạn đạt được số điểm mà mình mong muốn!",
        "🌼 Minori tin rằng bạn sẽ làm được!",
        "✨ Cố gắng hết sức và đừng bỏ cuộc nhé!",
        "🍀 Chúc bạn gặp thật nhiều may mắn trong phòng thi!",
        "📚 Kiến thức đã sẵn sàng rồi, giờ chỉ cần tự tin thôi!",
        "💛 Thi thật tốt nhé, mình luôn cổ vũ bạn!"
    ]

    embed = discord.Embed(
        title="🎓 Lời chúc thi THPT",
        description=random.choice(messages),
        color=0xF0B85A
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /NHAN_VAT
# =========================

@bot.tree.command(
    name="nhan_vat",
    description="Xem thông tin nhân vật"
)
@app_commands.choices(
    nhan_vat=[
        app_commands.Choice(name="Minori Hanasato", value="minori"),
        app_commands.Choice(name="Haruka Kiritani", value="haruka"),
        app_commands.Choice(name="Airi Momoi", value="airi"),
        app_commands.Choice(name="Shizuku Hinomori", value="hinomori"),
        app_commands.Choice(name="Saki Tenma", value="saki")
    ]
)
async def nhan_vat(
    interaction: discord.Interaction,
    nhan_vat: app_commands.Choice[str]
):

    char = CHARACTERS[nhan_vat.value]

    embed = discord.Embed(
        title=char["name"],
        description=char["info"],
        color=0xF0B85A
    )

    embed.set_image(
        url=char["image"]
    )

    embed.set_footer(
        text="Infomation by Project Sekai Wiki"
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /PROFILE
# =========================

@bot.tree.command(
    name="profile",
    description="Xem hồ sơ của bạn"
)
async def profile(interaction: discord.Interaction):

    users = get_user(interaction.user.id)

    user = users[str(interaction.user.id)]

    embed = discord.Embed(
        title=f"📖 Hồ sơ của {interaction.user.display_name}",
        color=0xF0B85A
    )

    embed.add_field(
        name="💎 Đá",
        value=user["gems"],
        inline=False
    )

    embed.add_field(
        name="🎵 Solo đã chơi",
        value=user["solo_count"],
        inline=False
    )

    await interaction.response.send_message(
        embed=embed
    )
# =========================
# BẮT LỖI
# =========================

@bot.tree.error
async def on_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):

    print("\n===== ERROR =====")

    traceback.print_exception(
        type(error),
        error,
        error.__traceback__
    )

# =========================
# TOKEN
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError(
        "Không tìm thấy DISCORD_TOKEN."
    )

# =========================
# CHẠY BOT
# =========================

print("=" * 40)
print("ĐANG KHỞI ĐỘNG MINORI BOT")
print("=" * 40)

bot.run(TOKEN)
