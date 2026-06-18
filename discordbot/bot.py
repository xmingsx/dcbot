import os
import random
import traceback
import discord
import psycopg2
import requests

from io import BytesIO
from PIL import Image
from datetime import datetime, timezone, timedelta
from discord.ext import commands
from discord import app_commands

from keep_alive import keep_alive

# =========================
# HÀM GHÉP 10 ẢNH GACHA
# =========================

def create_gacha_grid(results):

    CARD_WIDTH = 210
    CARD_HEIGHT = 148

    canvas = Image.open(
        "assets/bggc.png"
    ).convert("RGBA")

    POSITIONS = [
        (183, 179),
        (432, 179),
        (682, 179),
        (931, 179),
        (1180, 179),

        (183, 403),
        (432, 403),
        (682, 403),
        (931, 403),
        (1180, 403),
    ]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for index, card_key in enumerate(results):

        image_url = CARDS[card_key]["image"]

        response = requests.get(
            image_url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        img = Image.open(
            BytesIO(response.content)
        ).convert("RGBA")

        img = img.resize(
            (CARD_WIDTH, CARD_HEIGHT)
        )

        x, y = POSITIONS[index]

        canvas.paste(
            img,
            (x, y)
        )

    output = BytesIO()

    canvas.save(
        output,
        format="PNG"
    )

    output.seek(0)

    return output

# =========================
# KHỞI ĐỘNG WEB SERVER
# =========================

keep_alive()

# =========================
# CẤU HÌNH BOT
# =========================

intents = discord.Intents.default()
intents.members = True

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

# =========================
# Virtual Singer
# =========================

VS_CHARACTERS = {

    "miku": {
        "name": "🎤 Hatsune Miku",
        "unit": "Virtual Singer",
        "birthday": "31/08",
        "quote": "Hãy cùng tạo nên âm nhạc nhé!",
        "color": 0x39C5BB,
        "info": (
            "Ca sĩ ảo nổi tiếng nhất thế giới.\n"
            "Xuất hiện trong nhiều SEKAI khác nhau."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/ea/Happy_Anniversary%21%21_2025_%28Miku%29.png/revision/latest/scale-to-width-down/1000?cb=20250830150323"
    },

    "luka": {
        "name": "💗 Megurine Luka",
        "unit": "Virtual Singer",
        "birthday": "30/01",
        "quote": "Âm nhạc luôn kết nối mọi người.",
        "color": 0xF6A4C9,
        "info": (
            "Virtual Singer trưởng thành và dịu dàng."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/ed/Happy_Anniversary%21%21_2025_%28Luka%29.png/revision/latest/scale-to-width-down/1000?cb=20250129150033"
    },

    "meiko": {
        "name": "🍷 MEIKO",
        "unit": "Virtual Singer",
        "birthday": "05/11",
        "quote": "Hãy tự tin tiến về phía trước.",
        "color": 0xD84B4B,
        "info": (
            "Virtual Singer đáng tin cậy."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/df/Happy_Anniversary%21%21_2024_%28MEIKO%29.png/revision/latest/scale-to-width-down/1000?cb=20241104150013"
    },

    "rin": {
        "name": "🍊 Kagamine Rin",
        "unit": "Virtual Singer",
        "birthday": "27/12",
        "quote": "Cùng vui vẻ nào!",
        "color": 0xFFD54F,
        "info": (
            "Một nửa của bộ đôi Kagamine."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/0/09/Happy_Anniversary%21%21_2024_%28Rin%29.png/revision/latest/scale-to-width-down/1000?cb=20241226150134"
    },

    "len": {
        "name": "🍌 Kagamine Len",
        "unit": "Virtual Singer",
        "birthday": "27/12",
        "quote": "Mình sẽ cố gắng hết sức!",
        "color": 0xF9E64F,
        "info": (
            "Một nửa của bộ đôi Kagamine."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/0/06/Happy_Anniversary%21%21_2024_%28Len%29.png/revision/latest/scale-to-width-down/1000?cb=20241226150151"
    },

    "kaito": {
        "name": "🧣 KAITO",
        "unit": "Virtual Singer",
        "birthday": "17/02",
        "quote": "Đừng lo, mọi chuyện sẽ ổn thôi.",
        "color": 0x4F7FFF,
        "info": (
            "Virtual Singer đáng tin cậy."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/4/4a/Happy_Anniversary%21%21_2025_%28KAITO%29.png/revision/latest/scale-to-width-down/1000?cb=20250216153336"
    }
}

# =========================
# Leo/need
# =========================

LN_CHARACTERS = {

    "ichika": {
        "name": "🎸 Ichika Hoshino",
        "unit": "Leo/need",
        "birthday": "11/08",
        "quote": "Mình muốn truyền tải cảm xúc qua âm nhạc.",
        "color": 0x33A1FF,
        "info": "Guitarist và vocalist của Leo/need.",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/2/2c/Happy_Birthday%21%21_2025_%28Ichika%29.png/revision/latest/scale-to-width-down/1000?cb=20250810150111"
    },

    "saki": {
        "name": "⭐ Saki Tenma",
        "unit": "Leo/need",
        "birthday": "09/05",
        "quote": "Mỗi ngày đều thật tuyệt vời!",
        "color": 0xFFE066,
        "info": (
            "Keyboardist của Leo/need.\n"
            "Em gái của Tsukasa Tenma."
        ),
        
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/e8/Happy_Birthday%21%21_2025_%28Saki%29.png/revision/latest/scale-to-width-down/1000?cb=20250508150430"
    },

    "honami": {
        "name": "🥁 Honami Mochizuki",
        "unit": "Leo/need",
        "birthday": "27/10",
        "quote": "Mình muốn giúp đỡ mọi người.",
        "color": 0xF4B183,
        "info": "Drummer của Leo/need.",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/6/6f/Happy_Birthday%21%21_2024_%28Honami%29.png/revision/latest/scale-to-width-down/1000?cb=20241026150131"
    },

    "shiho": {
        "name": "🎸 Shiho Hinomori",
        "unit": "Leo/need",
        "birthday": "08/01",
        "quote": "Âm nhạc là thứ mình yêu thích nhất.",
        "color": 0x8BC34A,
        "info": "Bassist của Leo/need.",
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/eb/Happy_Birthday%21%21_2025_%28Shiho%29.png/revision/latest/scale-to-width-down/1000?cb=20250107164523"
    }
}

# =========================
# MORE MORE JUMP!
# =========================

MMJ_CHARACTERS = {

    "minori": {
        "name": "🌼 Minori Hanasato",
        "unit": "MORE MORE JUMP!",
        "birthday": "14/04",
        "quote": "Mình sẽ cố gắng hết sức!",
        "color": 0xF8BBD0,
        "info": (
            "Học sinh năm hai tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Là một cô gái luôn cố gắng hết mình để theo đuổi ước mơ."
        ),
    "images": [
        "https://static.wikia.nocookie.net/projectsekai/images/d/d0/Happy_Birthday%21%21_2025_%28Minori%29.png/revision/latest/scale-to-width-down/1000?cb=20250413150129",
        "https://static.wikia.nocookie.net/projectsekai/images/b/be/Glittering_Idol%21_T.png/revision/latest/scale-to-width-down/1000?cb=20250930030051",
        "https://static.wikia.nocookie.net/projectsekai/images/8/81/Each_Dream_Weaves_Another_T.png/revision/latest/scale-to-width-down/1000?cb=20240102194222",
        "https://static.wikia.nocookie.net/projectsekai/images/5/53/Blessings_From_My_Friends_T.png/revision/latest/scale-to-width-down/1000?cb=20211001233144",
        "https://static.wikia.nocookie.net/projectsekai/images/2/2f/Happy_Birthday%21%21_2024_%28Minori%29.png/revision/latest/scale-to-width-down/1000?cb=20240413152651",
        "https://static.wikia.nocookie.net/projectsekai/images/b/bf/Happy_Birthday%21%21_%28Minori%29.png/revision/latest/scale-to-width-down/1000?cb=20220413232810",
        "https://static.wikia.nocookie.net/projectsekai/images/2/20/All_I%27ve_Felt_T.png/revision/latest/scale-to-width-down/1000?cb=20240509060114",
        "https://static.wikia.nocookie.net/projectsekai/images/8/87/My_First_Vocal_Range_Check%21_T.png/revision/latest/scale-to-width-down/1000?cb=20220430031809",
        "https://static.wikia.nocookie.net/projectsekai/images/4/4c/Watch_Me_Transform%21_T.png/revision/latest/scale-to-width-down/1000?cb=20240531050532",
        "https://static.wikia.nocookie.net/projectsekai/images/6/63/Falling_With_Honor_T.png/revision/latest/scale-to-width-down/1000?cb=20220630031857",
        "https://static.wikia.nocookie.net/projectsekai/images/5/55/I%27m_Gonna_Lose_My_Head%21_T.png/revision/latest/scale-to-width-down/1000?cb=20221031030101",
        "https://static.wikia.nocookie.net/projectsekai/images/e/ed/The_Dreams_That_Get_Lost_In_The_Crowd_T.png/revision/latest/scale-to-width-down/1000?cb=20250808032731",
        "https://static.wikia.nocookie.net/projectsekai/images/7/7d/Happy_Birthday%21%21_2023_%28Minori%29.png/revision/latest/scale-to-width-down/1000?cb=20230415090351",
        "https://static.wikia.nocookie.net/projectsekai/images/8/81/Dance_Of_Wishes_T.png/revision/latest/scale-to-width-down/1000?cb=20251231030116",
        "https://static.wikia.nocookie.net/projectsekai/images/a/a7/Watching_Her_Back_T.png/revision/latest/scale-to-width-down/1000?cb=20230930061929",
        "https://static.wikia.nocookie.net/projectsekai/images/c/c0/Happy_Birthday%21%21_2026_%28Minori%29.png/revision/latest/scale-to-width-down/1000?cb=20260409150209",
        "https://static.wikia.nocookie.net/projectsekai/images/5/55/Fervor_Coaching%21%3F_T.png/revision/latest/scale-to-width-down/1000?cb=20260517030712"
    ],
     "captions": [
        "🎂 Happy Birthday!! 2025",
        "✨ Glittering Idol!",
        "🌈 Each Dream Weaves Another",
        "🎁 Blessings From My Friends",
        "🎂 Happy Birthday!! 2024",
        "🎂 Happy Birthday!!",
        "💖 All I've Felt",
        "🎤 My First Vocal Range Check!",
        "✨ Watch Me Transform!",
        "🎭 Falling With Honor",
        "😵 I'm Gonna Lose My Head!",
        "🌠 The Dreams That Get Lost In The Crowd",
        "🎂 Happy Birthday!! 2023",
        "💃 Dance Of Wishes",
        "👀 Watching Her Back",
        "🎂 Happy Birthday!! 2026",
        "🔥 Fervor Coaching!?"
    ]
},

    "haruka": {
        "name": "🐧 Haruka Kiritani",
        "unit": "MORE MORE JUMP!",
        "birthday": "05/10",
        "quote": "Mình sẽ tiếp tục tiến về phía trước.",
        "color": 0x6EC6FF,
        "info": (
            "Học sinh năm hai tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Từng là một idol nổi tiếng trước khi gia nhập nhóm."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/d/dc/Happy_Birthday%21%21_2024_%28Haruka%29.png/revision/latest/scale-to-width-down/1000?cb=20241004150010"
    },

    "airi": {
        "name": "🍑 Airi Momoi",
        "unit": "MORE MORE JUMP!",
        "birthday": "19/03",
        "quote": "Đừng đánh giá thấp thần tượng nhé!",
        "color": 0xFF9EAA,
        "info": (
            "Học sinh năm ba tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Luôn năng động và mang lại bầu không khí vui vẻ."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/7/70/Happy_Birthday%21%21_2025_%28Airi%29.png/revision/latest/scale-to-width-down/1000?cb=20250318150009"
    },

    "shizuku": {
        "name": "💧 Shizuku Hinomori",
        "unit": "MORE MORE JUMP!",
        "birthday": "06/12",
        "quote": "Mình muốn giúp đỡ mọi người.",
        "color": 0x7CD4FF,
        "info": (
            "Học sinh năm ba tại Miyamasuzaka Girls Academy.\n"
            "Thành viên MORE MORE JUMP!.\n"
            "Người chị dịu dàng và luôn quan tâm đến mọi người."
        ),
        "image": "https://static.wikia.nocookie.net/projectsekai/images/3/39/Happy_Birthday%21%21_2024_%28Shizuku%29.png/revision/latest/scale-to-width-down/1000?cb=20241205150501"
    }
}
# =========================
# Vivid BAD SQUAD
# =========================

VBS_CHARACTERS = {

    "kohane": {
        "name": "🐹 Kohane Azusawa",
        "unit": "Vivid BAD SQUAD",
        "birthday": "02/03",
        "quote": "Mình muốn hát cùng mọi người.",
        "color": 0xFFB74D,

        "info": (
            "Thành viên Vivid BAD SQUAD.\n"
            "Một cô gái nhút nhát nhưng rất yêu âm nhạc."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/ef/Happy_Birthday%21%21_2025_%28Kohane%29.png/revision/latest/scale-to-width-down/1000?cb=20250301150608"
    },

    "an": {
        "name": "🎧 An Shiraishi",
        "unit": "Vivid BAD SQUAD",
        "birthday": "26/07",
        "quote": "Hãy cho cả thế giới thấy âm nhạc của chúng ta!",
        "color": 0x4FC3F7,

        "info": (
            "Thành viên Vivid BAD SQUAD.\n"
            "Con gái của chủ quán cà phê WEEKEND GARAGE."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/8/83/Happy_Birthday%21%21_2025_%28An%29.png/revision/latest/scale-to-width-down/1000?cb=20250725194454"
    },

    "akito": {
        "name": "🍊 Akito Shinonome",
        "unit": "Vivid BAD SQUAD",
        "birthday": "12/11",
        "quote": "Tôi sẽ vượt qua bất kỳ giới hạn nào.",
        "color": 0xFF8A65,

        "info": (
            "Thành viên Vivid BAD SQUAD.\n"
            "Em trai của Ena Shinonome."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/b/b7/Happy_Birthday%21%21_2024_%28Akito%29.png/revision/latest/scale-to-width-down/1000?cb=20241111150004"
    },

    "toya": {
        "name": "☕ Toya Aoyagi",
        "unit": "Vivid BAD SQUAD",
        "birthday": "25/05",
        "quote": "Tôi muốn tự chọn con đường của mình.",
        "color": 0x64B5F6,

        "info": (
            "Thành viên Vivid BAD SQUAD.\n"
            "Từng được đào tạo piano cổ điển."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/b/b4/Happy_Birthday%21%21_2025_%28Toya%29.png/revision/latest/scale-to-width-down/1000?cb=20250524150009"
    }
}

# =========================
# Wonderlands x Showtime
# =========================

WXS_CHARACTERS = {

    "tsukasa": {
        "name": "🌟 Tsukasa Tenma",
        "unit": "Wonderlands x Showtime",
        "birthday": "17/05",
        "quote": "Ta sẽ trở thành ngôi sao sáng nhất!",
        "color": 0xFFD54F,

        "info": (
            "Trưởng nhóm Wonderlands x Showtime.\n"
            "Anh trai của Saki Tenma."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/5/5e/Happy_Birthday%21%21_2025_%28Tsukasa%29.png/revision/latest/scale-to-width-down/1000?cb=20250516150034"
    },

    "emu": {
        "name": "🍬 Emu Otori",
        "unit": "Wonderlands x Showtime",
        "birthday": "09/09",
        "quote": "Wonderhoy~!",
        "color": 0xFF80AB,

        "info": (
            "Thành viên Wonderlands x Showtime.\n"
            "Luôn tràn đầy năng lượng và niềm vui."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/3/32/Happy_Birthday%21%21_2025_%28Emu%29.png/revision/latest/scale-to-width-down/1000?cb=20250908165852"
    },

    "nene": {
        "name": "🎮 Nene Kusanagi",
        "unit": "Wonderlands x Showtime",
        "birthday": "20/07",
        "quote": "Mình sẽ cố gắng hết sức.",
        "color": 0x81C784,

        "info": (
            "Thành viên Wonderlands x Showtime.\n"
            "Yêu thích game và hát rất hay."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/c/c6/Happy_Birthday%21%21_2025_%28Nene%29.png/revision/latest/scale-to-width-down/1000?cb=20250719150017"
    },

    "rui": {
        "name": "🎈 Rui Kamishiro",
        "unit": "Wonderlands x Showtime",
        "birthday": "24/06",
        "quote": "Ý tưởng thú vị vừa xuất hiện rồi.",
        "color": 0xBA68C8,

        "info": (
            "Đạo diễn sân khấu của Wonderlands x Showtime.\n"
            "Thiên tài sáng tạo."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/eb/Happy_Birthday%21%21_2025_%28Rui%29.png/revision/latest/scale-to-width-down/1000?cb=20250623150053"
    }
}

# =========================
# Nightcord at 25:00
# =========================

N25_CHARACTERS = {

    "kanade": {
        "name": "🎼 Kanade Yoisaki",
        "unit": "Nightcord at 25:00",
        "birthday": "10/02",
        "quote": "Mình muốn cứu ai đó bằng âm nhạc.",
        "color": 0xB39DDB,

        "info": (
            "Người sáng tác nhạc của Nightcord at 25:00."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/4/4d/Happy_Birthday%21%21_2025_%28Kanade%29.png/revision/latest/scale-to-width-down/1000?cb=20250209154738"
    },

    "mafuyu": {
        "name": "❄️ Mafuyu Asahina",
        "unit": "Nightcord at 25:00",
        "birthday": "27/01",
        "quote": "Mình thật sự là ai...?",
        "color": 0x90CAF9,

        "info": (
            "Thành viên Nightcord at 25:00.\n"
            "Một học sinh ưu tú với nhiều áp lực."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/9/90/Happy_Birthday%21%21_2025_%28Mafuyu%29.png/revision/latest/scale-to-width-down/1000?cb=20250126150006"
    },

    "ena": {
        "name": "🎨 Ena Shinonome",
        "unit": "Nightcord at 25:00",
        "birthday": "30/04",
        "quote": "Tôi muốn mọi người công nhận mình.",
        "color": 0xF48FB1,

        "info": (
            "Thành viên Nightcord at 25:00.\n"
            "Chị gái của Akito Shinonome."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/8/88/Happy_Birthday%21%21_2025_%28Ena%29.png/revision/latest/scale-to-width-down/1000?cb=20250429150013"
    },

    "mizuki": {
        "name": "🎀 Mizuki Akiyama",
        "unit": "Nightcord at 25:00",
        "birthday": "27/08",
        "quote": "Hãy sống đúng với bản thân nhé.",
        "color": 0xCE93D8,

        "info": (
            "Thành viên Nightcord at 25:00.\n"
            "Chuyên thiết kế trang phục và phụ kiện."
        ),

        "image": "https://static.wikia.nocookie.net/projectsekai/images/2/2d/Happy_Birthday%21%21_2025_%28Mizuki%29.png/revision/latest/scale-to-width-down/1000?cb=20250826153012"
    }
}

CHARACTERS = {}

CHARACTERS.update(VS_CHARACTERS)
CHARACTERS.update(LN_CHARACTERS)
CHARACTERS.update(MMJ_CHARACTERS)
CHARACTERS.update(VBS_CHARACTERS)
CHARACTERS.update(WXS_CHARACTERS)
CHARACTERS.update(N25_CHARACTERS)

# =========================
# CARDS
# =========================

CARDS = {

    "minori_glittering_idol": {
        "name": "✨ Glittering Idol!",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/b/be/Glittering_Idol%21_T.png/revision/latest/scale-to-width-down/1000?cb=20250930030051"
    },

    "minori_each_dream": {
        "name": "🌈 Each Dream Weaves Another",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/8/81/Each_Dream_Weaves_Another_T.png/revision/latest/scale-to-width-down/1000?cb=20240102194222"
    },

    "minori_blessings": {
        "name": "🎁 Blessings From My Friends",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/5/53/Blessings_From_My_Friends_T.png/revision/latest/scale-to-width-down/1000?cb=20211001233144"
    },

    "minori_all_ive_felt": {
        "name": "💖 All I've Felt",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/2/20/All_I%27ve_Felt_T.png/revision/latest/scale-to-width-down/1000?cb=20240509060114"
    },

    "minori_vocal_range": {
        "name": "🎤 My First Vocal Range Check!",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/8/87/My_First_Vocal_Range_Check%21_T.png/revision/latest/scale-to-width-down/1000?cb=20220430031809"
    },

    "minori_transform": {
        "name": "✨ Watch Me Transform!",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/4/4c/Watch_Me_Transform%21_T.png/revision/latest/scale-to-width-down/1000?cb=20240531050532"
    },

    "minori_falling_honor": {
        "name": "🎭 Falling With Honor",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/6/63/Falling_With_Honor_T.png/revision/latest/scale-to-width-down/1000?cb=20220630031857"
    },

    "minori_lose_my_head": {
        "name": "😵 I'm Gonna Lose My Head!",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/5/55/I%27m_Gonna_Lose_My_Head%21_T.png/revision/latest/scale-to-width-down/1000?cb=20221031030101"
    },

    "minori_dreams_lost": {
        "name": "🌠 The Dreams That Get Lost In The Crowd",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/e/ed/The_Dreams_That_Get_Lost_In_The_Crowd_T.png/revision/latest/scale-to-width-down/1000?cb=20250808032731"
    },

    "minori_dance_of_wishes": {
        "name": "💃 Dance Of Wishes",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/8/81/Dance_Of_Wishes_T.png/revision/latest/scale-to-width-down/1000?cb=20251231030116"
    },

    "minori_watching_her_back": {
        "name": "👀 Watching Her Back",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/a/a7/Watching_Her_Back_T.png/revision/latest/scale-to-width-down/1000?cb=20230930061929"
    },

    "minori_fervor_coaching": {
        "name": "🔥 Fervor Coaching!?",
        "character": "Minori Hanasato",
        "rarity": 4,
        "image": "https://static.wikia.nocookie.net/projectsekai/images/5/55/Fervor_Coaching%21%3F_T.png/revision/latest/scale-to-width-down/1000?cb=20260517030712"
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
# SONG PHAT 
# =========================

MUSIC_FILES = {
    "hoshi": {
        "title": "⭐ Hoshi ni Ichiban Chikai Basho (Leo/need)",
        "path": "discordbot/Hoshi_ni_Ichiban_Chikai_Basho_(Full_Version_-_Leo-need).ogg"
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

# =========================
# TẠO BẢNG USERS
# =========================

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

# =========================
# TẠO BẢNG CARDS
# =========================

cur.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    card_id TEXT NOT NULL
)
""")

conn.commit()


def get_user(user_id):

    check_connection()

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

    global conn, cur

    try:

        check_connection()

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

    except Exception as e:

        print("Lỗi update_user:", e)

        conn = psycopg2.connect(
            DATABASE_URL,
            sslmode="require"
        )

        cur = conn.cursor()

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


def add_card(user_id, card_id):

    check_connection()

    cur.execute("""
    INSERT INTO cards (user_id, card_id)
    VALUES (%s, %s)
    """, (
        str(user_id),
        card_id
    ))

    conn.commit()


def get_inventory(user_id):

    check_connection()

    cur.execute("""
    SELECT card_id
    FROM cards
    WHERE user_id = %s
    """, (
        str(user_id),
    ))

    rows = cur.fetchall()

    return [row[0] for row in rows]


def roll_card():

    return random.choice(
        list(CARDS.keys())
    )

# =========================
# KHI BOT KHỞI ĐỘNG
# =========================

@bot.event
async def on_connect():
    print("CONNECTED TO DISCORD")


@bot.event
async def on_ready():

    print("=" * 40)
    print("ON_READY CALLED")
    print("=" * 40)

    print(f"BOT USER = {bot.user}")

    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.CustomActivity(
            "💖 Chưa làm gacha command được, không TÀY rồi :( "
        )
    )

    try:
        synced = await bot.tree.sync()

        print(
            f"Đã đồng bộ {len(synced)} slash command."
        )

        for cmd in synced:
            print(" -", cmd.name)

    except Exception as e:
        print("Lỗi sync command:")
        print(e)

    print("=" * 40)
    print("BOT ĐÃ SẴN SÀNG")
    print(f"Tên bot: {bot.user}")
    print(f"ID bot: {bot.user.id}")
    print(f"Đang ở {len(bot.guilds)} máy chủ")
    print("=" * 40)

    for guild in bot.guilds:
        print(
            f"{guild.name} | {guild.id}"
        )

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
        description=f"Mina-san konichiwa! Mình là Minori Hanasato nèee!\nMột số lệnh mà hiện tại bạn có thể dùng nèee {MINORI}",
        color=0xF0B85A
    )

    embed.add_field(
        name="🤖 Lệnh Bot",
        value=(
            "• /ping\n"
            "• /loi_chao\n"
            "• /loi_chuc_thi_cu\n"
            "• /nhan_vat\n"
            "• /gioi_thieu\n"
            "• /kick\n"
            "• /mute\n"
            "• /unmute"
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 Lệnh Game",
        value=(
            "• /profile\n"
            "• /daily\n"
            "• /play_solo\n"
            "• /tim_kiem_nhac\n"
            "• /gacha\n"
            "• /inventory"
        ),
        inline=False
    )

    embed.set_thumbnail(
        url=CHARACTERS["minori"]["images"][0]
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
    description="Lời chào ngẫu nhiên từ Minori"
)
async def loi_chao(interaction: discord.Interaction):

    greetings = [
        "🌼 Xin chào! Hôm nay bạn thế nào?",
        "💖 Rất vui được gặp bạn!",
        "✨ Chúc bạn một ngày thật tuyệt vời!",
        "🌸 Chào bạn! Cùng cố gắng nhé!",
        "☀️ Chúc bạn buổi sáng tràn đầy năng lượng!",
        "🌙 Chúc bạn có một buổi tối thật thư giãn!",
        "🍀 Mong mọi điều tốt đẹp sẽ đến với bạn!",
        "🎶 Minori đến chào bạn đây!",
        "🌈 Hy vọng hôm nay bạn sẽ mỉm cười thật nhiều!",
        "⭐ Chúc bạn gặp nhiều may mắn!",
        "🎉 Chúc bạn có thật nhiều niềm vui!",
        "🌺 Cảm ơn vì đã ghé thăm mình!",
        "📚 Chúc bạn học tập thật tốt!",
        "💛 Chúc bạn làm việc hiệu quả nhé!",
        "🌷 Đừng quên nghỉ ngơi khi mệt nha!",
        "🎀 Minori luôn cổ vũ bạn!",
        "💫 Hãy tin vào bản thân mình nhé!",
        "🍑 Chúc bạn luôn hạnh phúc!",
        "🌻 Hôm nay chắc chắn sẽ là một ngày tốt đẹp!",
        "🩷 Chúc bạn thật nhiều tiếng cười!",
        "🌼 Mình rất vui vì được gặp bạn!",
        "☁️ Chúc bạn một ngày bình yên!",
        "🌠 Mong ước của bạn sẽ thành hiện thực!",
        "🎵 Hãy tận hưởng từng khoảnh khắc nhé!",
        "💝 Chúc bạn luôn gặp điều tích cực!",
        "🌟 Bạn đang làm rất tốt rồi!",
        "🍀 Đừng bỏ cuộc nhé!",
        "🌸 Cố lên, mình tin bạn làm được!",
        "🎈 Hôm nay hãy thật tự tin nha!",
        "🐣 Chúc bạn thật nhiều động lực!",
        "🌹 Chúc bạn luôn giữ được nụ cười!",
        "✨ Hãy bắt đầu ngày mới thật vui vẻ!",
        "💖 Chào mừng bạn quay trở lại!",
        "🌼 Mỗi ngày đều là một khởi đầu mới!",
        "🎉 Hãy tạo nên những kỷ niệm đẹp hôm nay!",
        "🌈 Mong bạn có một ngày đầy màu sắc!",
        "☕ Đừng quên uống nước nhé!",
        "🍰 Chúc bạn có thật nhiều niềm vui nho nhỏ!",
        "🎶 Cùng nhau cố gắng nào!",
        "💫 Chỉ cần tiến lên từng bước là được!",
        "🌷 Chúc bạn luôn gặp quý nhân giúp đỡ!",
        "🌸 Mình luôn ủng hộ bạn!",
        "⭐ Chúc mọi điều thuận lợi đến với bạn!",
        "💛 Hãy luôn yêu thương bản thân nhé!",
        "🌻 Chúc bạn tràn đầy cảm hứng!",
        "🍀 Hy vọng hôm nay thật suôn sẻ!",
        "🎀 Bạn thật tuyệt vời!",
        "🌠 Mỉm cười lên nào!",
        "🩷 Chúc bạn thật nhiều hạnh phúc!",
        "💖 Minori gửi bạn thật nhiều năng lượng tích cực!",
        "🌼 Chúc bạn một ngày không có muộn phiền!",
        "🎉 Hãy vui vẻ hết mình nhé!",
        "🌸 Chúc bạn gặp thật nhiều điều bất ngờ thú vị!",
        "⭐ Hôm nay chắc chắn sẽ ổn thôi!",
        "🌈 Chúc bạn luôn lạc quan!",
        "💛 Mọi nỗ lực của bạn đều đáng quý!",
        "🍀 Đừng quên tự thưởng cho mình nhé!",
        "🎶 Chúc bạn nghe được nhiều bài hát hay!",
        "☀️ Ánh nắng hôm nay dành cho bạn!",
        "🌙 Chúc bạn ngủ ngon nếu đã khuya!",
        "🌷 Cố gắng thêm một chút nữa nhé!",
        "💖 Bạn không hề đơn độc đâu!",
        "🌼 Chúc bạn luôn khỏe mạnh!",
        "🎀 Hãy giữ trái tim đầy hy vọng!",
        "⭐ Chúc bạn đạt được mục tiêu của mình!",
        "🍰 Mong hôm nay có thật nhiều điều ngọt ngào!",
        "🌸 Bạn làm tốt hơn mình nghĩ đấy!",
        "🌈 Mỗi ngày đều có điều đáng mong chờ!",
        "🎉 Hãy tận hưởng hiện tại nhé!",
        "💫 Đừng quên yêu chính mình!",
        "🌻 Chúc bạn luôn tràn đầy nhiệt huyết!",
        "🍀 Chúc bạn gặp nhiều điều may mắn bất ngờ!",
        "🩷 Mình luôn ở đây để cổ vũ bạn!",
        "🌷 Hôm nay hãy thử điều mới nhé!",
        "💖 Hy vọng bạn sẽ có thật nhiều niềm vui!",
        "🌼 Chúc bạn một ngày đầy tiếng cười!",
        "🎶 Hãy để âm nhạc tiếp thêm động lực!",
        "⭐ Chúc bạn thành công trong mọi việc!",
        "🌸 Bạn thật đáng ngưỡng mộ!",
        "☁️ Bình yên sẽ luôn ở bên bạn!",
        "💛 Chúc bạn luôn giữ tinh thần tích cực!",
        "🎈 Mong mọi việc diễn ra như ý!",
        "🌠 Ước mơ của bạn rất đáng để theo đuổi!",
        "🍀 Hãy bước tiếp với sự tự tin!",
        "🌷 Mỗi ngày bạn đều tiến bộ hơn!",
        "💖 Chúc bạn có thật nhiều bạn bè tốt!",
        "🌈 Hy vọng bạn luôn gặp điều tốt đẹp!",
        "🎀 Chúc bạn một ngày tràn ngập niềm vui!",
        "🌻 Hãy tự hào về bản thân nhé!",
        "⭐ Cảm ơn bạn đã đến đây!",
        "🎶 Chúc bạn luôn giữ nụ cười trên môi!",
        "💫 Điều tuyệt vời đang chờ phía trước!",
        "🍑 Chúc bạn có một ngày thật đáng nhớ!",
        "🌸 Minori luôn tin tưởng bạn!",
        "🩷 Chúc bạn thật nhiều hạnh phúc và bình an!",
        "🌼 Hy vọng hôm nay sẽ là ngày tuyệt nhất của bạn!",
        "🎉 Mỗi ngày đều là cơ hội để tỏa sáng!",
        "💖 Chúc bạn gặp nhiều điều kỳ diệu!",
        "🌟 Hãy luôn là chính mình nhé!",
        "🍀 Minori chúc bạn một ngày thật vui vẻ!"
    ]

    embed = discord.Embed(
        title=f"{MINORI} Xin chào!",
        description=random.choice(greetings),
        color=0xF0B85A
    )

    embed.set_thumbnail(
        url=CHARACTERS["minori"]["images"][0]
    )

    embed.set_footer(
        text="Minori luôn ở đây để cổ vũ bạn! 💖"
    )

    await interaction.response.send_message(embed=embed)

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
        "💛 Thi thật tốt nhé, mình luôn cổ vũ bạn!",
        "🌟 Chúc bạn làm bài thật suôn sẻ!",
        "🎓 Hy vọng mọi câu hỏi đều nằm trong phần bạn ôn tập!",
        "🩷 Hãy hít thở thật sâu và làm bài từng bước nhé!",
        "🌈 Chúc bạn giữ được tinh thần thật thoải mái!",
        "🎉 Mong bạn đạt kết quả vượt ngoài mong đợi!",
        "💐 Mỗi nỗ lực của bạn đều sẽ được đền đáp!",
        "🌺 Đừng lo lắng quá, bạn đã chuẩn bị rất tốt rồi!",
        "📖 Chúc bạn nhớ hết những gì đã học!",
        "🌻 Cứ bình tĩnh, thành công sẽ đến!",
        "🍀 Chúc bạn gặp đề thi thật vừa sức!",
        "🌸 Hãy tự tin vì bạn có thể làm được!",
        "✨ Minori gửi bạn thật nhiều may mắn!",
        "💖 Chúc bạn hoàn thành bài thi trong thời gian quy định!",
        "⭐ Đừng quên kiểm tra lại bài trước khi nộp nhé!",
        "🌼 Chúc bạn giữ được phong độ đến phút cuối!",
        "📚 Mọi cố gắng của bạn đều rất đáng quý!",
        "🎀 Hôm nay là ngày để bạn tỏa sáng!",
        "🌷 Chúc bạn đạt điểm thật cao!",
        "🌞 Đừng để áp lực làm mất sự tự tin của mình!",
        "🍑 Chúc bạn luôn sáng suốt khi làm bài!",
        "🌠 Hy vọng kết quả sẽ khiến bạn mỉm cười!",
        "🎵 Chúc bạn có một kỳ thi thật thuận lợi!",
        "💫 Bình tĩnh là chìa khóa của thành công!",
        "🌈 Chúc bạn không bỏ sót bất kỳ câu nào!",
        "🌸 Tin tưởng vào bản thân nhé!",
        "🍀 Chúc bạn gặp thật nhiều câu hỏi quen thuộc!",
        "💛 Hãy phát huy hết khả năng của mình!",
        "📚 Bạn đã cố gắng rất nhiều rồi!",
        "🎉 Minori cổ vũ bạn từ xa nè!",
        "🌟 Chúc bạn làm bài thật chính xác!",
        "🩷 Đừng quên đọc kỹ đề bài nhé!",
        "🌻 Chúc bạn luôn giữ tinh thần lạc quan!",
        "💖 Chỉ cần cố gắng hết sức là đủ rồi!",
        "⭐ Mong bạn sẽ đạt kết quả như mong muốn!",
        "🌺 Hãy biến sự chăm chỉ thành điểm số thật đẹp!",
        "🍀 Chúc bạn thật bình tĩnh trong mọi tình huống!",
        "📖 Chúc bạn nhớ công thức đúng lúc!",
        "🌸 Đừng căng thẳng quá nhé!",
        "✨ Hôm nay nhất định sẽ là một ngày may mắn!",
        "🎀 Chúc bạn hoàn thành bài thi thật xuất sắc!",
        "🌈 Tự tin lên, bạn giỏi hơn mình nghĩ đó!",
        "💛 Chúc bạn luôn giữ được sự tập trung!",
        "🌼 Hy vọng bạn sẽ đạt được mục tiêu của mình!",
        "🎓 Mong bạn có một kỳ thi thật thành công!",
        "🌻 Đừng quên kiểm soát thời gian khi làm bài!",
        "💖 Mỗi câu trả lời đều đưa bạn đến gần thành công hơn!",
        "🍀 Chúc bạn gặp nhiều điều thuận lợi!",
        "🌟 Thi thật tốt nhé!",
        "📚 Kiến thức bạn học sẽ phát huy đúng lúc!",
        "✨ Chúc bạn không bị áp lực!",
        "🌸 Hãy làm bài với nụ cười trên môi!",
        "🎉 Chúc bạn vượt qua mọi thử thách!",
        "💛 Mọi người đều tin tưởng bạn!",
        "🩷 Minori luôn đứng về phía bạn!",
        "🌼 Hãy mạnh dạn trả lời những gì mình biết!",
        "🍀 Chúc bạn có thật nhiều cảm hứng!",
        "⭐ Chúc bạn không mắc lỗi đáng tiếc!",
        "🌺 Đừng quên giữ bình tĩnh nhé!",
        "📖 Bạn chắc chắn sẽ làm được!",
        "🌻 Thành công đang chờ bạn phía trước!",
        "💖 Chúc bạn nhận được kết quả thật xứng đáng!",
        "🎓 Thi cử chỉ là một bước trên hành trình thôi!",
        "✨ Hãy tự hào về những gì mình đã cố gắng!",
        "🌈 Chúc bạn hoàn thành mọi mục tiêu!",
        "🍀 Chúc bạn luôn giữ tinh thần tích cực!",
        "🎀 Hãy tin vào chính mình!",
        "💫 Chúc bạn làm bài thật nhanh và chính xác!",
        "🌸 Hy vọng hôm nay sẽ là ngày tuyệt vời của bạn!",
        "⭐ Chúc bạn có thật nhiều may mắn!",
        "📚 Kiến thức sẽ không phụ lòng người chăm chỉ!",
        "🌻 Đừng bỏ cuộc đến phút cuối nhé!",
        "💖 Mình tin bạn sẽ đạt kết quả tốt!",
        "🍑 Chúc bạn luôn sáng suốt khi lựa chọn đáp án!",
        "🌟 Hãy tự tin bước vào phòng thi!",
        "🎉 Chúc bạn có một trải nghiệm thi cử nhẹ nhàng!",
        "🌼 Chỉ cần cố gắng hết mình là tuyệt lắm rồi!",
        "🩷 Chúc bạn luôn giữ vững tinh thần!",
        "🍀 Hôm nay vận may sẽ mỉm cười với bạn!",
        "🌸 Đừng lo, bạn đã chuẩn bị rất kỹ rồi!",
        "💛 Chúc bạn có thật nhiều năng lượng tích cực!",
        "📖 Mong mọi câu trả lời đều đến đúng lúc!",
        "🌺 Chúc bạn không bị hồi hộp quá!",
        "✨ Thành công chắc chắn sẽ đến với người nỗ lực!",
        "🎀 Hãy bình tĩnh và tin vào bản thân!",
        "🌈 Chúc bạn đạt điểm số thật ấn tượng!",
        "⭐ Mình luôn cổ vũ bạn hết mình!",
        "🌻 Chúc bạn thi đâu thắng đó!",
        "💖 Mong bạn mỉm cười thật tươi khi nhận kết quả!",
        "🍀 Chúc bạn hoàn thành kỳ thi với kết quả tốt nhất!",
        "🎓 Minori chúc bạn thành công trên mọi chặng đường học tập!"
    ]

    embed = discord.Embed(
        title="🎓 Lời chúc thi cử",
        description=random.choice(messages),
        color=0xF0B85A
    )
    embed.set_footer(
    text="💖 Minori sẽ luôn ở đây để cổ vũ bạn. Chúc bạn thi thật tốt nhé!"
    )

    await interaction.response.send_message(
        embed=embed
    )

# =========================
# CHARACTER IMAGE VIEW
# =========================

class CharacterImageView(discord.ui.View):

    def __init__(self, char):
        super().__init__(timeout=120)

        self.char = char
        self.index = 0

    def make_embed(self):

        embed = discord.Embed(
            title=self.char["name"],
            description=self.char["info"],
            color=self.char["color"]
        )

        embed.add_field(
            name="🎤 Unit",
            value=self.char["unit"]
        )

        embed.add_field(
            name="🎂 Birthday",
            value=self.char["birthday"]
        )

        embed.add_field(
            name="💖 Quote",
            value=self.char["quote"],
            inline=False
        )

        images = self.char.get("images", [])

        if images:
            embed.set_image(
                url=images[self.index]
            )

        if images:

            captions = self.char.get("captions", [])

            footer_text = f"Ảnh {self.index+1}/{len(images)}"

            if self.index < len(captions):
                footer_text += f" • {captions[self.index]}"

            embed.set_footer(text=footer_text)
        else:
            embed.set_footer(
                text="Project SEKAI Character Information"
            )
        return embed

    @discord.ui.button(
        emoji="⬅️",
        style=discord.ButtonStyle.secondary
    )
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.index -= 1

        if self.index < 0:
            self.index = len(self.char["images"]) - 1

        await interaction.response.edit_message(
            embed=self.make_embed(),
            view=self
        )

    @discord.ui.button(
        emoji="➡️",
        style=discord.ButtonStyle.secondary
    )
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        self.index += 1

        if self.index >= len(self.char["images"]):
            self.index = 0

        await interaction.response.edit_message(
            embed=self.make_embed(),
            view=self
        )

# =========================
# =========================
# INVENTORY SELECT
# =========================

class InventorySelect(discord.ui.Select):

    def __init__(self, owned_cards):

        options = []

        for card_id in owned_cards:

            if card_id not in CARDS:
                continue

            card = CARDS[card_id]

            options.append(
                discord.SelectOption(
                    label=card["name"][:100],
                    description=f"{card['rarity']} | {card['character']}"[:100],
                    value=card_id
                )
            )

        super().__init__(
            placeholder="Chọn card để xem ảnh...",
            options=options[:25]
        )

    async def callback(
        self,
        interaction: discord.Interaction
    ):

        card_id = self.values[0]

        card = CARDS[card_id]

        embed = discord.Embed(
            title=card["name"],
            description=(
                f"{card['rarity']}\n"
                f"{card['character']}"
            ),
            color=0xF0B85A
        )

        embed.set_image(
            url=card["image"]
        )

        await interaction.response.edit_message(
            embed=embed,
            view=self.view
        )


# =========================
# INVENTORY VIEW
# =========================

class InventoryView(discord.ui.View):

    def __init__(self, owned_cards):

        super().__init__(
            timeout=300
        )

        self.add_item(
            InventorySelect(
                owned_cards
            )
        )

# =========================
# /NHAN_VAT
# =========================

@bot.tree.command(
    name="nhan_vat",
    description="Xem thông tin nhân vật"
)
async def nhan_vat(
    interaction: discord.Interaction,
    nhan_vat: str
):

    nhan_vat = nhan_vat.lower()

    if nhan_vat not in CHARACTERS:

        await interaction.response.send_message(
            "❌ Nhân vật này chưa có dữ liệu.",
            ephemeral=True
        )
        return

    char = CHARACTERS[nhan_vat]

    embed = discord.Embed(
        title=char["name"],
        description=char["info"],
        color=char["color"]
    )

    embed.add_field(
        name="🎤 Unit",
        value=char["unit"],
        inline=True
    )

    embed.add_field(
        name="🎂 Birthday",
        value=char["birthday"],
        inline=True
    )

    embed.add_field(
        name="💖 Quote",
        value=char["quote"],
        inline=False
    )

    images = char.get("images")

    if not images and "image" in char:
        images = [char["image"]]

    if not images:
        images = []

    if images:

        if len(images) > 1:

            view = CharacterImageView(char)

            await interaction.response.send_message(
                embed=view.make_embed(),
                view=view
            )

        else:

            embed.set_image(
                url=images[0]
            )

            await interaction.response.send_message(
                embed=embed
            )

@nhan_vat.autocomplete("nhan_vat")
async def nhan_vat_autocomplete(
    interaction: discord.Interaction,
    current: str
):

    choices = []

    for key, data in CHARACTERS.items():

        if current.lower() in data["name"].lower():

            choices.append(
                app_commands.Choice(
                    name=data["name"],
                    value=key
                )
            )

    return choices[:25]

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

    embed.set_thumbnail(
        url=interaction.user.display_avatar.url
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

    today = (
        datetime.now(timezone.utc) + timedelta(hours=7)
    ).strftime("%Y-%m-%d")

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
# COOLDOWN /PLAY_SOLO
# =========================

play_solo_cooldowns = {}

# =========================
# COOLDOWN /GACHA
# =========================

gacha_cooldowns = {}

# =========================
# /GACHA
# =========================

@app_commands.choices(
    amount=[
        app_commands.Choice(name="x1", value=1),
        app_commands.Choice(name="x10", value=10)
    ]
)
@bot.tree.command(
    name="gacha",
    description="Quay thẻ Project SEKAI"
)
async def gacha(
    interaction: discord.Interaction,
    amount: app_commands.Choice[int]
):

    user_id = interaction.user.id
    now = datetime.now().timestamp()

    if user_id in gacha_cooldowns:

        remaining = gacha_cooldowns[user_id] - now

        if remaining > 0:

            await interaction.response.send_message(
                f"⏳ Vui lòng chờ {remaining:.1f} giây trước khi quay tiếp.",
                ephemeral=True
            )
            return

    gacha_cooldowns[user_id] = now + 10

    rolls = amount.value
    cost = 300 * rolls

    user = get_user(user_id)

    if user["gems"] < cost:

        await interaction.response.send_message(
            f"❌ Bạn cần {cost} 💎 để quay gacha x{rolls}."
        )
        return

    await interaction.response.defer()

    user["gems"] -= cost

    inventory = get_inventory(user_id)

    results = []
    duplicate_count = 0

    for _ in range(rolls):

        card_id = roll_card()

        if card_id in inventory:

            duplicate_count += 1
            user["gems"] += 150

        else:

            add_card(
                user_id,
                card_id
            )

            inventory.append(card_id)

        results.append(card_id)

    update_user(user)

    result_text = ""

    for card_id in results:

        card = CARDS[card_id]

        result_text += (
            f"⭐ {card['name']}\n"
            f"   {card['rarity']} • {card['character']}\n\n"
        )

    embed = discord.Embed(
        title=f"🎊 Gacha x{rolls}",
        description=result_text,
        color=0xF0B85A
    )

    embed.add_field(
        name="💎 Đá đã tiêu",
        value=str(cost),
        inline=True
    )

    embed.add_field(
        name="💎 Đá còn lại",
        value=str(user["gems"]),
        inline=True
    )

    if duplicate_count > 0:

        embed.add_field(
            name="♻️ Card trùng",
            value=(
                f"{duplicate_count} card\n"
                f"+{duplicate_count * 150} 💎"
            ),
            inline=False
        )

    embed.set_footer(
        text="Chúc bạn may mắn ở lần quay tiếp theo! ✨"
    )

    if rolls == 10:

        grid = create_gacha_grid(results)

        file = discord.File(
            fp=grid,
            filename="gacha10.png"
        )

        embed.set_image(
            url="attachment://gacha10.png"
        )

        await interaction.followup.send(
            embed=embed,
            file=file
        )

    else:

        last_card = CARDS[
            results[-1]
        ]

        embed.set_image(
            url=last_card["image"]
        )

        await interaction.followup.send(
            embed=embed
        )

# =========================
# /INVENTORY
# =========================

@bot.tree.command(
    name="inventory",
    description="Xem bộ sưu tập thẻ của bạn"
)
async def inventory(
    interaction: discord.Interaction
):

    user_id = interaction.user.id

    owned_cards = get_inventory(
        user_id
    )

    if not owned_cards:

        await interaction.response.send_message(
            "📦 Bạn chưa sở hữu card nào."
        )
        return

    embed = discord.Embed(
        title=f"📦 Inventory của {interaction.user.display_name}",
        description=(
            "Chọn một card bên dưới để xem ảnh."
        ),
        color=0x4FC3F7
    )

    embed.set_footer(
        text=f"Tổng số card: {len(owned_cards)}"
    )

    await interaction.response.send_message(
        embed=embed,
        view=InventoryView(
            owned_cards
        )
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

    user_id = interaction.user.id
    now = datetime.now().timestamp()

    if user_id in play_solo_cooldowns:
        remaining = play_solo_cooldowns[user_id] - now

        if remaining > 0:
            await interaction.response.send_message(
                f"⏳ Vui lòng chờ {remaining:.1f} giây trước khi chơi tiếp.",
                ephemeral=True
            )
            return

    play_solo_cooldowns[user_id] = now + 5

    user = get_user(user_id)

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
# /Tim nhac
# =========================

@bot.tree.command(
    name="tim_kiem_nhac",
    description="Tìm kiếm nhạc của game"
)
@app_commands.choices(
    bai_hat=[
        app_commands.Choice(
            name="⭐ Hoshi ni Ichiban Chikai Basho (Leo/need)",
            value="hoshi"
        )
    ]
)
async def phat_nhac(
    interaction: discord.Interaction,
    bai_hat: app_commands.Choice[str]
):
    music = MUSIC_FILES[bai_hat.value]

    # Kiểm tra file có tồn tại hay không
    if not os.path.isfile(music["path"]):
        await interaction.response.send_message(
            "❌ Không tìm thấy file nhạc.",
            ephemeral=True
        )
        return

    # Nếu có thì gửi file
    await interaction.response.send_message(
        content=f"🎶 **{music['title']}**",
        file=discord.File(music["path"])
    )

# =========================
# /KICK
# =========================

@bot.tree.command(
    name="kick",
    description="Kick một thành viên khỏi máy chủ"
)
@app_commands.checks.has_permissions(administrator=True)
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "Không có lý do"
):
    # Không cho kick chính mình
    if member == interaction.user:
        await interaction.response.send_message(
            "❌ Bạn không thể kick chính mình.",
            ephemeral=True
        )
        return

    # Không cho kick chủ server
    if member == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Không thể kick chủ server.",
            ephemeral=True
        )
        return

    # Bot phải có role cao hơn
    bot_member = interaction.guild.get_member(bot.user.id)

    if bot_member is None or member.top_role >= bot_member.top_role:
        await interaction.response.send_message(
            "❌ Vai trò của mình thấp hơn hoặc bằng thành viên này.",
            ephemeral=True
        )
        return

    try:
        await member.kick(reason=reason)

        await interaction.response.send_message(
            f"👢 Đã kick {member.mention}\n"
            f"📝 Lý do: {reason}"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Mình không có quyền kick thành viên này.",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Đã xảy ra lỗi: {e}",
            ephemeral=True
        )


@kick.error
async def kick_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❌ Chỉ quản trị viên (Administrator) mới có thể sử dụng lệnh này.",
            ephemeral=True
        )

# =========================
# /MUTE
# =========================

@bot.tree.command(
    name="mute",
    description="Timeout (mute) một thành viên"
)
@app_commands.checks.has_permissions(administrator=True)
async def mute(
    interaction: discord.Interaction,
    member: discord.Member,
    minutes: app_commands.Range[int, 1, 40320],
    reason: str = "Không có lý do"
):
    # Không cho mute chính mình
    if member == interaction.user:
        await interaction.response.send_message(
            "❌ Bạn không thể mute chính mình.",
            ephemeral=True
        )
        return

    # Không cho mute chủ server
    if member == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Không thể mute chủ server.",
            ephemeral=True
        )
        return

    # Bot phải có role cao hơn
    bot_member = interaction.guild.get_member(bot.user.id)

    if bot_member is None or member.top_role >= bot_member.top_role:
        await interaction.response.send_message(
            "❌ Vai trò của mình thấp hơn hoặc bằng thành viên này.",
            ephemeral=True
        )
        return

    try:
        until = datetime.now(timezone.utc) + timedelta(minutes=minutes)

        await member.edit(
            timed_out_until=until,
            reason=reason
        )

        await interaction.response.send_message(
            f"🔇 Đã mute {member.mention} trong **{minutes} phút**.\n"
            f"📝 Lý do: {reason}"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Mình không có quyền mute thành viên này.",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Đã xảy ra lỗi: {e}",
            ephemeral=True
        )


@mute.error
async def mute_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❌ Chỉ quản trị viên (Administrator) mới có thể sử dụng lệnh này.",
            ephemeral=True
        )

# =========================
# Unmute
# =========================

@bot.tree.command(
    name="unmute",
    description="Bỏ timeout (unmute) một thành viên"
)
@app_commands.checks.has_permissions(administrator=True)
async def unmute(
    interaction: discord.Interaction,
    member: discord.Member
):
    # Không cho unmute chủ server
    if member == interaction.guild.owner:
        await interaction.response.send_message(
            "❌ Không thể bỏ mute chủ server.",
            ephemeral=True
        )
        return

    # Bot phải có role cao hơn
    bot_member = interaction.guild.get_member(bot.user.id)

    if bot_member is None or member.top_role >= bot_member.top_role:
        await interaction.response.send_message(
            "❌ Vai trò của mình thấp hơn hoặc bằng thành viên này.",
            ephemeral=True
        )
        return

    try:
        await member.edit(
            timed_out_until=None,
            reason="Unmute"
        )

        await interaction.response.send_message(
            f"🔊 Đã bỏ mute cho {member.mention}."
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Mình không có quyền bỏ mute thành viên này.",
            ephemeral=True
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ Đã xảy ra lỗi: {e}",
            ephemeral=True
        )


@unmute.error
async def unmute_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message(
            "❌ Chỉ quản trị viên (Administrator) mới có thể sử dụng lệnh này.",
            ephemeral=True
        )

# =========================
# BẮT LỖI
# =========================

@bot.tree.error
async def on_error(interaction, error):

    print("\n===== ERROR =====")

    traceback.print_exception(
        type(error),
        error,
        error.__traceback__
    )

    try:
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "❌ Đã xảy ra lỗi.",
                ephemeral=True
            )
    except:
        pass
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

print("BOT FILE LOADED 999999")
print("TOKEN OK")
print("STARTING BOT...")

bot.run(TOKEN)
