import os
import random
import traceback
import discord
import psycopg2

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
# DỮ LIỆU BÀI HÁT
# =========================

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
# USER DATA (POSTGRESQL)
# =========================

DATABASE_URL = os.getenv("DATABASE_URL")

# =========================
# KIỂM TRA DATABASE_URL
# =========================

if not DATABASE_URL:
    raise ValueError(
        "Không tìm thấy DATABASE_URL trong Environment Variables."
    )

print("=" * 40)
print("DATABASE_URL ĐÃ ĐƯỢC NẠP")
print("=" * 40)

try:
    conn = psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )

    cur = conn.cursor()

    print("=" * 40)
    print("KẾT NỐI POSTGRESQL THÀNH CÔNG")
    print("=" * 40)

except Exception as e:
    print("LỖI POSTGRESQL:", e)
    raise e


def check_connection():
    global conn, cur

    try:
        cur.execute("SELECT 1")

    except Exception:

        print("MẤT KẾT NỐI DATABASE - ĐANG KẾT NỐI LẠI")

        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode="require"
        )

        cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    gems INTEGER DEFAULT 0,
    daily TEXT DEFAULT '',
    solo_count INTEGER DEFAULT 0,
    clear_count INTEGER DEFAULT 0,
    fail_count INTEGER DEFAULT 0
)
""")

conn.commit()


def get_user(user_id):

    check_connection()

    user_id = str(user_id)
    user_id = str(user_id)

    cur.execute(
        "SELECT * FROM users WHERE user_id = %s",
        (user_id,)
    )

    user = cur.fetchone()

    if user is None:

        cur.execute("""
        INSERT INTO users
        (user_id, gems, daily, solo_count, clear_count, fail_count)
        VALUES (%s, 0, '', 0, 0, 0)
        """, (user_id,))

        conn.commit()

        cur.execute(
            "SELECT * FROM users WHERE user_id = %s",
            (user_id,)
        )

        user = cur.fetchone()

    return {
        "user_id": user[0],
        "gems": user[1],
        "daily": user[2],
        "solo_count": user[3],
        "clear_count": user[4],
        "fail_count": user[5]
    }


def update_user(user):

    cur.execute("""
    UPDATE users
    SET gems=%s,
        daily=%s,
        solo_count=%s,
        clear_count=%s,
        fail_count=%s
    WHERE user_id=%s
    """, (
        user["gems"],
        user["daily"],
        user["solo_count"],
        user["clear_count"],
        user["fail_count"],
        user["user_id"]
    ))

    conn.commit()

# =========================
# KHI BOT KHỞI ĐỘNG
# =========================

@bot.event
async def on_ready():

    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.CustomActivity(
            "💖 Sáng nay thi Ngữ Văn, Hãy cố hết sức mình, viết ra những câu từ bay bổng trên bằng chính đôi tay của mình nào!"
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
        name="🤖 Lệnh Bot",
        value=(
            "• /ping\n"
            "• /loi_chao\n"
            "• /loi_chuc_thi_cu\n"
            "• /nhan_vat\n"
            "• /gioi_thieu"
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 Lệnh Game",
        value=(
            "• /profile\n"
            "• /daily\n"
            "• /play_solo"
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
# /LOI_CHUC_THI_CU
# =========================

@bot.tree.command(
    name="loi_chuc_thi_cu",
    description="Nhận lời chúc thi cử từ Minori"
)
async def loi_chuc_thi_cu(interaction: discord.Interaction):

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
        title="🎓 Lời chúc thi cử",
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
        text="Information by Project Sekai Wiki"
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

    user = get_user(interaction.user.id)

    total = (
        user["clear_count"] +
        user["fail_count"]
    )

    if total > 0:
        clear_rate = round(
            user["clear_count"] / total * 100,
            2
        )
    else:
        clear_rate = 0

    embed = discord.Embed(
        title=f"📖 Hồ sơ của {interaction.user.display_name}",
        color=0xF0B85A
    )

    embed.add_field(
        name="💎 Đá",
        value=str(user["gems"]),
        inline=False
    )

    embed.add_field(
        name="🎵 Solo đã chơi",
        value=str(user["solo_count"]),
        inline=True
    )

    embed.add_field(
        name="✅ Clear",
        value=str(user["clear_count"]),
        inline=True
    )

    embed.add_field(
        name="❌ Fail",
        value=str(user["fail_count"]),
        inline=True
    )

    embed.add_field(
        name="🏆 Tỉ lệ Clear",
        value=f"{clear_rate}%",
        inline=False
    )

    embed.set_footer(
        text="Minori luôn cổ vũ bạn! 💖"
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /DAILY
# =========================

@bot.tree.command(
    name="daily",
    description="Nhận đá hằng ngày"
)
async def daily(interaction: discord.Interaction):

    user = get_user(interaction.user.id)

    today = datetime.now().strftime("%Y-%m-%d")

    if user["daily"] == today:

        await interaction.response.send_message(
            "❌ Hôm nay bạn đã nhận Daily rồi!"
        )
        return

    gems = random.randint(367, 3670)

    user["gems"] += gems
    user["daily"] = today

    update_user(user)

    embed = discord.Embed(
        title="🎁 Daily Reward",
        description=f"Bạn nhận được **{gems} 💎**",
        color=0xF0B85A
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# /PLAY_SOLO
# =========================

@bot.tree.command(
    name="play_solo",
    description="Chơi Solo Live để nhận đá"
)
@app_commands.choices(
    song=[
        app_commands.Choice(
            name="Tell Your World",
            value="tell_your_world"
        )
    ],
    difficulty=[
        app_commands.Choice(name="Easy", value="easy"),
        app_commands.Choice(name="Normal", value="normal"),
        app_commands.Choice(name="Hard", value="hard"),
        app_commands.Choice(name="Expert", value="expert"),
        app_commands.Choice(name="Master", value="master"),
        app_commands.Choice(name="Append", value="append")
    ]
)
async def play_solo(
    interaction: discord.Interaction,
    song: app_commands.Choice[str],
    difficulty: app_commands.Choice[str]
):

    user = get_user(interaction.user.id)

    level = SONGS[song.value]["levels"][difficulty.value]

    rewards = {
        "easy": 10,
        "normal": 20,
        "hard": 30,
        "expert": 40,
        "master": 50,
        "append": 50
    }

    reward = rewards[difficulty.value]

    is_clear = random.random() < 0.763

    if is_clear:

        user["clear_count"] += 1
        user["gems"] += reward

        embed = discord.Embed(
            title="🎵 Solo Live - CLEAR",
            description=(
                f"Bạn đã hoàn thành "
                f"**{song.name}** "
                f"({difficulty.name})"
            ),
            color=0x57F287
        )

        embed.add_field(
            name="💎 Đá nhận được",
            value=f"+{reward}",
            inline=True
        )

    else:

        user["fail_count"] += 1

        embed = discord.Embed(
            title="💀 Solo Live - FAILED",
            description=(
                f"Bạn đã thất bại ở "
                f"**{song.name}** "
                f"({difficulty.name})"
            ),
            color=0xED4245
        )

        embed.add_field(
            name="💖 An ủi",
            value="Bạn không bị mất đá nào!",
            inline=False
        )

    user["solo_count"] += 1

    update_user(user)

    embed.add_field(
        name="📈 Độ khó",
        value=str(level),
        inline=False
    )

    embed.add_field(
        name="💖 Tổng đá hiện tại",
        value=str(user["gems"]),
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
