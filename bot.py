# pip install python-telegram-bot==21.6
import os
from telegram import InlineKeyboardButton as Btn, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

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

LANGS = {
    "ps": {
        "name": "پښتو",
        "welcome": "ښه راغلاست! القريشي فودز ته 🌿\nیوه برخه وټاکئ:",
        "btn": ["📦 محصولات", "🕙 د کار وخت", "📞 اړیکه", "📍 موقعیت", "🌐 ژبه", "ℹ️ زموږ په اړه"],
        "back": "🔙 اصلي مینو",
        "products": "📦 زموږ محصولات:\n• مصالحې\n• بوټي (اعشاب)\n• وچې میوې (مکسرات)\n• قهوه\n• کجورې",
        "hours": "🕙 د کار وخت:\nله ۱۰ سهار تر ۱۰ شپې",
        "contact": "📞 اړیکه:",
        "location": "📍 موقعیت:",
        "about": "ℹ️ د القريشي فودز په اړه:\nالقريشي فودز د مصالحو، بوټو (اعشابو)، فاخرو مکسراتو، قهوې او کجورو د عمده او پرچون پلور شرکت دی.",
    },
    "fa": {
        "name": "دری",
        "welcome": "خوش آمدید به القریشی فودز 🌿\nیک بخش را انتخاب کنید:",
        "btn": ["📦 محصولات", "🕙 ساعات کار", "📞 تماس", "📍 موقعیت", "🌐 زبان", "ℹ️ درباره ما"],
        "back": "🔙 منوی اصلی",
        "products": "📦 محصولات ما:\n• ادویه‌جات\n• گیاهان (اعشاب)\n• میوه‌های خشک و مغزها\n• قهوه\n• خرما",
        "hours": "🕙 ساعات کار:\nاز ساعت ۱۰ صبح تا ۱۰ شب",
        "contact": "📞 تماس:",
        "location": "📍 موقعیت:",
        "about": "ℹ️ درباره القریشی فودز:\nالقریشی فودز شرکت عمده‌فروشی و پرچون‌فروشی ادویه‌جات، گیاهان (اعشاب)، مغزهای مرغوب، انواع قهوه و خرما است.",
    },
    "ar": {
        "name": "العربية",
        "welcome": "أهلاً بكم في القريشي فودز 🌿\nاختر قسماً:",
        "btn": ["📦 منتجاتنا", "🕙 مواعيد العمل", "📞 تواصل معنا", "📍 الموقع", "🌐 اللغة", "ℹ️ من نحن"],
        "back": "🔙 القائمة الرئيسية",
        "products": "📦 منتجاتنا:\n• البهارات\n• الأعشاب\n• المكسرات الفاخرة\n• القهوة\n• التمور",
        "hours": "🕙 مواعيد العمل:\nمن ١٠ صباحاً وحتى ١٠ مساءً",
        "contact": "📞 تواصل معنا:",
        "location": "📍 الموقع:",
        "about": "ℹ️ عن القريشي فودز:\nالقريشي فودز للتجارة بالجملة والتجزئة للبهارات والأعشاب والمكسرات الفاخرة وأنواع القهوة والتمور.",
    },
    "hi": {
        "name": "हिन्दी",
        "welcome": "अल क़ुरैशी फ़ूड्स में आपका स्वागत है 🌿\nकृपया एक विकल्प चुनें:",
        "btn": ["📦 उत्पाद", "🕙 कार्य समय", "📞 संपर्क", "📍 लोकेशन", "🌐 भाषा", "ℹ️ हमारे बारे में"],
        "back": "🔙 मुख्य मेनू",
        "products": "📦 हमारे उत्पाद:\n• मसाले\n• जड़ी-बूटियाँ\n• ड्राई फ्रूट्स और मेवे\n• कॉफ़ी\n• खजूर",
        "hours": "🕙 कार्य समय:\nसुबह 10 बजे से रात 10 बजे तक",
        "contact": "📞 संपर्क:",
        "location": "📍 लोकेशन:",
        "about": "ℹ️ अल क़ुरैशी फ़ूड्स के बारे में:\nअल क़ुरैशी फ़ूड्स मसालों, जड़ी-बूटियों, प्रीमियम मेवों, कॉफ़ी और खजूर का थोक और खुदरा व्यापार करती है।",
    },
    "en": {
        "name": "English",
        "welcome": "Welcome to Al Quraishi Foods 🌿\nChoose a section:",
        "btn": ["📦 Products", "🕙 Working hours", "📞 Contact", "📍 Location", "🌐 Language", "ℹ️ About us"],
        "back": "🔙 Main menu",
        "products": "📦 Our products:\n• Spices\n• Herbs\n• Premium nuts\n• Coffee\n• Dates",
        "hours": "🕙 Working hours:\n10 AM to 10 PM",
        "contact": "📞 Contact:",
        "location": "📍 Location:",
        "about": "ℹ️ About Al Quraishi Foods:\nAl Quraishi Foods is a wholesale and retail trader of spices, herbs, premium nuts, coffee and dates.",
    },
}


def lang_menu():
    items = [Btn(v["name"], callback_data=f"lang:{k}") for k, v in LANGS.items()]
    return InlineKeyboardMarkup([items[:3], items[3:]])


def main_menu(code):
    b = LANGS[code]["btn"]
    return InlineKeyboardMarkup([
        [Btn(b[0], callback_data="products"), Btn(b[5], callback_data="about")],
        [Btn(b[1], callback_data="hours"), Btn(b[2], callback_data="contact")],
        [Btn(b[3], callback_data="location"), Btn(b[4], callback_data="chooselang")],
    ])


def back_menu(code):
    return InlineKeyboardMarkup([[Btn(LANGS[code]["back"], callback_data="menu")]])


def contact_menu(code):
    return InlineKeyboardMarkup([
        [Btn("WhatsApp", url=WHATSAPP), Btn("Instagram", url=INSTAGRAM)],
        [Btn("Telegram", url=TELEGRAM), Btn("TikTok", url=TIKTOK)],
        [Btn(LANGS[code]["back"], callback_data="menu")],
    ])


def location_menu(code):
    return InlineKeyboardMarkup([
        [Btn(LANGS[code]["btn"][3], url=MAP_LINK)],
        [Btn(LANGS[code]["back"], callback_data="menu")],
    ])


async def show(q, text, markup):
    # هماغه پیغام بدلوي، نوی پیغام نه جوړوي
    try:
        await q.edit_message_text(text, reply_markup=markup)
    except BadRequest:
        pass


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 ژبه وټاکئ / زبان / اللغة / भाषा / Language", reply_markup=lang_menu()
    )


async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "chooselang":
        await show(q, "🌐", lang_menu())
        return
    if data.startswith("lang:"):
        ctx.user_data["lang"] = data.split(":")[1]
        data = "menu"

    code = ctx.user_data.get("lang", "en")
    t = LANGS[code]

    if data == "menu":
        await show(q, t["welcome"], main_menu(code))
    elif data == "contact":
        await show(q, f"{t['contact']}\n📱 {PHONE} (WhatsApp)", contact_menu(code))
        await q.message.reply_contact(phone_number=PHONE, first_name="Al Quraishi Foods")
    elif data == "location":
        await show(q, f"{t['location']}\n{MAP_LINK}", location_menu(code))
        if LAT is not None and LON is not None:
            await q.message.reply_location(latitude=LAT, longitude=LON)
    elif data in ("products", "hours", "about"):
        await show(q, t[data], back_menu(code))


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
