import telebot
from telebot import types
import os
import json

TOKEN = '8475878629:AAG2LhDAFGCFNTz6iFq_SECmunU1pJTMlzg'
bot = telebot.TeleBot(TOKEN)

# Fayllar
ADMIN_FILE = 'adminlar.json'
MOVIE_FILE = 'kinolar.json'
CHANNEL_FILE = 'kanal.txt'

# Egasi
OWNER_ID = 8098302197  # O'zgartiring agar kerak bo‘lsa

# Fayllarni tekshirish
if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, 'w') as f:
        json.dump([OWNER_ID], f)

if not os.path.exists(MOVIE_FILE):
    with open(MOVIE_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(CHANNEL_FILE):
    with open(CHANNEL_FILE, 'w') as f:
        f.write('@yourchannel')  # O'zgartiring

# Foydali funksiyalar
def is_admin(user_id):
    with open(ADMIN_FILE) as f:
        return user_id in json.load(f)

def get_channel():
    with open(CHANNEL_FILE) as f:
        return f.read().strip()

def load_movies():
    with open(MOVIE_FILE) as f:
        return json.load(f)

def save_movies(movies):
    with open(MOVIE_FILE, 'w') as f:
        json.dump(movies, f)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    channel = get_channel()
    try:
        member = bot.get_chat_member(channel, user_id)
        if member.status in ['left', 'kicked']:
            raise Exception("Not subscribed")
    except:
        btn = types.InlineKeyboardButton("Obuna bo‘lish", url=f"https://t.me/{channel.lstrip('@')}")
        markup = types.InlineKeyboardMarkup().add(btn)
        bot.send_message(user_id, "Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=markup)
        return

    text = "Assalomu alaykum! 🎬 Kino kodini yoki nomini yuboring."
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📩 Bosh admin bilan bog‘lanish")
    bot.send_message(user_id, text, reply_markup=markup)

# Bosh admin bilan bog‘lanish
@bot.message_handler(func=lambda m: m.text == "📩 Bosh admin bilan bog‘lanish")
def contact_admin(message):
    bot.send_message(message.chat.id, "Bosh admin: @STIZZY_SALE_1")

# Kino qo‘shish bosqichlari
add_code = {}

@bot.message_handler(commands=['panel'])
def admin_panel(message):
    if not is_admin(message.from_user.id): return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎬 Kino kodlari", "📢 Xabar yuborish")
    markup.row("➕ Admin qo‘shish", "➖ Admin o‘chirish", "📋 Adminlar")
    markup.row("📣 Kanal ulash")
    bot.send_message(message.chat.id, "Admin panelga xush kelibsiz", reply_markup=markup)

# Kino kod qo‘shish
@bot.message_handler(func=lambda m: m.text == "🎬 Kino kodlari")
def ask_code(message):
    if not is_admin(message.from_user.id): return
    bot.send_message(message.chat.id, "Kino kodini yoki nomini yuboring:")
    add_code[message.from_user.id] = {"step": "awaiting_code"}

@bot.message_handler(func=lambda m: m.from_user.id in add_code)
def handle_kino
