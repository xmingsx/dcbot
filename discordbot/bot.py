import os
import traceback
import discord
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
# KHI BOT KHỞI ĐỘNG
# =========================

@bot.event
async def on_ready():

    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.CustomActivity(
            "💖 Cố gắng lên nhé!"
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
    print("=" * 40)

    print("DANH SÁCH SERVER:")
    for guild in bot.guilds:
        print(f"{guild.name} | ID: {guild.id}")

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
        f"Hehehe\nĐộ trễ hiện tại là: {latency}ms nhóoo"
    )

# =========================
# /GIOI_THIEU
# =========================

@bot.tree.command(
    name="gioi_thieu",
    description="Giới thiệu về mình"
)
async def gioi_thieu(interaction: discord.Interaction):

    embed = discord.Embed(
        title=f"{MINORI} Giới thiệu về mình",
        description="Mina-san konichiwa! Mình là Minori Hanasato nèee!",
        color=0xF0B85A
    )

    embed.add_field(
        name=f"Một số lệnh bạn có thể sử dụng nè {MINORI}",
        value=(
            "• /ping - Kiểm tra độ trễ của mình\n"
            "• /loi_chao - Lời chào từ Minori\n"
            "• /nhan_vat - Xem thông tin nhân vật\n"
            "• /gioi_thieu - Giới thiệu về mình"
        ),
        inline=False
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
    description="1 Lời chào lúc thức dậy, nếu rảnh sẽ update chào random"
)
async def chao(interaction: discord.Interaction):

    embed = discord.Embed(
        title=f"{MINORI} Ô 2 Ô!",
        description=(
            "Ô ai vậy nè\n"
            f"Dậy đi nào darling, trời sáng rồi nè {MINORI}"
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
# /NHAN_VAT
# =========================

@bot.tree.command(
    name="nhan_vat",
    description="Xem thông tin nhân vật"
)
@app_commands.choices(
    nhan_vat=[
        app_commands.Choice(
            name="Minori Hanasato",
            value="minori"
        ),
        app_commands.Choice(
            name="Haruka Kiritani",
            value="haruka"
        ),
        app_commands.Choice(
            name="Airi Momoi",
            value="airi"
        ),
        app_commands.Choice(
            name="Shizuku Hinomori",
            value="hinomori"
        ),
        app_commands.Choice(
            name="Saki Tenma",
            value="saki"
        ),
    ]
)
async def nhan_vat(
    interaction: discord.Interaction,
    nhan_vat: app_commands.Choice[str]
):

    data = {
        "minori": "🌼 Minori Hanasato là học sinh năm hai tại Miyamasuzaka. Thành viên MORE MORE JUMP!",
        "haruka": "🐧 Haruka Kiritani là học sinh năm hai tại Miyamasuzaka. Thành viên MORE MORE JUMP!",
        "airi": "🍑 Airi Momoi là học sinh năm ba tại Miyamasuzaka. Thành viên MORE MORE JUMP!",
        "hinomori": "💧 Shizuku Hinomori là học sinh năm ba tại Miyamasuzaka. Thành viên MORE MORE JUMP!",
        "saki": "⭐ Saki Tenma là học sinh năm hai tại Miyamasuzaka. Thành viên Leo/need!"
    }

    await interaction.response.send_message(
        data.get(
            nhan_vat.value,
            "Không tìm thấy nhân vật."
        )
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
        "Không tìm thấy DISCORD_TOKEN trong Environment Variables."
    )

# =========================
# CHẠY BOT
# =========================

print("=" * 40)
print("ĐANG KHỞI ĐỘNG DISCORD BOT")
print("=" * 40)

bot.run(TOKEN)
