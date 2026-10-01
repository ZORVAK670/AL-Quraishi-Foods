# pip install python-telegram-bot==21.6
import os
from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "BOTFATHER_TOKEN_HERE")

# ---- دلته خپل معلومات ولیکئ ----
PHONE = "+000000000000"
INSTAGRAM = "@alquraishifoods"
MAP_LINK = "https://maps.google.com/?q=YOUR_LOCATION"

LANGS = {
    "ps": {
        "name": "پښتو",
        "welcome": "ښه راغلاست! القريشي فودز ته 🌿\nیوه برخه وټاکئ:",
        "btn": ["📦 محصولات", "🕙 د کار وخت", "📞 اړیکه", "📍 موقعیت", "🌐 ژبه"],
        "products": "📦 زموږ محصولات:\n• مصالحې\n• بوټي (اعشاب)\n• وچې میوې (مکسرات)\n• قهوه\n• کجورې",
        "hours": "🕙 د کار وخت:\nله ۱۰ سهار تر ۱۰ شپې",
        "contact": "📞 اړیکه:",
        "location": "📍 موقعیت:",
    },
    "fa": {
        "name": "دری",
        "welcome": "خوش آمدید به القریشی فودز 🌿\nیک بخش را انتخاب کنید:",
        "btn": ["📦 محصولات", "🕙 ساعات کار", "📞 تماس", "📍 موقعیت", "🌐 زبان"],
        "products": "📦 محصولات ما:\n• ادویه‌جات\n• گیاهان (اعشاب)\n• میوه‌های خشک و مغزها\n• قهوه\n• خرما",
        "hours": "🕙 ساعات کار:\nاز ساعت ۱۰ صبح تا ۱۰ شب",
        "contact": "📞 تماس:",
        "location": "📍 موقعیت:",
    },
    "ar": {
        "name": "العربية",
        "welcome": "أهلاً بكم في القريشي فودز 🌿\nاختر قسماً:",
        "btn": ["📦 منتجاتنا", "🕙 مواعيد العمل", "📞 تواصل معنا", "📍 الموقع", "🌐 اللغة"],
        "products": "📦 منتجاتنا:\n• البهارات\n• الأعشاب\n• المكسرات الفاخرة\n• القهوة\n• التمور",
        "hours": "🕙 مواعيد العمل:\nمن ١٠ صباحاً وحتى ١٠ مساءً",
        "contact": "📞 تواصل معنا:",
        "location": "📍 الموقع:",
    },
    "hi": {
        "name": "हिन्दी",
        "welcome": "अल क़ुरैशी फ़ूड्स में आपका स्वागत है 🌿\nकृपया एक विकल्प चुनें:",
        "btn": ["📦 उत्पाद", "🕙 कार्य समय", "📞 संपर्क", "📍 लोकेशन", "🌐 भाषा"],
        "products": "📦 हमारे उत्पाद:\n• मसाले\n• जड़ी-बूटियाँ\n• ड्राई फ्रूट्स और मेवे\n• कॉफ़ी\n• खजूर",
        "hours": "🕙 कार्य समय:\nसुबह 10 बजे से रात 10 बजे तक",
        "contact": "📞 संपर्क:",
        "location": "📍 लोकेशन:",
    },
    "en": {
        "name": "English",
        "welcome": "Welcome to Al Quraishi Foods 🌿\nChoose a section:",
        "btn": ["📦 Products", "🕙 Working hours", "📞 Contact", "📍 Location", "🌐 Language"],
        "products": "📦 Our products:\n• Spices\n• Herbs\n• Premium nuts\n• Coffee\n• Dates",
        "hours": "🕙 Working hours:\n10 AM to 10 PM",
        "contact": "📞 Contact:",
        "location": "📍 Location:",
    },
}


def lang_menu():
    items = [Btn(v["name"], callback_data=f"lang:{k}") for k, v in LANGS.items()]
    return InlineKeyboardMarkup([items[:3], items[3:]])


def main_menu(code):
    b = LANGS[code]["btn"]
    return InlineKeyboardMarkup([
        [Btn(b[0], callback_data="products"), Btn(b[1], callback_data="hours")],
        [Btn(b[2], callback_data="contact"), Btn(b[3], callback_data="location")],
        [Btn(b[4], callback_data="chooselang")],
    ])


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 ژبه وټاکئ / زبان / اللغة / भाषा / Language", reply_markup=lang_menu()
    )


async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "chooselang":
        await q.message.reply_text("🌐", reply_markup=lang_menu())
        return
    if data.startswith("lang:"):
        ctx.user_data["lang"] = data.split(":")[1]
        code = ctx.user_data["lang"]
        await q.message.reply_text(LANGS[code]["welcome"], reply_markup=main_menu(code))
        return

    code = ctx.user_data.get("lang", "en")
    t = LANGS[code]
    if data == "contact":
        text = f"{t['contact']}\n{PHONE}\nInstagram: {INSTAGRAM}"
    elif data == "location":
        text = f"{t['location']}\n{MAP_LINK}"
    else:
        text = t[data]
    await q.message.reply_text(text, reply_markup=main_menu(code))


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
