import os
import time
import base64
import marshal
import random
import zlib
import re
import requests
import telebot
import ast
import subprocess
import json
import string
import hashlib
from datetime import datetime, timedelta
from telebot import types
from io import StringIO
from contextlib import redirect_stdout

# Bot token ve admin ID listesi
BOT_TOKEN = "8500043223:AAGNqLIe3qFHlbPo11DEgJjWqSE6CRj9-GE"
ADMIN_IDS = [8528166940, 8500043223]  # İki admin ID'si

print(f"DEBUG: Admin ID'ler ayarlandı: {ADMIN_IDS}")
print(f"DEBUG: Bot token: {BOT_TOKEN[:10]}...")

# Renk kodları
COLOR_BLUE = "\033[94m"
COLOR_GRAY = "\033[100m"
COLOR_RESET = "\033[0m"

# ASCII sanat
ASCII_ART = """⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀
⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣤⠶⠶⠶⠰⠦⣤⣀⠀⠙⣷⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⢀⣀⣤⢴⠆⠲⠶⠶⣤⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣆⠀⠀⢠⣾⣫⣶⣾⣿⣿⣿⣿⣷⣯⣿⣦⠈⠃⡇⠀⠀⠀⠀⢸⠘⢁⣶⣿⣵⣾⣿⣿⣿⣿⣷⣦⣝⣷⡄⠀⠀⡰⠂⠀
⠀⠀⣨⣷⣶⣿⣧⣛⣛⠿⠿⣿⢿⣿⣿⣛⣿⡿⠀⠀⡇⠀⠀⠀⠀⢸⠀⠈⢿⣟⣛⠿⢿⡿⢿⢿⢿⣛⣫⣼⡿⣶⣾⣅⡀⠀
⢀⡼⠋⠁⠀⠀⠈⠉⠛⠛⠻⠟⠸⠛⠋⠉⠁⠀⠀⢸⡇⠀⠀⠄⠀⢸⡄⠀⠀⠈⠉⠙⠛⠃⠻⠛⠛⠛⠉⠁⠀⠀⠈⠙⢧⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡇⢠⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⡇⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠟⠁⣿⠇⠀⠀⠀⠀⢸⡇⠙⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠰⣄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⠖⡾⠁⠀⠀⣿⠀⠀⠀⠀⠀⠘⣿⠀⠀⠙⡇⢸⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠄⠀
⠀⠀⢻⣷⡦⣤⣤⣤⡴⠶⠿⠛⠉⠁⠀⢳⠀⢠⡀⢿⣀⠀⠀⠀⠀⣠⡟⢀⣀⢠⠇⠀⠈⠙⠛⠷⠶⢦⣤⣤⣤⢴⣾⡏⠀⠀
⠀⠀⠈⣿⣧⠙⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢊⣙⠛⠒⠒⢛⣋⡚⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⡿⠁⣾⡿⠀⠀⠀
⠀⠀⠀⠘⣿⣇⠈⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⢿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⡟⠁⣼⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠘⣿⣦⠀⠻⣿⣷⣦⣤⣤⣶⣶⣶⣿⣿⣿⣿⠏⠀⠀⠻⣿⣿⣿⣿⣶⣶⣶⣦⣤⣴⣿⣿⠏⢀⣼⡿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⢿⣷⣄⠙⠻⠿⠿⠿⠿⠿⢿⣿⣿⣿⣁⣀⣀⣀⣀⣙⣿⣿⣿⠿⠿⠿⠿⠿⠿⠟⠁⣠⣿⡿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠻⣯⠙⢦⣀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⣠⠴⢋⣾⠟⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢧⡀⠈⠉⠒⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⠒⠉⠁⢀⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

# Bot başlatma
bot = telebot.TeleBot(BOT_TOKEN)

print("DEBUG: Bot nesnesi oluşturuldu")

# Kanal ve geliştirici bilgileri
CHANNEL_LINK = "https://t.me/+5a2WZsI_ETw4MzA0"
DEVELOPER = "@Scorpion292439"

# Dosya yolları
WORK_FOLDER = "BATUFLEX"
ARAB_ENCODE_FOLDER = "/storage/emulated/0/BATUFLEX/"
DATA_FOLDER = "data"

# JSON dosyaları
BANNED_FILE = os.path.join(DATA_FOLDER, "banned_users.json")
USERS_FILE = os.path.join(DATA_FOLDER, "registered_users.json")
VIP_FILE = os.path.join(DATA_FOLDER, "vip_users.json")
VIP_CODES_FILE = os.path.join(DATA_FOLDER, "vip_codes.json")
ADMIN_FILE = os.path.join(DATA_FOLDER, "admin_settings.json")
ANNOUNCEMENT_FILE = os.path.join(DATA_FOLDER, "announcements.json")

# Klasörleri oluştur
for folder in [WORK_FOLDER, ARAB_ENCODE_FOLDER, DATA_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Başlık ve son ek
HEADER = f"# Geliştirici {DEVELOPER} | Kanal: {CHANNEL_LINK}\n\n"
FOOTER = f"\n\n# Geliştirici {DEVELOPER} | Kanal: {CHANNEL_LINK}\n"

# Verileri yükle
def load_data():
    """Tüm veri dosyalarını yükler"""
    print("DEBUG: Veriler yükleniyor...")
    data = {
        "banned_users": set(),
        "registered_users": {},
        "vip_users": {},
        "vip_codes": {},
        "admin_settings": {},
        "announcements": []
    }
    
    files = {
        "banned_users": BANNED_FILE,
        "registered_users": USERS_FILE,
        "vip_users": VIP_FILE,
        "vip_codes": VIP_CODES_FILE,
        "admin_settings": ADMIN_FILE,
        "announcements": ANNOUNCEMENT_FILE
    }
    
    for key, file_path in files.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if key == "banned_users":
                        data[key] = set(content)
                    else:
                        data[key] = content
                print(f"DEBUG: {key} yüklendi: {len(content) if content else 0} kayıt")
            except Exception as e:
                print(f"DEBUG: {key} file error: {e}")
    
    return data

def save_data(key, data):
    """Belirli bir veriyi kaydeder"""
    try:
        files = {
            "banned_users": BANNED_FILE,
            "registered_users": USERS_FILE,
            "vip_users": VIP_FILE,
            "vip_codes": VIP_CODES_FILE,
            "admin_settings": ADMIN_FILE,
            "announcements": ANNOUNCEMENT_FILE
        }
        
        if key in files:
            with open(files[key], "w", encoding="utf-8") as f:
                if key == "banned_users":
                    json.dump(list(data), f)
                else:
                    json.dump(data, f, indent=4)
    except Exception as e:
        print(f"DEBUG: Save {key} error: {e}")

# Verileri yükle
print("DEBUG: Veri yükleniyor...")
data = load_data()
banned_users = data["banned_users"]
registered_users = data["registered_users"]
vip_users = data["vip_users"]
vip_codes = data["vip_codes"]
admin_settings = data["admin_settings"]
announcements = data["announcements"]

user_selections = {}

print(f"DEBUG: Admin ID'ler: {ADMIN_IDS}")
print(f"DEBUG: VIP kullanıcılar: {len(vip_users)}")
print(f"DEBUG: Kayıtlı kullanıcılar: {len(registered_users)}")

# Admin kontrol fonksiyonu - ÇOKLU ADMIN DESTEĞİ
def is_admin(user_id):
    """Kullanıcının admin olup olmadığını kontrol eder"""
    result = user_id in ADMIN_IDS
    print(f"DEBUG: Admin kontrolü - User ID: {user_id}, Admin ID'ler: {ADMIN_IDS}, Sonuç: {result}")
    return result

# VIP kontrolü
def is_vip(user_id):
    """Kullanıcının VIP olup olmadığını kontrol eder"""
    # Admin otomatik VIP
    if is_admin(user_id):
        print(f"DEBUG: {user_id} admin olduğu için VIP")
        return True
    
    user_id_str = str(user_id)
    if user_id_str in vip_users:
        vip_info = vip_users[user_id_str]
        if vip_info["expiry_date"] > datetime.now().isoformat():
            print(f"DEBUG: {user_id} aktif VIP")
            return True
        else:
            # VIP süresi dolmuş
            print(f"DEBUG: {user_id} VIP süresi dolmuş")
            del vip_users[user_id_str]
            save_data("vip_users", vip_users)
    print(f"DEBUG: {user_id} VIP değil")
    return False

def get_vip_days_left(user_id):
    """VIP gün sayısını döndürür"""
    if is_admin(user_id):
        return 9999  # Admin için sınırsız
    
    user_id_str = str(user_id)
    if user_id_str in vip_users:
        expiry_date = datetime.fromisoformat(vip_users[user_id_str]["expiry_date"])
        days_left = (expiry_date - datetime.now()).days
        return max(0, days_left)
    return 0

def generate_vip_code(days, max_uses=1):
    """VIP kodu oluşturur"""
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(chars) for _ in range(20))
    code = f"vip-code-sc-{random_part}"
    
    vip_codes[code] = {
        "days": days,
        "max_uses": max_uses,
        "used_count": 0,
        "created_date": datetime.now().isoformat(),
        "created_by": ADMIN_IDS[0]  # İlk admin
    }
    
    save_data("vip_codes", vip_codes)
    return code

def activate_vip_code(user_id, code):
    """VIP kodunu aktif eder"""
    if code in vip_codes:
        code_info = vip_codes[code]
        
        if code_info["used_count"] >= code_info["max_uses"]:
            return False, "Bu kod kullanım limitine ulaşmış."
        
        # VIP süresini ekle
        user_id_str = str(user_id)
        expiry_date = datetime.now() + timedelta(days=code_info["days"])
        
        if user_id_str in vip_users:
            # Mevcut VIP süresine ekle
            current_expiry = datetime.fromisoformat(vip_users[user_id_str]["expiry_date"])
            new_expiry = max(current_expiry, expiry_date)
            vip_users[user_id_str]["expiry_date"] = new_expiry.isoformat()
        else:
            # Yeni VIP oluştur
            vip_users[user_id_str] = {
                "activated_date": datetime.now().isoformat(),
                "expiry_date": expiry_date.isoformat(),
                "activated_by_code": code,
                "days": code_info["days"]
            }
        
        # Kodu güncelle
        vip_codes[code]["used_count"] += 1
        vip_codes[code]["last_used"] = datetime.now().isoformat()
        vip_codes[code]["used_by"] = user_id
        
        save_data("vip_users", vip_users)
        save_data("vip_codes", vip_codes)
        
        return True, f"VIP aktif edildi! {code_info['days']} gün VIP üyeliğiniz başladı."
    
    return False, "Geçersiz VIP kodu."

# Yardımcı fonksiyonlar
def clean_filename(filename):
    """Dosya adını temizler"""
    name = os.path.splitext(filename)[0]
    name = re.sub(r'\W+', '_', name)
    return name + ".py"

def get_sms_code():
    """SMS kodunu alır"""
    url = "https://raw.githubusercontent.com/muhammadkaracak/Sms/refs/heads/main/Sms.py"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def run_sms_encode(input_file, output_file):
    """SMS encode çalıştırır"""
    code = get_sms_code()
    with open("temp_sms.py", "w", encoding="utf-8") as f:
        f.write(code)
    
    process = subprocess.Popen(
        ["python", "temp_sms.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    output, _ = process.communicate(f"{input_file}\n{output_file}\n")
    os.remove("temp_sms.py")
    return output

def set_reaction(chat_id, message_id, emoji):
    """Mesaja reaksiyon ekler"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction"
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }
    try:
        requests.post(url, json=data)
    except:
        pass

# ========== ADMIN KOMUTLARI ==========
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    """Admin paneli"""
    user_id = message.from_user.id
    print(f"DEBUG: /admin komutu çağrıldı - User ID: {user_id}")
    
    admin_check = is_admin(user_id)
    print(f"DEBUG: Admin kontrol sonucu: {admin_check}")
    
    if not admin_check:
        bot.reply_to(message, f"❌ Bu komut sadece adminler içindir.\n\nUser ID: {user_id}\nAdmin ID'ler: {ADMIN_IDS}")
        return
    
    print(f"DEBUG: Admin panel gösteriliyor - User ID: {user_id}")
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("📢 Duyuru Yap", callback_data="admin_announce"),
        types.InlineKeyboardButton("🎟 VIP Kod Üret", callback_data="admin_generate_vip"),
        types.InlineKeyboardButton("📊 İstatistikler", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Kullanıcı Yönetimi", callback_data="admin_users"),
        types.InlineKeyboardButton("🔑 VIP Kodları", callback_data="admin_vip_codes"),
        types.InlineKeyboardButton("⬅️ Ana Menü", callback_data="back_to_menu")
    )
    
    bot.send_message(
        message.chat.id,
        f"👑 Admin Paneli\n\n"
        f"✅ Hoş geldiniz Admin! (ID: {user_id})\n"
        f"🔧 Aşağıdaki işlemlerden birini seçin:",
        reply_markup=keyboard
    )

@bot.message_handler(commands=['newvipcode'])
def generate_vip_command(message):
    """VIP kodu oluşturur"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.reply_to(message, f"❌ Bu komut sadece adminler içindir.\nUser ID: {user_id}\nAdmin ID'ler: {ADMIN_IDS}")
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Kullanım: /newvipcode <gün> <max_kullanım>\nÖrnek: /newvipcode 30 1")
            return
        
        days = int(parts[1])
        max_uses = int(parts[2])
        
        if days <= 0 or max_uses <= 0:
            bot.reply_to(message, "Gün ve max kullanım 0'dan büyük olmalı.")
            return
        
        code = generate_vip_code(days, max_uses)
        bot.reply_to(message, f"✅ Yeni VIP kodu oluşturuldu!\n\nKod: `{code}`\nSüre: {days} gün\nMax Kullanım: {max_uses}")
    
    except ValueError:
        bot.reply_to(message, "Geçersiz sayı formatı.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['key'])
def activate_vip_command(message):
    """VIP kodunu aktif eder"""
    user_id = message.from_user.id
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "Kullanım: /key <VIP_kodu>\nÖrnek: /key vip-code-sc-abc123")
            return
        
        code = parts[1]
        success, result_msg = activate_vip_code(user_id, code)
        
        if success:
            bot.reply_to(message, f"✅ {result_msg}")
        else:
            bot.reply_to(message, f"❌ {result_msg}")
    
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['myvip'])
def my_vip_info(message):
    """VIP bilgilerini gösterir"""
    user_id = message.from_user.id
    
    if is_admin(user_id):
        bot.reply_to(message,
            f"👑 ADMIN\n\n"
            f"✅ Tüm özelliklere erişiminiz var.\n"
            f"🔧 Admin paneli: /admin\n"
            f"🆔 Your ID: {user_id}\n"
            f"📋 Admin ID'ler: {ADMIN_IDS}"
        )
    elif is_vip(user_id):
        days_left = get_vip_days_left(user_id)
        expiry_date = datetime.fromisoformat(vip_users[str(user_id)]["expiry_date"]).strftime("%d.%m.%Y %H:%M")
        
        bot.reply_to(message,
            f"⭐ VIP ÜYESİNİZ!\n\n"
            f"📅 Kalan Süre: {days_left} gün\n"
            f"⏰ Bitiş Tarihi: {expiry_date}\n\n"
            f"✅ Tüm encode/decode yöntemlerini kullanabilirsiniz."
        )
    else:
        bot.reply_to(message,
            f"🔓 FREE ÜYESİNİZ\n\n"
            f"⚠️ Sadece Base64 encode kullanabilirsiniz.\n"
            f"⭐ VIP olmak için: /key <kod>\n"
            f"🆔 Your ID: {user_id}\n\n"
            f"💎 VIP özellikleri:\n"
            f"  • Tüm encode yöntemleri\n"
            f"  • Tüm decode yöntemleri\n"
            f"  • Arap encode\n"
            f"  • Advanced yöntemler\n"
            f"  • Ninjapy encode\n"
            f"  • Daha fazlası..."
        )

@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    """Başlangıç komutu"""
    user_id = message.from_user.id
    print(f"DEBUG: /start komutu - User ID: {user_id}")
    
    # Admin kontrolü
    if is_admin(user_id):
        print(f"DEBUG: Admin {user_id} start komutunu kullandı")
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("👑 Admin Panel", callback_data="admin_menu"),
            types.InlineKeyboardButton("🔐 Encode/Decode", callback_data="user_menu"),
            types.InlineKeyboardButton("ℹ️ Bot Bilgisi", callback_data="bot_info")
        )
        
        bot.send_message(
            message.chat.id,
            f"👑 Hoş geldiniz Admin! (ID: {user_id})\n\n"
            f"✅ Tüm özelliklere erişiminiz var.\n"
            f"🔧 Admin işlemleri için Admin Panel'i seçin.\n"
            f"🔐 Encode/Decode için diğer butonu seçin.\n\n"
            f"Admin ID'ler: {ADMIN_IDS}",
            reply_markup=keyboard
        )
        return
    
    # Normal kullanıcı için
    print(f"DEBUG: Normal kullanıcı {user_id} start komutunu kullandı")
    
    # Yasak kontrolü
    if user_id in banned_users:
        bot.reply_to(message, "❌ Yasaklı kullanıcısınız!")
        return
    
    # Kullanıcıyı kaydet
    if str(user_id) not in registered_users:
        registered_users[str(user_id)] = {
            "id": user_id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "first_join": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "is_vip": False
        }
        save_data("registered_users", registered_users)
        print(f"DEBUG: Yeni kullanıcı kaydedildi: {user_id}")
    else:
        # Son aktiviteyi güncelle
        registered_users[str(user_id)]["last_activity"] = datetime.now().isoformat()
        save_data("registered_users", registered_users)
    
    # VIP kontrolü
    vip_status = "⭐ VIP ÜYE" if is_vip(user_id) else "🔓 FREE ÜYE"
    vip_days = get_vip_days_left(user_id) if is_vip(user_id) else 0
    
    welcome_msg = (
        f"🤖 Hoş geldiniz!\n\n"
        f"🔒 Güvenli Dosya Şifreleyici Bot\n"
        f"👤 Geliştirici: {DEVELOPER}\n"
        f"📢 Kanal: {CHANNEL_LINK}\n\n"
        f"🎫 Durumunuz: {vip_status}\n"
        f"🆔 User ID: {user_id}\n"
    )
    
    if is_vip(user_id):
        welcome_msg += f"📅 Kalan VIP Günü: {vip_days} gün\n\n"
    else:
        welcome_msg += (
            f"⚠️ FREE sürümde sadece Base64 kullanabilirsiniz.\n"
            f"⭐ VIP olmak için: /key <kod>\n"
            f"📋 VIP bilgileri: /myvip\n\n"
        )
    
    welcome_msg += "Lütfen aşağıdaki menüden bir işlem seçin:"
    
    # Menüyü göster
    show_user_menu(message.chat.id, welcome_msg, user_id)

def show_user_menu(chat_id, message_text, user_id=None):
    """Kullanıcı menüsünü gösterir"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Admin kontrolü
    is_user_admin = is_admin(user_id) if user_id else False
    is_user_vip = is_vip(user_id) if user_id else False
    
    buttons = [
        types.InlineKeyboardButton("🔐 Encode", callback_data="encode"),
        types.InlineKeyboardButton("🔓 Decode", callback_data="decode"),
        types.InlineKeyboardButton("📋 VIP Bilgi", callback_data="vip_info"),
        types.InlineKeyboardButton("📢 Kanal", url=CHANNEL_LINK)
    ]
    
    # Sadece VIP/Admin için ek butonlar
    if is_user_vip or is_user_admin:
        buttons.insert(2, types.InlineKeyboardButton("🇦🇷 Arap Encode", callback_data="arab_encode"))
        buttons.insert(3, types.InlineKeyboardButton("🟣 Marshal Decode", callback_data="marshal_decode"))
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            keyboard.add(buttons[i], buttons[i+1])
        else:
            keyboard.add(buttons[i])
    
    # Admin için admin butonu ekle
    if is_user_admin:
        keyboard.add(types.InlineKeyboardButton("👑 Admin Panel", callback_data="admin_menu"))
    
    keyboard.add(types.InlineKeyboardButton("ℹ️ Bot Bilgisi", callback_data="bot_info"))
    
    bot.send_message(chat_id, message_text, reply_markup=keyboard)

# ========== CALLBACK HANDLER ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Callback sorgularını işler"""
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    
    print(f"DEBUG: Callback - User: {user_id}, Data: {call.data}")
    
    data = call.data
    
    if data == "admin_menu":
        print(f"DEBUG: Admin menu callback - User: {user_id}")
        if is_admin(user_id):
            admin_panel(call.message)
        else:
            bot.answer_callback_query(call.id, f"❌ Admin değilsiniz! ID: {user_id}", show_alert=True)
    
    elif data == "user_menu":
        welcome_msg = f"Ana menüye döndünüz.\n👤 Geliştirici: {DEVELOPER}\n🆔 User ID: {user_id}"
        show_user_menu(chat_id, welcome_msg, user_id)
    
    elif data == "bot_info":
        show_bot_info(call.message, user_id)
    
    elif data == "vip_info":
        my_vip_info(call.message)
        bot.answer_callback_query(call.id)
    
    elif data == "back_to_menu":
        welcome_msg = f"Ana menüye döndünüz.\n👤 Geliştirici: {DEVELOPER}\n🆔 User ID: {user_id}"
        show_user_menu(chat_id, welcome_msg, user_id)
    
    elif data == "encode":
        user_selections[chat_id] = {"operation": "encode", "user_id": user_id}
        
        # Admin ve VIP kontrolü
        if is_admin(user_id) or is_vip(user_id):
            methods = [
                ("Base64", "base64"),
                ("Marshal", "marshal"),
                ("Zlib", "zlib"),
                ("Base16", "base16"),
                ("Base32", "base32"),
                ("Marshal+Zlib", "marshal_zlib"),
                ("Advanced", "advanced"),
                ("Ninjapy", "ninjapy"),
                ("Zlib Base64", "zlib_base64"),
                ("Zlib Base85", "zlib_base85"),
                ("Marshal Zlib Base64", "marshal_zlib_base64"),
                ("Marshal Zlib Base85", "marshal_zlib_base85")
            ]
            title = "Encode Yöntemleri"
        else:
            methods = [("Base64", "base64")]
            title = "FREE Encode Yöntemleri\n⭐ Diğer yöntemler için VIP olun!"
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for label, value in methods:
            keyboard.add(types.InlineKeyboardButton(label, callback_data=f"encode:{value}"))
        
        # VIP değilse VIP ol butonu ekle
        if not is_vip(user_id) and not is_admin(user_id):
            keyboard.add(types.InlineKeyboardButton("⭐ VIP Ol", callback_data="vip_info"))
        
        keyboard.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="back_to_menu"))
        
        bot.edit_message_text(
            title,
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    
    elif data.startswith("encode:"):
        operation, method = data.split(':')
        user_selections[chat_id] = {"operation": operation, "method": method, "user_id": user_id}
        
        # VIP kontrolü (admin hariç)
        if not is_vip(user_id) and not is_admin(user_id) and method != "base64":
            bot.answer_callback_query(call.id, "❌ Bu yöntem sadece VIP'ler içindir!", show_alert=True)
            return
        
        bot.send_message(chat_id, f"🔐 {method.upper()} encode seçildi.\nLütfen .py dosyanızı gönderin.")
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    
    elif data == "decode":
        user_selections[chat_id] = {"operation": "decode", "user_id": user_id}
        
        # Decode için VIP/Admin kontrolü
        if not is_vip(user_id) and not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ Decode işlemi sadece VIP'ler içindir!", show_alert=True)
            return
        
        bot.send_message(chat_id, "🔓 Decode işlemi seçildi.\nLütfen .py dosyanızı gönderin.")
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    
    elif data == "arab_encode":
        # Sadece VIP'ler ve admin
        if not is_vip(user_id) and not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ Arap Encode sadece VIP'ler içindir!", show_alert=True)
            return
        
        user_selections[chat_id] = {"operation": "arab_encode", "user_id": user_id}
        bot.send_message(chat_id, "🇦🇷 Arap Encode seçildi.\nLütfen .py dosyanızı gönderin.")
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    
    elif data == "marshal_decode":
        user_selections[chat_id] = {"operation": "marshal_decode", "user_id": user_id}
        message_text = ("Lütfen @PycConvertBot'a MARSHAL dosyasını gönderin, "
                       ".pyc dosyası oluşturulacak. Sonra .pyc dosyasını "
                       "https://pylingual.io/ sitesine ekleyin.\n\n"
                       f"Geliştirici: {DEVELOPER}")
        bot.send_message(chat_id, message_text)
    
    elif data.startswith("admin_"):
        # Admin callback'leri
        if not is_admin(user_id):
            bot.answer_callback_query(call.id, "❌ Admin değilsiniz!", show_alert=True)
            return
        
        if data == "admin_announce":
            msg = bot.send_message(
                call.message.chat.id,
                "📢 Duyuru yapmak için mesajınızı gönderin.\n\n"
                "Format: [metin]\n"
                "İptal etmek için: /cancel"
            )
            bot.register_next_step_handler(msg, process_announcement)
        
        elif data == "admin_generate_vip":
            msg = bot.send_message(
                call.message.chat.id,
                "🎟 VIP kodu oluşturmak için format:\n"
                "/newvipcode <gün_sayısı> <max_kullanım>\n\n"
                "Örnek: /newvipcode 30 1"
            )
        
        elif data == "admin_stats":
            total_users = len(registered_users)
            vip_count = len(vip_users)
            active_vip = sum(1 for v in vip_users.values() if datetime.fromisoformat(v["expiry_date"]) > datetime.now())
            banned_count = len(banned_users)
            
            stats_text = (
                f"📊 Bot İstatistikleri\n\n"
                f"👥 Toplam Kullanıcı: {total_users}\n"
                f"⭐ VIP Üye: {vip_count}\n"
                f"✅ Aktif VIP: {active_vip}\n"
                f"🚫 Yasaklı: {banned_count}\n"
                f"🎟 VIP Kodları: {len(vip_codes)}\n"
                f"📢 Duyuru Sayısı: {len(announcements)}\n\n"
                f"👑 Admin ID'ler: {ADMIN_IDS}"
            )
            
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="admin_back"))
            
            bot.edit_message_text(
                stats_text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=keyboard
            )
        
        elif data == "admin_back":
            admin_panel(call.message)

def process_announcement(message):
    """Duyuruyu işler"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        return
    
    if message.text and message.text.startswith('/'):
        if message.text == '/cancel':
            bot.reply_to(message, "❌ Duyuru iptal edildi.")
        admin_panel(message)
        return
    
    announcement = {
        "id": len(announcements) + 1,
        "text": message.text,
        "date": datetime.now().isoformat(),
        "type": "text"
    }
    
    announcements.append(announcement)
    save_data("announcements", announcements)
    
    # Tüm kullanıcılara gönder
    success = 0
    failed = 0
    
    for user_id_str in registered_users.keys():
        try:
            bot.send_message(int(user_id_str), f"📢 DUYURU\n\n{message.text}")
            success += 1
        except:
            failed += 1
    
    bot.reply_to(message, f"✅ Duyuru gönderildi!\nBaşarılı: {success}\nBaşarısız: {failed}")
    admin_panel(message)

# ========== ENCODE/DECODE FONKSİYONLARI ==========
def encode_base64(data):
    """Base64 encode"""
    encoded = base64.b64encode(data)[::-1]
    return f"_ = lambda __ : __import__('base64').b64decode(__[::-1]);exec((_)({encoded}))"

def encode_marshal(data):
    """Marshal encode"""
    encoded = marshal.dumps(compile(data.decode(), 'module', 'exec'))
    return f"import marshal\nexec(marshal.loads({encoded}))"

def encode_zlib(data):
    """Zlib encode"""
    compressed = zlib.compress(data)
    encoded = base64.b64encode(compressed)[::-1]
    return f"_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)({encoded}))"

def encode_base16(data):
    """Base16 encode"""
    compressed = zlib.compress(data)
    encoded = base64.b16encode(compressed)[::-1]
    return f"_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));exec((_)({encoded}))"

def encode_base32(data):
    """Base32 encode"""
    compressed = zlib.compress(data)
    encoded = base64.b32encode(compressed)[::-1]
    return f"_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));exec((_)({encoded}))"

def encode_marshal_zlib(data):
    """Marshal + Zlib encode"""
    marshaled = marshal.dumps(compile(data.decode(), 'module', 'exec'))
    compressed = zlib.compress(marshaled)
    encoded = base64.b64encode(compressed)[::-1]
    return f"import marshal, zlib, base64\nexec(marshal.loads(zlib.decompress(base64.b64decode({encoded}))))"

def encode_advanced(data):
    """Advanced encode"""
    vars = random.sample(['x', 'y', 'z', 'p', 'q', 'r'], 3)
    a, b, c = vars[0], vars[1], vars[2]
    marshaled = marshal.dumps(compile(data.decode(), 'module', 'exec'))
    compressed = zlib.compress(marshaled)
    encoded = base64.b64encode(compressed)[::-1]
    return f"import base64, zlib, marshal\n{a} = lambda {b}: marshal.loads(zlib.decompress(base64.b64decode({b})))\n{c} = \"{encoded}\"\nexec({a}({c}))"

def encode_ninjapy(data):
    """Ninjapy encode"""
    encoded = base64.b64encode(data).decode("utf-8")
    return (f"import os, sys, base64 as B\n"
            f"C = '{encoded}'\n"
            f"exec(B.b64decode(C).decode('utf-8'))")

def encode_zlib_base64(data):
    """Zlib + Base64 encode"""
    compressed = zlib.compress(data)
    encoded = base64.b64encode(compressed).decode("utf-8")
    return f"exec(__import__('zlib').decompress(__import__('base64').b64decode('{encoded}')).decode('utf-8'))"

def encode_zlib_base85(data):
    """Zlib + Base85 encode"""
    compressed = zlib.compress(data)
    encoded = base64.b85encode(compressed).decode("utf-8")
    return f"exec(__import__('zlib').decompress(__import__('base64').b85decode('{encoded}')).decode('utf-8'))"

def encode_marshal_zlib_base64(data):
    """Marshal + Zlib + Base64 encode"""
    marshaled = marshal.dumps(compile(data.decode(), 'module', 'exec'))
    compressed = zlib.compress(marshaled)
    encoded = base64.b64encode(compressed).decode("utf-8")
    return f"import marshal, zlib, base64\nexec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"

def encode_marshal_zlib_base85(data):
    """Marshal + Zlib + Base85 encode"""
    marshaled = marshal.dumps(compile(data.decode(), 'module', 'exec'))
    compressed = zlib.compress(marshaled)
    encoded = base64.b85encode(compressed).decode("utf-8")
    return f"import marshal, zlib, base64\nexec(marshal.loads(zlib.decompress(base64.b85decode('{encoded}'))))"

def encode_file(method, file_path, user_id):
    """Dosyayı encode eder"""
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read().encode("utf-8")
    
    # FREE kullanıcılar için sadece base64
    if not is_vip(user_id) and not is_admin(user_id) and method != "base64":
        return "❌ Bu özellik sadece VIP üyeler içindir!\n⭐ VIP olmak için: /key <kod>"
    
    encode_functions = {
        "base64": encode_base64,
        "marshal": encode_marshal,
        "zlib": encode_zlib,
        "base16": encode_base16,
        "base32": encode_base32,
        "marshal_zlib": encode_marshal_zlib,
        "advanced": encode_advanced,
        "ninjapy": encode_ninjapy,
        "zlib_base64": encode_zlib_base64,
        "zlib_base85": encode_zlib_base85,
        "marshal_zlib_base64": encode_marshal_zlib_base64,
        "marshal_zlib_base85": encode_marshal_zlib_base85
    }
    
    if method in encode_functions:
        encoded = encode_functions[method](source)
        return HEADER + encoded + FOOTER
    else:
        return "Hata: Bilinmeyen encode yöntemi"

# Decode işlemleri
def auto_decode_file(file_path, user_id):
    """Dosyayı otomatik decode eder"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # VIP/Admin kontrolü
    if not is_vip(user_id) and not is_admin(user_id):
        return "❌ Decode işlemi sadece VIP üyeler içindir!\n⭐ VIP olmak için: /key <kod>"
    
    result = f"# Decoded by {DEVELOPER}\n# Kanal: {CHANNEL_LINK}\n\n"
    
    # Basit decode (gerçek decode işlemleri için önceki kodları kullanabilirsiniz)
    if "base64" in content.lower():
        try:
            # Base64 decode dene
            result += "# Base64 decode denendi\n"
            # Buraya gerçek decode kodunuzu ekleyin
        except:
            pass
    
    result += f"# Orijinal dosya içeriği ({len(content)} karakter):\n"
    if len(content) > 3000:
        result += content[:3000] + "...\n\n# Devamı kesildi"
    else:
        result += content
    
    return result

# ========== DOSYA İŞLEME ==========
@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Dosya işler"""
    user_id = message.from_user.id
    
    if user_id in banned_users and not is_admin(user_id):
        return
    
    try:
        chat_id = message.chat.id
        
        if chat_id not in user_selections or "operation" not in user_selections[chat_id]:
            bot.send_message(chat_id, "Lütfen önce bir işlem seçin!")
            return
        
        selection = user_selections[chat_id]
        operation = selection["operation"]
        method = selection.get("method", None)
        selection_user_id = selection.get("user_id", user_id)
        
        # Reaksiyon ekle
        set_reaction(chat_id, message.message_id, "👨🏻‍💻")
        
        # Dosyayı indir
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        if operation == "encode":
            filename = f"ENCODED-{method.upper()}.py"
            filepath = os.path.join(WORK_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                f.write(downloaded)
            
            process_encode(chat_id, filepath, operation, method, selection_user_id)
        
        elif operation == "decode":
            filename = "DECODED.py"
            filepath = os.path.join(WORK_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                f.write(downloaded)
            
            process_decode(chat_id, filepath, selection_user_id)
        
        elif operation == "arab_encode":
            # VIP/Admin kontrolü
            if not is_vip(selection_user_id) and not is_admin(selection_user_id):
                bot.send_message(chat_id, "❌ Arap Encode sadece VIP üyeler içindir!\n⭐ VIP olmak için: /key <kod>")
                return
            
            original_name = message.document.file_name
            clean_name = clean_filename(original_name)
            input_path = os.path.join(ARAB_ENCODE_FOLDER, clean_name)
            output_path = input_path + "_Enc.py"
            
            with open(input_path, 'wb') as f:
                f.write(downloaded)
            
            bot.send_message(chat_id, "🇦🇷 Arap encode işlemi başlatılıyor...")
            result = run_sms_encode(input_path, output_path)
            
            if "done encode" in result.lower() and os.path.exists(output_path):
                with open(output_path, 'rb') as output_file:
                    bot.send_document(chat_id, output_file)
                bot.send_message(chat_id, "✅ Encode tamamlandı!")
            else:
                error_msg = "Encode başarısız oldu.\n\nOlası nedenler:\n"
                if "cython" in result.lower():
                    error_msg += "- Cython yüklü değil.\n"
                if ".cpp" in result.lower() or "not found" in result.lower():
                    error_msg += "- Dosya adı veya yolu sorunlu.\n"
                error_msg += f"\nÇıktı:\n\n{result[:4000]}"
                bot.send_message(chat_id, error_msg)
            
            # Temizlik
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
        
        # Seçimi temizle
        user_selections[chat_id] = {}
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Hata: {str(e)}")

def process_encode(chat_id, filepath, operation, method, user_id):
    """Encode işlemini yapar"""
    progress_msg = bot.send_message(chat_id, "Encode işleniyor...\n[0%] █▒▒▒▒▒▒▒▒▒")
    
    for i in range(1, 101, random.randint(7, 14)):
        time.sleep(0.02)
        progress = min(i, 100)
        bars = '█' * (progress // 10)
        empty = '▒' * (10 - (progress // 10))
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=progress_msg.message_id,
            text=f"Encode işleniyor...\n[{progress}%] {bars}{empty}"
        )
    
    try:
        result = encode_file(method, filepath, user_id)
        
        if result.startswith("❌"):
            bot.delete_message(chat_id, progress_msg.message_id)
            bot.send_message(chat_id, result)
            os.remove(filepath)
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        
        bot.delete_message(chat_id, progress_msg.message_id)
        
        with open(filepath, 'rb') as f:
            bot.send_document(chat_id, f)
        
        status = "👑 ADMIN" if is_admin(user_id) else ("⭐ VIP" if is_vip(user_id) else "🔓 FREE")
        bot.send_message(chat_id, f"✅ Encode tamamlandı!\nYöntem: {method.upper()}\nDurum: {status}")
        
    except Exception as e:
        bot.delete_message(chat_id, progress_msg.message_id)
        bot.send_message(chat_id, f"❌ Encode hatası: {str(e)}")
    
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

def process_decode(chat_id, filepath, user_id):
    """Decode işlemini yapar"""
    progress_msg = bot.send_message(chat_id, "Decode işleniyor...\n[0%] █▒▒▒▒▒▒▒▒▒")
    
    for i in range(1, 101, random.randint(7, 14)):
        time.sleep(0.02)
        progress = min(i, 100)
        bars = '█' * (progress // 10)
        empty = '▒' * (10 - (progress // 10))
        
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=progress_msg.message_id,
            text=f"Decode işleniyor...\n[{progress}%] {bars}{empty}"
        )
    
    try:
        result = auto_decode_file(filepath, user_id)
        
        if result.startswith("❌"):
            bot.delete_message(chat_id, progress_msg.message_id)
            bot.send_message(chat_id, result)
            os.remove(filepath)
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        
        bot.delete_message(chat_id, progress_msg.message_id)
        
        with open(filepath, 'rb') as f:
            bot.send_document(chat_id, f)
        
        status = "👑 ADMIN" if is_admin(user_id) else ("⭐ VIP" if is_vip(user_id) else "🔓 FREE")
        bot.send_message(chat_id, f"✅ Decode tamamlandı!\nDurum: {status}")
        
    except Exception as e:
        bot.delete_message(chat_id, progress_msg.message_id)
        bot.send_message(chat_id, f"❌ Decode hatası: {str(e)}")
    
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

def show_bot_info(message, user_id=None):
    """Bot bilgilerini gösterir"""
    status = "👑 ADMIN" if is_admin(user_id) else ("⭐ VIP" if is_vip(user_id) else "🔓 FREE")
    
    info_text = f"""
🤖 <b>Bot Adı:</b> Güvenli Dosya Şifreleyici

<blockquote>
💻 <b>Dil:</b> Python
👤 <b>Geliştirici:</b> {DEVELOPER}
📢 <b>Kanal:</b> {CHANNEL_LINK}
🎫 <b>Durumunuz:</b> {status}
🆔 <b>User ID:</b> {user_id}
👑 <b>Admin ID'ler:</b> {ADMIN_IDS}
</blockquote>

<b>Özellikler:</b>

<code>🔓 FREE Sürüm:
• Base64 Encode

⭐ VIP Sürüm:
• Tüm encode yöntemleri
• Tüm decode yöntemleri
• Arap Encode
• Advanced Obfuscation
• Ninjapy
• Daha fazlası...</code>

👑 <i>Admin: Tüm özelliklere erişim</i>
💎 <i>VIP olmak için: /key &lt;kod&gt;</i>
📋 <i>VIP bilgileri: /myvip</i>
"""
    keyboard = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("⬅️ Geri", callback_data="back_to_menu")
    
    if is_admin(user_id):
        admin_button = types.InlineKeyboardButton("👑 Admin", callback_data="admin_menu")
        keyboard.add(back_button, admin_button)
    else:
        vip_button = types.InlineKeyboardButton("⭐ VIP Ol", callback_data="vip_info")
        keyboard.add(back_button, vip_button)
    
    if hasattr(message, 'message_id'):
        bot.edit_message_text(
            info_text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            info_text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

def main():
    """Ana fonksiyon"""
    print(f"{COLOR_BLUE}{ASCII_ART}{COLOR_RESET}")
    print(f"{COLOR_GRAY}                  BOT BAŞLATILDI - {DEVELOPER}                        {COLOR_RESET}")
    print(f"{COLOR_GRAY}                  Admin ID'ler: {ADMIN_IDS}                           {COLOR_RESET}")
    print(f"{COLOR_GRAY}                  DEBUG MODE: AKTİF                                    {COLOR_RESET}")
    
    while True:
        try:
            print("DEBUG: Bot polling başlatılıyor...")
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"DEBUG: Hata: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()