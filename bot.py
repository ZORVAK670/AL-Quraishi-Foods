# pip install python-telegram-bot==21.6
import os
from telegram import (
    InlineKeyboardButton as Btn,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.environ.get("BOT_TOKEN", "BOTFATHER_TOKEN_HERE")

# ---- دلته خپل معلومات ولیکئ ----
PHONE = "+96599407958"
WHATSAPP = "https://wa.me/96599407958"
INSTAGRAM = "https://instagram.com/alquraishifoods"
TELEGRAM = "https://t.me/Alquraishifoods"
TIKTOK = "https://www.tiktok.com/@alquraishifoods"
MAP_LINK = "https://maps.app.goo.gl/txw6yBjew3kBzY137?g_st=ac"
LAT = 29.32324
LON = 47.93314

# د دکمو ترتیب په "btn" لیست کې:
ACTIONS = ["products", "hours", "contact", "location", "language", "about", "social"]

LANGS = {
    "ps": {
        "name": "پښتو",
        "welcome": "ښه راغلاست! القريشي فودز ته 🌿\nله لاندې مینو یوه برخه وټاکئ.",
        "btn": ["📦 محصولات", "🕙 د کار وخت", "📞 اړیکه", "📍 موقعیت", "🌐 ژبه", "ℹ️ زموږ په اړه", "📲 ټولنیز رسنۍ"],
        "products": "📦 زموږ محصولات:\n• مصالحې\n• بوټي (اعشاب)\n• وچې میوې (مکسرات)\n• قهوه\n• کجورې",
        "hours": "🕙 د کار وخت:\nله ۱۰ سهار تر ۱۰ شپې",
        "contact": "📞 اړیکه:",
        "location": "📍 موقعیت:",
        "about": "ℹ️ د القريشي فودز په اړه:\nالقريشي فودز د مصالحو، بوټو (اعشابو)، فاخرو مکسراتو، قهوې او کجورو د عمده او پرچون پلور شرکت دی.",
    },
    "fa": {
        "name": "دری",
        "welcome": "خوش آمدید به القریشی فودز 🌿\nاز منوی پایین یک بخش را انتخاب کنید.",
        "btn": ["📦 محصولات", "🕙 ساعات کار", "📞 تماس", "📍 موقعیت", "🌐 زبان", "ℹ️ درباره ما", "📲 شبکه‌های اجتماعی"],
        "products": "📦 محصولات ما:\n• ادویه‌جات\n• گیاهان (اعشاب)\n• میوه‌های خشک و مغزها\n• قهوه\n• خرما",
        "hours": "🕙 ساعات کار:\nاز ساعت ۱۰ صبح تا ۱۰ شب",
        "contact": "📞 تماس:",
        "location": "📍 موقعیت:",
        "about": "ℹ️ درباره القریشی فودز:\nالقریشی فودز شرکت عمده‌فروشی و پرچون‌فروشی ادویه‌جات، گیاهان (اعشاب)، مغزهای مرغوب، انواع قهوه و خرما است.",
    },
    "ar": {
        "name": "العربية",
        "welcome": "أهلاً بكم في القريشي فودز 🌿\nاختر قسماً من القائمة بالأسفل.",
        "btn": ["📦 منتجاتنا", "🕙 مواعيد العمل", "📞 تواصل معنا", "📍 الموقع", "🌐 اللغة", "ℹ️ من نحن", "📲 مواقع التواصل"],
        "products": "📦 منتجاتنا:\n• البهارات\n• الأعشاب\n• المكسرات الفاخرة\n• القهوة\n• التمور",
        "hours": "🕙 مواعيد العمل:\nمن ١٠ صباحاً وحتى ١٠ مساءً",
        "contact": "📞 تواصل معنا:",
        "location": "📍 الموقع:",
        "about": "ℹ️ عن القريشي فودز:\nالقريشي فودز للتجارة بالجملة والتجزئة للبهارات والأعشاب والمكسرات الفاخرة وأنواع القهوة والتمور.",
    },
    "hi": {
        "name": "हिन्दी",
        "welcome": "अल क़ुरैशी फ़ूड्स में आपका स्वागत है 🌿\nनीचे के मेनू से एक विकल्प चुनें।",
        "btn": ["📦 उत्पाद", "🕙 कार्य समय", "📞 संपर्क", "📍 लोकेशन", "🌐 भाषा", "ℹ️ हमारे बारे में", "📲 सोशल मीडिया"],
        "products": "📦 हमारे उत्पाद:\n• मसाले\n• जड़ी-बूटियाँ\n• ड्राई फ्रूट्स और मेवे\n• कॉफ़ी\n• खजूर",
        "hours": "🕙 कार्य समय:\nसुबह 10 बजे से रात 10 बजे तक",
        "contact": "📞 संपर्क:",
        "location": "📍 लोकेशन:",
        "about": "ℹ️ अल क़ुरैशी फ़ूड्स के बारे में:\nअल क़ुरैशी फ़ूड्स मसालों, जड़ी-बूटियों, प्रीमियम मेवों, कॉफ़ी और खजूर का थोक और खुदरा व्यापार करती है।",
    },
    "en": {
        "name": "English",
        "welcome": "Welcome to Al Quraishi Foods 🌿\nChoose a section from the menu below.",
        "btn": ["📦 Products", "🕙 Working hours", "📞 Contact", "📍 Location", "🌐 Language", "ℹ️ About us", "📲 Social media"],
        "products": "📦 Our products:\n• Spices\n• Herbs\n• Premium nuts\n• Coffee\n• Dates",
        "hours": "🕙 Working hours:\n10 AM to 10 PM",
        "contact": "📞 Contact:",
        "location": "📍 Location:",
        "about": "ℹ️ About Al Quraishi Foods:\nAl Quraishi Foods is a wholesale and retail trader of spices, herbs, premium nuts, coffee and dates.",
    },
}

# هره دکمه → (ژبه، عمل)
LABELS = {}
for _code, _v in LANGS.items():
    for _action, _label in zip(ACTIONS, _v["btn"]):
        LABELS[_label] = (_code, _action)


def keyboard(code):
    """د ټيلګرام لاندې دايمي مینو (د ننوتلو ځای ته نږدې)"""
    b = LANGS[code]["btn"]
    return ReplyKeyboardMarkup(
        [[b[0], b[5]], [b[1], b[2]], [b[6], b[3]], [b[4]]],
        resize_keyboard=True,
        is_persistent=True,
    )


def lang_menu():
    items = [Btn(v["name"], callback_data=f"lang:{k}") for k, v in LANGS.items()]
    return InlineKeyboardMarkup([items[:3], items[3:]])


def contact_links():
    return InlineKeyboardMarkup([[Btn("WhatsApp", url=WHATSAPP)]])


def social_links():
    return InlineKeyboardMarkup([
        [Btn("Instagram", url=INSTAGRAM), Btn("TikTok", url=TIKTOK)],
        [Btn("Telegram", url=TELEGRAM)],
    ])


def map_button(code):
    return InlineKeyboardMarkup([[Btn(LANGS[code]["btn"][3], url=MAP_LINK)]])


async def ask_language(msg):
    await msg.reply_text(
        "🌐 ژبه وټاکئ / زبان / اللغة / भाषा / Language", reply_markup=lang_menu()
    )


async def do_action(msg, code, action):
    t = LANGS[code]
    if action == "language":
        await ask_language(msg)
    elif action == "contact":
        await msg.reply_text(f"{t['contact']}\n📱 {PHONE} (WhatsApp)", reply_markup=contact_links())
        await msg.reply_contact(phone_number=PHONE, first_name="Al Quraishi Foods")
    elif action == "social":
        await msg.reply_text(t["btn"][6], reply_markup=social_links())
    elif action == "location":
        await msg.reply_text(f"{t['location']}\n{MAP_LINK}", reply_markup=map_button(code))
        if LAT is not None and LON is not None:
            await msg.reply_location(latitude=LAT, longitude=LON)
    else:
        await msg.reply_text(t[action])


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await ask_language(update.message)


async def on_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    code = q.data.split(":")[1]
    ctx.user_data["lang"] = code
    await q.message.reply_text(LANGS[code]["welcome"], reply_markup=keyboard(code))
    try:
        await q.message.delete()
    except Exception:
        pass


async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text
    code = ctx.user_data.get("lang")
    action = None

    if code and text in LANGS[code]["btn"]:
        action = ACTIONS[LANGS[code]["btn"].index(text)]
    elif text in LABELS:
        code, action = LABELS[text]
        ctx.user_data["lang"] = code

    if action:
        await do_action(msg, code, action)
    elif code:
        await msg.reply_text(LANGS[code]["welcome"], reply_markup=keyboard(code))
    else:
        await ask_language(msg)


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(on_lang, pattern="^lang:"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
app.run_polling()
