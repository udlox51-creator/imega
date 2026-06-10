"""
╔══════════════════════════════════════════════════════════════╗
║         RASM TINIQLASHTIRUVCHI TELEGRAM BOT                  ║
║         @imega_foto_4k_bot — Pro versiya v3.1 (tuzatilgan)  ║
╚══════════════════════════════════════════════════════════════╝
"""

import asyncio  # ← TUZATILDI: import qo'shildi
import io, json, logging, os, time
from datetime import datetime, date, timedelta
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ═══════════════════════════════════════════
#   SOZLAMALAR
# ═══════════════════════════════════════════
BOT_TOKEN      = "8615927460:AAEtFxnz1K5OyqCdcqgVXxu6IxLwT7XWpBg"
PICWISH_KEY    = "wxhy8t9jo72vcgynr"
ADMIN_ID       = 8330377593
KARTA_RAQAM    = "9860080151682814"
KARTA_EGASI    = "Axadov A"
PREMIUM_NARX   = 10000
PREMIUM_KUN    = 30
BEPUL_LIMIT    = 5
PREMIUM_LIMIT  = 30
BOT_USERNAME   = "@imega_foto_4k_bot"
ADMIN_PAROL    = "admin2024"

PICWISH_CREATE_URL = "https://techhk.aoscdn.com/api/tasks/visual/scale"
PICWISH_RESULT_URL = "https://techhk.aoscdn.com/api/tasks/visual/scale/{task_id}"

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# ═══════════════════════════════════════════
#   TILLAR
# ═══════════════════════════════════════════
TILLAR = {
    "uz": {
        "til_nomi": "🇺🇿 O'zbek",
        "bosh_menu": "👋 Xush kelibsiz!\n\nQuyidagi menyudan tanlang:",
        "til_tanlang": "🌐 Tilni tanlang:",
        "sifat_tanlang": "🎚 Sifatni tanlang:",
        "rasm_yukor": "⏬ Rasm qabul qilinmoqda...",
        "qoldi": "📊 Bugun qoldi: {} ta",
        "jarayon": "⏳ Tiniqlashtir'lyapti...\nBiroz kuting...",
        "tayyor": "✨ Tayyor! Sifat: {}\n🤖 {} orqali tiniqlashtirildi\n📊 Bugun qoldi: {} ta",
        "limit_bepul": "⛔ Kunlik limit tugadi! ({} ta/kun)\n\n⭐ Premium oling — 30 ta/kun + 4K!",
        "limit_premium": "⛔ Kunlik limit tugadi! (30 ta/kun)\n⏰ Ertaga yangilanadi.",
        "premium_bor": "✅ Siz Premium foydalanuvchisiz!\n📅 Tugash: {}",
        "premium_info": "⭐ Premium — {:,} so'm/oy\n\n✅ Kuniga 30 ta rasm\n✅ 4K sifat\n✅ Ustuvor ishlov",
        "tolov_info": "💳 To'lov ma'lumotlari:\n\n💰 Summa: {:,} so'm\n🏦 Karta: <code>{}</code>\n👤 Egasi: {}\n\n📌 To'lov qilgach:\n1️⃣ To'lov chekini (screenshot) yuboring\n⚠️ Chek yuborishda /chek buyrug'ini bosing!\n\n❗ Izohga ID yozing: <code>{}</code>",
        "chek_yuborish": "📸 /chek buyrug'ini bosib chek rasmini yuboring:",
        "chek_qabul": "✅ Chekingiz qabul qilindi!\n⏳ Admin tekshiradi, tez orada javob beradi.",
        "chek_kutilmoqda": "⏳ Oldingi to'lovingiz ko'rib chiqilmoqda!",
        "holat": "📊 Hisobingiz:\n\n👤 Ism: {}\n🆔 ID: {}\n⭐ Obuna: {}\n📅 Tugash: {}\n📸 Bugun: {} ta\n🔢 Qoldi: {} ta\n🖼 Jami: {} ta\n👥 Referral: {} ta → {} bonus",
        "premium_label": "Premium ✅",
        "oddiy_label": "Bepul",
        "blok": "🚫 Siz bloklangansiz.",
        "premium_kerak": "🔒 Bu sifat faqat Premium!\n\n⭐ Premium: {:,} so'm/oy",
        "referral_matn": "👥 Referral:\n\n🔗 Havola:\n{}\n\n✅ Har taklif = +1 bepul rasm!\n📊 Taklif: {} ta\n🎁 Bonus: {} ta\n💰 Qolgan: {} ta",
        "bonus_xabar": "🎁 +1 bonus rasm! Do'stingiz qo'shildi.",
        "xato": "❌ Xato: {}",
        "vaqt_tugadi": "⌛ Vaqt tugadi. Qayta urinib ko'ring!",
        "rasm_yuboring": "📸 Rasm yuboring:",
        "chek_emas": "⚠️ Bu rasm chek emas!\nChek yuborish uchun /chek buyrug'ini bosing.",
        "broadcast_tasdiq": "📢 Quyidagi xabarni {} ta foydalanuvchiga yubormoqchisiz:\n\n{}\n\nTasdiqlaysizmi?",
        "broadcast_ha": "✅ Ha, yuborish",
        "broadcast_yoq": "❌ Bekor qilish",
        "broadcast_yuborildi": "📢 Yuborildi!\n✅ Muvaffaqiyatli: {}\n❌ Xato: {}",
        "broadcast_bekor": "❌ Broadcast bekor qilindi.",
    },
    "ru": {
        "til_nomi": "🇷🇺 Русский",
        "bosh_menu": "👋 Добро пожаловать!\n\nВыберите из меню:",
        "til_tanlang": "🌐 Выберите язык:",
        "sifat_tanlang": "🎚 Выберите качество:",
        "rasm_yukor": "⏬ Фото принимается...",
        "qoldi": "📊 Осталось сегодня: {} шт",
        "jarayon": "⏳ Улучшение...\nПодождите...",
        "tayyor": "✨ Готово! Качество: {}\n🤖 Улучшено через {}\n📊 Осталось: {} шт",
        "limit_bepul": "⛔ Лимит исчерпан! ({} шт/день)\n\n⭐ Получите Premium — 30 шт/день + 4K!",
        "limit_premium": "⛔ Дневной лимит исчерпан!\n⏰ Обновится завтра.",
        "premium_bor": "✅ Вы Premium пользователь!\n📅 До: {}",
        "premium_info": "⭐ Premium — {:,} сум/мес\n\n✅ 30 фото в день\n✅ Качество 4K\n✅ Приоритет",
        "tolov_info": "💳 Данные для оплаты:\n\n💰 Сумма: {:,} сум\n🏦 Карта: <code>{}</code>\n👤 Владелец: {}\n\n📌 После оплаты:\n1️⃣ Отправьте чек через команду /chek\n⚠️ Используйте команду /chek для отправки!\n\n❗ В комментарии ID: <code>{}</code>",
        "chek_yuborish": "📸 Нажмите /chek и отправьте скриншот чека:",
        "chek_qabul": "✅ Чек принят!\n⏳ Админ проверит и ответит.",
        "chek_kutilmoqda": "⏳ Ваш предыдущий чек уже на проверке!",
        "holat": "📊 Аккаунт:\n\n👤 Имя: {}\n🆔 ID: {}\n⭐ Подписка: {}\n📅 До: {}\n📸 Сегодня: {}\n🔢 Осталось: {}\n🖼 Всего: {}\n👥 Рефералы: {} → {} бонус",
        "premium_label": "Premium ✅",
        "oddiy_label": "Бесплатно",
        "blok": "🚫 Вы заблокированы.",
        "premium_kerak": "🔒 Только для Premium!\n\n⭐ Premium: {:,} сум/мес",
        "referral_matn": "👥 Реферал:\n\n🔗 Ссылка:\n{}\n\n✅ Каждый приглашённый = +1 фото!\n📊 Приглашено: {}\n🎁 Бонус: {}\n💰 Остаток: {}",
        "bonus_xabar": "🎁 +1 бонусное фото! Ваш друг присоединился.",
        "xato": "❌ Ошибка: {}",
        "vaqt_tugadi": "⌛ Время вышло. Попробуйте снова!",
        "rasm_yuboring": "📸 Отправьте фото:",
        "chek_emas": "⚠️ Это не чек!\nДля отправки чека используйте /chek.",
        "broadcast_tasdiq": "📢 Отправить сообщение {} пользователям:\n\n{}\n\nПодтверждаете?",
        "broadcast_ha": "✅ Да, отправить",
        "broadcast_yoq": "❌ Отмена",
        "broadcast_yuborildi": "📢 Отправлено!\n✅ Успешно: {}\n❌ Ошибок: {}",
        "broadcast_bekor": "❌ Broadcast отменён.",
    },
    "en": {
        "til_nomi": "🇬🇧 English",
        "bosh_menu": "👋 Welcome!\n\nChoose from the menu:",
        "til_tanlang": "🌐 Select language:",
        "sifat_tanlang": "🎚 Select quality:",
        "rasm_yukor": "⏬ Receiving photo...",
        "qoldi": "📊 Remaining today: {}",
        "jarayon": "⏳ Enhancing...\nPlease wait...",
        "tayyor": "✨ Done! Quality: {}\n🤖 Enhanced via {}\n📊 Remaining: {}",
        "limit_bepul": "⛔ Daily limit reached! ({}/day)\n\n⭐ Get Premium — 30/day + 4K!",
        "limit_premium": "⛔ Daily limit reached!\n⏰ Resets tomorrow.",
        "premium_bor": "✅ You are Premium!\n📅 Expires: {}",
        "premium_info": "⭐ Premium — {:,} UZS/month\n\n✅ 30 photos/day\n✅ 4K quality\n✅ Priority",
        "tolov_info": "💳 Payment details:\n\n💰 Amount: {:,} UZS\n🏦 Card: <code>{}</code>\n👤 Owner: {}\n\n📌 After payment:\n1️⃣ Send receipt via /chek command\n⚠️ Use /chek command to send!\n\n❗ Include ID in notes: <code>{}</code>",
        "chek_yuborish": "📸 Press /chek and send receipt screenshot:",
        "chek_qabul": "✅ Receipt accepted!\n⏳ Admin will verify soon.",
        "chek_kutilmoqda": "⏳ Your previous receipt is being reviewed!",
        "holat": "📊 Account:\n\n👤 Name: {}\n🆔 ID: {}\n⭐ Plan: {}\n📅 Expires: {}\n📸 Today: {}\n🔢 Remaining: {}\n🖼 Total: {}\n👥 Referrals: {} → {} bonus",
        "premium_label": "Premium ✅",
        "oddiy_label": "Free",
        "blok": "🚫 You are banned.",
        "premium_kerak": "🔒 Premium only!\n\n⭐ Premium: {:,} UZS/month",
        "referral_matn": "👥 Referral:\n\n🔗 Your link:\n{}\n\n✅ Each invite = +1 free photo!\n📊 Invited: {}\n🎁 Bonus: {}\n💰 Balance: {}",
        "bonus_xabar": "🎁 +1 bonus photo! Your friend joined.",
        "xato": "❌ Error: {}",
        "vaqt_tugadi": "⌛ Timed out. Try again!",
        "rasm_yuboring": "📸 Send a photo:",
        "chek_emas": "⚠️ This is not a receipt!\nUse /chek command to send receipt.",
        "broadcast_tasdiq": "📢 Send message to {} users:\n\n{}\n\nConfirm?",
        "broadcast_ha": "✅ Yes, send",
        "broadcast_yoq": "❌ Cancel",
        "broadcast_yuborildi": "📢 Done!\n✅ Success: {}\n❌ Failed: {}",
        "broadcast_bekor": "❌ Broadcast cancelled.",
    },
    "kz": {
        "til_nomi": "🇰🇿 Қазақ",
        "bosh_menu": "👋 Қош келдіңіз!\n\nМәзірден таңдаңыз:",
        "til_tanlang": "🌐 Тілді таңдаңыз:",
        "sifat_tanlang": "🎚 Сапаны таңдаңыз:",
        "rasm_yukor": "⏬ Сурет қабылдануда...",
        "qoldi": "📊 Бүгін қалды: {} дана",
        "jarayon": "⏳ Жақсартылуда...\nКүтіңіз...",
        "tayyor": "✨ Дайын! Сапа: {}\n🤖 {} арқылы жақсартылды\n📊 Қалды: {} дана",
        "limit_bepul": "⛔ Лимит бітті! ({} дана/күн)\n\n⭐ Premium алыңыз — 30 дана/күн + 4K!",
        "limit_premium": "⛔ Күндік лимит бітті!\n⏰ Ертең жаңарады.",
        "premium_bor": "✅ Сіз Premium пайдаланушысысыз!\n📅 Мерзімі: {}",
        "premium_info": "⭐ Premium — {:,} сум/ай\n\n✅ Күніне 30 сурет\n✅ 4K сапа\n✅ Басымдық",
        "tolov_info": "💳 Төлем деректері:\n\n💰 Сома: {:,} сум\n🏦 Карта: <code>{}</code>\n👤 Иесі: {}\n\n📌 Төлемнен кейін:\n1️⃣ /chek арқылы чек жіберіңіз\n⚠️ /chek пәрменін қолданыңыз!\n\n❗ Түсініктемеге ID: <code>{}</code>",
        "chek_yuborish": "📸 /chek басып чек суретін жіберіңіз:",
        "chek_qabul": "✅ Чек қабылданды!\n⏳ Әкімші тексереді.",
        "chek_kutilmoqda": "⏳ Алдыңғы чегіңіз қаралуда!",
        "holat": "📊 Аккаунт:\n\n👤 Аты: {}\n🆔 ID: {}\n⭐ Жазылым: {}\n📅 Мерзімі: {}\n📸 Бүгін: {} дана\n🔢 Қалды: {} дана\n🖼 Барлығы: {} дана\n👥 Рефералдар: {} → {} бонус",
        "premium_label": "Premium ✅",
        "oddiy_label": "Тегін",
        "blok": "🚫 Сіз бұғатталғансыз.",
        "premium_kerak": "🔒 Тек Premium үшін!\n\n⭐ Premium: {:,} сум/ай",
        "referral_matn": "👥 Реферал:\n\n🔗 Сілтеме:\n{}\n\n✅ Әр шақырылған = +1 тегін сурет!\n📊 Шақырылды: {}\n🎁 Бонус: {}\n💰 Қалдық: {}",
        "bonus_xabar": "🎁 +1 бонус сурет! Досыңыз қосылды.",
        "xato": "❌ Қате: {}",
        "vaqt_tugadi": "⌛ Уақыт бітті. Қайта көріңіз!",
        "rasm_yuboring": "📸 Сурет жіберіңіз:",
        "chek_emas": "⚠️ Бұл чек емес!\nЧек жіберу үшін /chek пәрменін қолданыңыз.",
        "broadcast_tasdiq": "📢 {} пайдаланушыға хабар жіберу:\n\n{}\n\nРастайсыз ба?",
        "broadcast_ha": "✅ Иә, жіберу",
        "broadcast_yoq": "❌ Болдырмау",
        "broadcast_yuborildi": "📢 Жіберілді!\n✅ Сәтті: {}\n❌ Қате: {}",
        "broadcast_bekor": "❌ Broadcast болдырылмады.",
    },
}

SIFATLAR = {
    "144p":  {"scale": 2, "label": "🔹 144p  — tez",         "premium": False},
    "720p":  {"scale": 2, "label": "🔷 720p  — yaxshi",      "premium": False},
    "1080p": {"scale": 4, "label": "🔶 1080p — yuqori",      "premium": False},
    "4K":    {"scale": 4, "label": "💎 4K    — maksimal ⭐", "premium": True},
}

# ═══════════════════════════════════════════
#   DATABASE
# ═══════════════════════════════════════════
DB_FAYL = "database.json"

def db_yukla():
    if os.path.exists(DB_FAYL):
        with open(DB_FAYL, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "pending_payments": {}, "blocked": [], "chek_mode": []}

def db_sayla(data):
    with open(DB_FAYL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def user_get(user_id: int) -> dict:
    db  = db_yukla()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": user_id, "ism": "", "username": "",
            "til": "uz", "til_tanlangan": False,
            "premium": False, "premium_tugash": None,
            "bugun_soni": 0, "sana": str(date.today()),
            "jami_rasm": 0, "bonus_rasm": 0,
            "referral_soni": 0, "referral_jami_bonus": 0,
            "ref_by": None,
            "qoshilgan": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        db_sayla(db)
    u = db["users"][uid]
    if u.get("sana") != str(date.today()):
        u["bugun_soni"] = 0
        u["sana"] = str(date.today())
        db["users"][uid] = u
        db_sayla(db)
    return db["users"][uid]

def user_yangi(user_id: int, **kwargs):
    db  = db_yukla()
    uid = str(user_id)
    user_get(user_id)
    db["users"][uid].update(kwargs)
    db_sayla(db)

def t(user_id: int, kalit: str) -> str:
    u   = user_get(user_id)
    til = u.get("til", "uz")
    return TILLAR.get(til, TILLAR["uz"]).get(kalit, kalit)

def premium_tekshir(user_id: int) -> bool:
    u = user_get(user_id)
    if not u.get("premium"):
        return False
    tugash = u.get("premium_tugash")
    if tugash and datetime.strptime(tugash, "%Y-%m-%d") < datetime.now():
        user_yangi(user_id, premium=False, premium_tugash=None)
        return False
    return True

def limit_tekshir(user_id: int) -> tuple:
    u     = user_get(user_id)
    limit = PREMIUM_LIMIT if premium_tekshir(user_id) else BEPUL_LIMIT
    bonus = u.get("bonus_rasm", 0)
    qoldi = (limit + bonus) - u.get("bugun_soni", 0)
    return qoldi > 0, max(0, qoldi)

def bloklangan_mi(user_id: int) -> bool:
    return user_id in db_yukla().get("blocked", [])

def chek_mode_mi(user_id: int) -> bool:
    return user_id in db_yukla().get("chek_mode", [])

def chek_mode_qosh(user_id: int):
    db = db_yukla()
    if user_id not in db.setdefault("chek_mode", []):
        db["chek_mode"].append(user_id)
        db_sayla(db)

def chek_mode_ochir(user_id: int):
    db = db_yukla()
    if user_id in db.get("chek_mode", []):
        db["chek_mode"].remove(user_id)
        db_sayla(db)

async def admin_xabar(ctx, matn: str, photo_id=None):
    try:
        if photo_id:
            await ctx.bot.send_photo(chat_id=ADMIN_ID, photo=photo_id, caption=matn)
        else:
            await ctx.bot.send_message(chat_id=ADMIN_ID, text=matn)
    except Exception as e:
        log.error(f"Admin xabar xato: {e}")

def foydalanuvchi_sayla(update: Update):
    u = update.effective_user
    user_yangi(u.id, ism=u.full_name,
               username=f"@{u.username}" if u.username else "—")

# ═══════════════════════════════════════════
#   MENYULAR
# ═══════════════════════════════════════════
def bosh_menu_tugmalari(user_id: int) -> InlineKeyboardMarkup:
    is_prem = premium_tekshir(user_id)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Rasm tiniqlashtirish", callback_data="menu_rasm")],
        [InlineKeyboardButton("⭐ Premium olish" if not is_prem else "⭐ Premium hisobim", callback_data="menu_premium")],
        [InlineKeyboardButton("👥 Referral", callback_data="menu_referral"),
         InlineKeyboardButton("📊 Holat", callback_data="menu_holat")],
        [InlineKeyboardButton("🌐 Til", callback_data="menu_til")],
    ])

def sifat_tugmalari(user_id: int) -> InlineKeyboardMarkup:
    is_prem = premium_tekshir(user_id)
    rows = []
    for k, v in SIFATLAR.items():
        if v["premium"] and not is_prem:
            rows.append([InlineKeyboardButton(f"🔒 {v['label']} (Premium)", callback_data=f"premium_kerak_{k}")])
        else:
            rows.append([InlineKeyboardButton(v["label"], callback_data=f"sifat_{k}")])
    rows.append([InlineKeyboardButton("◀️ Orqaga", callback_data="menu_back")])
    return InlineKeyboardMarkup(rows)

def orqaga_tugma() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data="menu_back")]])

# ═══════════════════════════════════════════
#   /start
# ═══════════════════════════════════════════
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id

    if bloklangan_mi(user_id):
        await update.message.reply_text(t(user_id, "blok"))
        return

    # Referral
    args = ctx.args
    if args and args[0].startswith("ref_"):
        try:
            ref_id = int(args[0].replace("ref_", ""))
            u = user_get(user_id)
            if ref_id != user_id and not u.get("ref_by"):
                ref_u = user_get(ref_id)
                user_yangi(ref_id,
                    referral_soni=ref_u.get("referral_soni", 0) + 1,
                    referral_jami_bonus=ref_u.get("referral_jami_bonus", 0) + 1,
                    bonus_rasm=ref_u.get("bonus_rasm", 0) + 1
                )
                user_yangi(user_id, ref_by=ref_id)
                try:
                    await ctx.bot.send_message(chat_id=ref_id, text=t(ref_id, "bonus_xabar"))
                except:
                    pass
        except:
            pass

    u = user_get(user_id)
    if not u.get("til_tanlangan"):
        tugmalar = [[InlineKeyboardButton(v["til_nomi"], callback_data=f"til_{k}")]
                    for k, v in TILLAR.items()]
        await update.message.reply_text(
            "🌐 Choose language / Tilni tanlang / Выберите язык / Тілді таңдаңыз:",
            reply_markup=InlineKeyboardMarkup(tugmalar)
        )
        return

    await update.message.reply_text(
        t(user_id, "bosh_menu"),
        reply_markup=bosh_menu_tugmalari(user_id)
    )

# ═══════════════════════════════════════════
#   /chek — chek yuborish rejimi
# ═══════════════════════════════════════════
async def chek_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id
    if bloklangan_mi(user_id):
        return
    db  = db_yukla()
    uid = str(user_id)
    if uid in db.get("pending_payments", {}):
        await update.message.reply_text(t(user_id, "chek_kutilmoqda"))
        return
    chek_mode_qosh(user_id)
    await update.message.reply_text(t(user_id, "chek_yuborish"))

# ═══════════════════════════════════════════
#   RASM KELDI
# ═══════════════════════════════════════════
async def rasm_keldi(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    foydalanuvchi_sayla(update)
    user_id = update.effective_user.id

    if bloklangan_mi(user_id):
        await update.message.reply_text(t(user_id, "blok"))
        return

    u = user_get(user_id)
    if not u.get("til_tanlangan"):
        await start(update, ctx)
        return

    # Chek rejimida bo'lsa — chek sifatida qabul qil
    if chek_mode_mi(user_id):
        await chek_rasm_qabul(update, ctx)
        return

    # Oddiy rasm tiniqlashtirish
    o_tdi, qoldi = limit_tekshir(user_id)
    if not o_tdi:
        is_prem = premium_tekshir(user_id)
        tugmalar = [[InlineKeyboardButton("⭐ Premium olish", callback_data="menu_premium")]]
        if is_prem:
            await update.message.reply_text(t(user_id, "limit_premium"))
        else:
            await update.message.reply_text(
                t(user_id, "limit_bepul").format(BEPUL_LIMIT),
                reply_markup=InlineKeyboardMarkup(tugmalar)
            )
        return

    msg   = await update.message.reply_text(t(user_id, "rasm_yukor"))
    photo = update.message.photo[-1]
    file  = await ctx.bot.get_file(photo.file_id)
    buf   = io.BytesIO()
    await file.download_to_memory(buf)

    # Vaqtinchalik saqlash
    db  = db_yukla()
    db.setdefault("kutish", {})[str(user_id)] = {
        "bytes": buf.getvalue().hex(),
        "vaqt": time.time()
    }
    db_sayla(db)

    await msg.delete()
    await update.message.reply_text(
        t(user_id, "sifat_tanlang") + f"\n{t(user_id, 'qoldi').format(qoldi)}",
        reply_markup=sifat_tugmalari(user_id)
    )

# ═══════════════════════════════════════════
#   CHEK RASM QABUL
# ═══════════════════════════════════════════
async def chek_rasm_qabul(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    u       = user_get(user_id)
    photo   = update.message.photo[-1] if update.message.photo else None
    doc     = update.message.document if update.message.document else None

    if not photo and not doc:
        await update.message.reply_text(t(user_id, "chek_emas"))
        return

    fid = photo.file_id if photo else doc.file_id

    db  = db_yukla()
    uid = str(user_id)
    db["pending_payments"][uid] = {
        "user_id": user_id,
        "ism": u.get("ism", "—"),
        "username": u.get("username", "—"),
        "vaqt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "file_id": fid
    }
    db_sayla(db)
    chek_mode_ochir(user_id)

    await update.message.reply_text(t(user_id, "chek_qabul"))

    await admin_xabar(
        ctx,
        f"💳 YANGI TO'LOV!\n\n"
        f"👤 {u.get('ism','—')} | {u.get('username','—')}\n"
        f"🆔 {user_id}\n"
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"✅ Tasdiqlash: /premium_ber_{user_id}\n"
        f"❌ Rad etish: /premium_rad_{user_id}",
        photo_id=fid
    )

# ═══════════════════════════════════════════
#   CALLBACK HANDLER
# ═══════════════════════════════════════════
async def callback_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    amal    = query.data

    if bloklangan_mi(user_id):
        await query.edit_message_text(t(user_id, "blok"))
        return

    # ── Til tanlash ──
    if amal.startswith("til_"):
        til = amal.replace("til_", "")
        user_yangi(user_id, til=til, til_tanlangan=True)
        await query.edit_message_text(
            t(user_id, "bosh_menu"),
            reply_markup=bosh_menu_tugmalari(user_id)
        )
        return

    # ── Bosh menyu ──
    if amal == "menu_back":
        await query.edit_message_text(
            t(user_id, "bosh_menu"),
            reply_markup=bosh_menu_tugmalari(user_id)
        )
        return

    if amal == "menu_rasm":
        await query.edit_message_text(
            t(user_id, "rasm_yuboring"),
            reply_markup=orqaga_tugma()
        )
        return

    if amal == "menu_til":
        tugmalar = [[InlineKeyboardButton(v["til_nomi"], callback_data=f"til_{k}")]
                    for k, v in TILLAR.items()]
        tugmalar.append([InlineKeyboardButton("◀️ Orqaga", callback_data="menu_back")])
        await query.edit_message_text(
            t(user_id, "til_tanlang"),
            reply_markup=InlineKeyboardMarkup(tugmalar)
        )
        return

    if amal == "menu_holat":
        u        = user_get(user_id)
        is_prem  = premium_tekshir(user_id)
        _, qoldi = limit_tekshir(user_id)
        await query.edit_message_text(
            t(user_id, "holat").format(
                u.get("ism","—"), user_id,
                t(user_id, "premium_label") if is_prem else t(user_id, "oddiy_label"),
                u.get("premium_tugash","—"),
                u.get("bugun_soni",0), qoldi,
                u.get("jami_rasm",0),
                u.get("referral_soni",0), u.get("referral_jami_bonus",0)
            ),
            reply_markup=orqaga_tugma()
        )
        return

    if amal == "menu_referral":
        bot_info = await ctx.bot.get_me()
        havola   = f"https://t.me/{bot_info.username}?start=ref_{user_id}"
        u        = user_get(user_id)
        await query.edit_message_text(
            t(user_id, "referral_matn").format(
                havola,
                u.get("referral_soni",0),
                u.get("referral_jami_bonus",0),
                u.get("bonus_rasm",0)
            ),
            reply_markup=orqaga_tugma()
        )
        return

    if amal == "menu_premium":
        is_prem = premium_tekshir(user_id)
        if is_prem:
            u = user_get(user_id)
            await query.edit_message_text(
                t(user_id, "premium_bor").format(u.get("premium_tugash","—")),
                reply_markup=orqaga_tugma()
            )
        else:
            await query.edit_message_text(
                t(user_id, "premium_info").format(PREMIUM_NARX),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 To'lov qilish", callback_data="tolov_boshlash")],
                    [InlineKeyboardButton("◀️ Orqaga", callback_data="menu_back")]
                ])
            )
        return

    if amal == "tolov_boshlash":
        await query.edit_message_text(
            t(user_id, "tolov_info").format(PREMIUM_NARX, KARTA_RAQAM, KARTA_EGASI, user_id),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📸 Chek yuborish → /chek", callback_data="chek_yuborish_btn")],
                [InlineKeyboardButton("◀️ Orqaga", callback_data="menu_premium")]
            ])
        )
        return

    if amal == "chek_yuborish_btn":
        db  = db_yukla()
        uid = str(user_id)
        if uid in db.get("pending_payments", {}):
            await query.edit_message_text(
                t(user_id, "chek_kutilmoqda"),
                reply_markup=orqaga_tugma()
            )
            return
        chek_mode_qosh(user_id)
        await query.edit_message_text(
            t(user_id, "chek_yuborish"),
            reply_markup=orqaga_tugma()
        )
        return

    # ── Premium kerak ──
    if amal.startswith("premium_kerak_"):
        await query.edit_message_text(
            t(user_id, "premium_kerak").format(PREMIUM_NARX),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⭐ Premium olish", callback_data="menu_premium")],
                [InlineKeyboardButton("◀️ Orqaga", callback_data="menu_back")]
            ])
        )
        return

    # ── Broadcast tasdiqlash ──
    if amal == "broadcast_ha":
        if query.from_user.id != ADMIN_ID:
            return
        matn_yuborish = ctx.bot_data.pop("broadcast_matn", None)
        if not matn_yuborish:
            await query.edit_message_text("❌ Xabar topilmadi.")
            return
        db    = db_yukla()
        users = db.get("users", {})
        ok = xato = 0
        await query.edit_message_text("⏳ Yuborilmoqda...")
        for uid in users:
            try:
                await ctx.bot.send_message(chat_id=int(uid), text=matn_yuborish)
                ok += 1
                await asyncio.sleep(0.05)  # ← TUZATILDI: asyncio.sleep
            except:
                xato += 1
        await query.edit_message_text(
            t(ADMIN_ID, "broadcast_yuborildi").format(ok, xato)
        )
        return

    if amal == "broadcast_yoq":
        if query.from_user.id != ADMIN_ID:
            return
        ctx.bot_data.pop("broadcast_matn", None)
        await query.edit_message_text(t(ADMIN_ID, "broadcast_bekor"))
        return

    # ── Admin callback ──
    if amal.startswith("admin_"):
        await admin_callback_handler(query, ctx)
        return

    # ── Sifat tanlash ──
    if amal.startswith("sifat_"):
        sifat = amal.replace("sifat_", "")
        await sifat_ishlash(query, ctx, user_id, sifat)
        return

# ═══════════════════════════════════════════
#   SIFAT ISHLASH
# ═══════════════════════════════════════════
async def sifat_ishlash(query, ctx, user_id: int, sifat: str):
    db  = db_yukla()
    uid = str(user_id)

    if uid not in db.get("kutish", {}):
        await query.edit_message_text(
            t(user_id, "rasm_yuboring"),
            reply_markup=bosh_menu_tugmalari(user_id)
        )
        return

    o_tdi, _ = limit_tekshir(user_id)
    if not o_tdi:
        await query.edit_message_text(t(user_id, "limit_premium"))
        return

    if SIFATLAR[sifat]["premium"] and not premium_tekshir(user_id):
        await query.edit_message_text(
            t(user_id, "premium_kerak").format(PREMIUM_NARX),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⭐ Premium olish", callback_data="menu_premium")]
            ])
        )
        return

    rasm_bytes = bytes.fromhex(db["kutish"][uid]["bytes"])
    del db["kutish"][uid]
    db_sayla(db)

    scale = min(SIFATLAR[sifat]["scale"], 4)
    await query.edit_message_text(t(user_id, "jarayon"))

    try:
        # ── TUZATILDI: requests ni thread pool'da ishlatish ──
        loop = asyncio.get_event_loop()

        def picwish_yuborish():
            resp = requests.post(
                PICWISH_CREATE_URL,
                headers={"X-API-KEY": PICWISH_KEY},
                files={"image_file": ("rasm.jpg", rasm_bytes, "image/jpeg")},
                data={"sync": 0, "scale": scale},
                timeout=60
            )
            resp.raise_for_status()
            return resp.json()

        javob = await loop.run_in_executor(None, picwish_yuborish)

        if javob.get("status") != 200:
            await query.edit_message_text(
                t(user_id, "xato").format(javob.get("message", str(javob)))
            )
            return

        task_id = javob["data"]["task_id"]

        for _ in range(30):
            await asyncio.sleep(2)  # ← TUZATILDI: asyncio.sleep

            def picwish_tekshir():
                r = requests.get(
                    PICWISH_RESULT_URL.format(task_id=task_id),
                    headers={"X-API-KEY": PICWISH_KEY},
                    timeout=30
                )
                r.raise_for_status()
                return r.json()

            holat = await loop.run_in_executor(None, picwish_tekshir)

            if holat.get("status") != 200:
                continue

            state = holat["data"].get("state", 0)

            if state == 1:
                natija_url = holat["data"].get("image")

                def rasm_yukla():
                    return requests.get(natija_url, timeout=60)

                r = await loop.run_in_executor(None, rasm_yukla)

                u     = user_get(user_id)
                bonus = u.get("bonus_rasm", 0)
                limit = PREMIUM_LIMIT if premium_tekshir(user_id) else BEPUL_LIMIT
                ishlatilgan = u.get("bugun_soni", 0)
                if ishlatilgan >= limit and bonus > 0:
                    user_yangi(user_id, bonus_rasm=bonus - 1)
                user_yangi(user_id,
                    bugun_soni=ishlatilgan + 1,
                    jami_rasm=u.get("jami_rasm", 0) + 1
                )
                _, qoldi = limit_tekshir(user_id)
                await ctx.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=io.BytesIO(r.content),
                    caption=t(user_id, "tayyor").format(sifat, BOT_USERNAME, qoldi)
                )
                await query.edit_message_text(
                    t(user_id, "bosh_menu"),
                    reply_markup=bosh_menu_tugmalari(user_id)
                )
                return
            elif state < 0:
                await query.edit_message_text(t(user_id, "xato").format("ishlov xato"))
                return

        await query.edit_message_text(t(user_id, "vaqt_tugadi"))

    except requests.HTTPError as e:
        await query.edit_message_text(t(user_id, "xato").format(e.response.status_code))
    except Exception as e:
        log.error(f"Xato: {e}")
        await query.edit_message_text(t(user_id, "xato").format(str(e)))

# ═══════════════════════════════════════════
#   ADMIN PANEL
# ═══════════════════════════════════════════
async def admin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.strip()
    if matn != f"/{ADMIN_PAROL}" or update.effective_user.id != ADMIN_ID:
        return
    await admin_panel_yuborish(update.message)

async def admin_panel_yuborish(message):
    db    = db_yukla()
    users = db.get("users", {})
    await message.reply_text(
        f"🔐 ADMIN PANEL\n\n"
        f"👥 Jami: {len(users)}\n"
        f"⭐ Premium: {sum(1 for u in users.values() if u.get('premium'))}\n"
        f"🚫 Bloklangan: {len(db.get('blocked', []))}\n"
        f"💳 Kutayotgan: {len(db.get('pending_payments', {}))}\n"
        f"📸 Bugun: {sum(u.get('bugun_soni',0) for u in users.values())}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")],
            [InlineKeyboardButton("⭐ Premium lar",       callback_data="admin_premiums")],
            [InlineKeyboardButton("💳 Kutayotgan to'lovlar", callback_data="admin_pending")],
            [InlineKeyboardButton("🚫 Bloklangan lar",    callback_data="admin_blocked")],
            [InlineKeyboardButton("📢 Hammaga xabar",     callback_data="admin_broadcast")],
            [InlineKeyboardButton("📊 Statistika",        callback_data="admin_stat")],
        ])
    )

async def admin_callback_handler(query, ctx):
    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ Ruxsat yo'q!")
        return
    db   = db_yukla()
    amal = query.data
    orqa = InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Orqaga", callback_data="admin_back")]])

    if amal == "admin_back":
        users = db.get("users", {})
        await query.edit_message_text(
            f"🔐 ADMIN PANEL\n\n"
            f"👥 Jami: {len(users)}\n"
            f"⭐ Premium: {sum(1 for u in users.values() if u.get('premium'))}\n"
            f"🚫 Bloklangan: {len(db.get('blocked', []))}\n"
            f"💳 Kutayotgan: {len(db.get('pending_payments', {}))}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="admin_users")],
                [InlineKeyboardButton("⭐ Premium lar",       callback_data="admin_premiums")],
                [InlineKeyboardButton("💳 Kutayotgan to'lovlar", callback_data="admin_pending")],
                [InlineKeyboardButton("🚫 Bloklangan lar",    callback_data="admin_blocked")],
                [InlineKeyboardButton("📢 Hammaga xabar",     callback_data="admin_broadcast")],
                [InlineKeyboardButton("📊 Statistika",        callback_data="admin_stat")],
            ])
        )
    elif amal == "admin_stat":
        users = db.get("users", {})
        await query.edit_message_text(
            f"📊 STATISTIKA:\n\n"
            f"👥 Jami: {len(users)}\n"
            f"⭐ Premium: {sum(1 for u in users.values() if u.get('premium'))}\n"
            f"🖼 Jami rasm: {sum(u.get('jami_rasm',0) for u in users.values())}\n"
            f"📸 Bugun: {sum(u.get('bugun_soni',0) for u in users.values())}\n"
            f"👥 Jami referral: {sum(u.get('referral_soni',0) for u in users.values())}",
            reply_markup=orqa
        )
    elif amal == "admin_users":
        users = db.get("users", {})
        matn  = f"👥 FOYDALANUVCHILAR ({len(users)} ta):\n\n"
        for u in list(users.values())[-20:]:
            e = "⭐" if u.get("premium") else "👤"
            matn += f"{e} {u.get('ism','—')} | {u.get('username','—')} | {u['id']}\n"
        await query.edit_message_text(matn[:4000], reply_markup=orqa)
    elif amal == "admin_premiums":
        prems = [u for u in db.get("users", {}).values() if u.get("premium")]
        matn  = f"⭐ PREMIUM ({len(prems)} ta):\n\n"
        for u in prems:
            matn += f"• {u.get('ism','—')} | {u['id']} | {u.get('premium_tugash','—')}\n"
        if not prems:
            matn += "Yo'q."
        await query.edit_message_text(matn[:4000], reply_markup=orqa)
    elif amal == "admin_pending":
        pending = db.get("pending_payments", {})
        if not pending:
            await query.edit_message_text("💳 Kutayotgan to'lov yo'q.", reply_markup=orqa)
            return
        matn = f"💳 KUTAYOTGAN ({len(pending)} ta):\n\n"
        for p in pending.values():
            matn += (
                f"👤 {p.get('ism','—')} | {p.get('username','—')}\n"
                f"🆔 {p['user_id']} | {p.get('vaqt','—')}\n"
                f"✅ /premium_ber_{p['user_id']}\n"
                f"❌ /premium_rad_{p['user_id']}\n\n"
            )
        await query.edit_message_text(matn[:4000], reply_markup=orqa)
    elif amal == "admin_blocked":
        blocked = db.get("blocked", [])
        matn    = f"🚫 BLOKLANGAN ({len(blocked)} ta):\n\n"
        for bid in blocked:
            u = db["users"].get(str(bid), {})
            matn += f"• {u.get('ism','—')} | {bid} | /blok_ochish_{bid}\n"
        if not blocked:
            matn += "Yo'q."
        await query.edit_message_text(matn[:4000], reply_markup=orqa)
    elif amal == "admin_broadcast":
        # ← TUZATILDI: broadcast_mode o'rniga to'g'ri flag
        ctx.bot_data["waiting_broadcast"] = True
        await query.edit_message_text(
            "📢 Xabarni yozing:\n(Bekor qilish uchun /admin2024 yozing)"
        )

# ═══════════════════════════════════════════
#   ADMIN MATN BUYRUQLARI
# ═══════════════════════════════════════════
async def admin_matn(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    matn = update.message.text.strip()
    db   = db_yukla()

    # ← TUZATILDI: broadcast confirmation qo'shildi
    if ctx.bot_data.get("waiting_broadcast"):
        ctx.bot_data.pop("waiting_broadcast")
        ctx.bot_data["broadcast_matn"] = matn
        users = db.get("users", {})
        await update.message.reply_text(
            t(ADMIN_ID, "broadcast_tasdiq").format(len(users), matn[:200]),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(t(ADMIN_ID, "broadcast_ha"), callback_data="broadcast_ha"),
                    InlineKeyboardButton(t(ADMIN_ID, "broadcast_yoq"), callback_data="broadcast_yoq"),
                ]
            ])
        )
        return

    if matn.startswith("/premium_ber_"):
        try: uid = int(matn.split("_")[-1])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        tugash = (datetime.now() + timedelta(days=PREMIUM_KUN)).strftime("%Y-%m-%d")
        user_yangi(uid, premium=True, premium_tugash=tugash)
        db = db_yukla()
        db["pending_payments"].pop(str(uid), None)
        db_sayla(db)
        await update.message.reply_text(f"✅ {uid} ga Premium berildi! ({tugash} gacha)")
        try:
            await ctx.bot.send_message(chat_id=uid,
                text=f"🎉 Premium berildi!\n📅 {PREMIUM_KUN} kun ({tugash} gacha)\n💎 4K va 30 ta/kun!")
        except: pass

    elif matn.startswith("/premium_rad_"):
        try: uid = int(matn.split("_")[-1])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        db["pending_payments"].pop(str(uid), None)
        db_sayla(db)
        await update.message.reply_text(f"❌ {uid} rad etildi.")
        try:
            await ctx.bot.send_message(chat_id=uid,
                text="❌ To'lovingiz tasdiqlanmadi. Admin bilan bog'laning.")
        except: pass

    elif matn.startswith("/blok_ochish_"):
        try: uid = int(matn.split("_")[-1])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        blocked = db.get("blocked", [])
        if uid in blocked:
            blocked.remove(uid)
            db["blocked"] = blocked
            db_sayla(db)
        await update.message.reply_text(f"✅ {uid} blokdan chiqarildi!")

    elif matn.startswith("/blok_"):
        try: uid = int(matn.replace("/blok_", "").split()[0])
        except:
            await update.message.reply_text("❌ ID noto'g'ri")
            return
        db.setdefault("blocked", [])
        if uid not in db["blocked"]:
            db["blocked"].append(uid)
            db_sayla(db)
        await update.message.reply_text(f"🚫 {uid} bloklandi!")

    elif matn.startswith("/bonus_"):
        parts = matn.replace("/bonus_", "").split("_")
        try: uid, soni = int(parts[0]), int(parts[1])
        except:
            await update.message.reply_text("Format: /bonus_ID_SONI")
            return
        u = user_get(uid)
        user_yangi(uid, bonus_rasm=u.get("bonus_rasm", 0) + soni)
        await update.message.reply_text(f"✅ {uid} ga {soni} bonus rasm berildi!")

# ═══════════════════════════════════════════
#   ADMIN RASM (chek ko'rish uchun)
# ═══════════════════════════════════════════
async def admin_rasm(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Admin ham rasm yuborishi mumkin (masalan, test uchun)"""
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("✅ Rasm qabul qilindi (admin).")

# ═══════════════════════════════════════════
#   ISHGA TUSHIRISH
# ═══════════════════════════════════════════
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",      start))
    app.add_handler(CommandHandler("chek",       chek_cmd))
    app.add_handler(CommandHandler(ADMIN_PAROL,  admin_cmd))

    app.add_handler(CallbackQueryHandler(callback_handler))

    # ← TUZATILDI: filters.User(user_id=...) to'g'ri sintaksis
    app.add_handler(MessageHandler(
        filters.PHOTO & ~filters.User(user_id=ADMIN_ID),
        rasm_keldi
    ))
    app.add_handler(MessageHandler(
        filters.PHOTO & filters.User(user_id=ADMIN_ID),
        admin_rasm
    ))
    app.add_handler(MessageHandler(
        filters.TEXT & filters.User(user_id=ADMIN_ID),
        admin_matn
    ))

    print(f"✅ Bot ishga tushdi!")
    print(f"   Admin panel: /{ADMIN_PAROL}")
    print("   To'xtatish: Ctrl+C")
    app.run_polling()

if __name__ == "__main__":
    main()
