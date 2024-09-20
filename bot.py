import os
import mysql.connector
from telethon import TelegramClient, events
from dotenv import load_dotenv
from function.connect import connect_user
from function.clone import clone_messages
from function.forward import handle_forward_command
from function.logout import logout_user
from function.get_data import get_channel_list, get_group_list
from function.task_setup import setup_task, set_filter, set_blacklist, set_replace

# Load environment variables dari file .env
load_dotenv()

# Ambil API credentials dari environment variables
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# Fungsi untuk menguji koneksi MySQL
def test_mysql_connection():
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )
        if db_connection.is_connected():
            print("✅ Koneksi MySQL berhasil!")
            db_connection.close()
    except mysql.connector.Error as err:
        print(f"❌ Koneksi MySQL gagal: {err}")

# Inisialisasi client bot
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Tes koneksi MySQL saat bot mulai
print("🔄 Memulai proses tes koneksi MySQL...")
test_mysql_connection()

# Sambutan ketika user mengirimkan command /start
@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await event.respond("Selamat datang! Gunakan /connect untuk menghubungkan akun Anda.")

# Command /connect untuk proses login
@bot.on(events.NewMessage(pattern='/connect'))
async def handle_connect(event):
    await connect_user(bot, event)

# Command /clone untuk cloning pesan lama
@bot.on(events.NewMessage(pattern='/clone'))
async def handle_clone(event):
    await clone_messages(bot, event)

# Command /forward untuk meneruskan pesan berdasarkan format yang diinginkan
@bot.on(events.NewMessage(pattern='/forward'))
async def handle_forward(event):
    await handle_forward_command(bot, event)

# Command /logout untuk logout user dan menghapus sesi
@bot.on(events.NewMessage(pattern='/logout'))
async def handle_logout(event):
    await logout_user(bot, event)

# Command /get_channel untuk mendapatkan daftar channel
@bot.on(events.NewMessage(pattern='/get_channel'))
async def handle_get_channel(event):
    await get_channel_list(bot, event)

# Command /get_group untuk mendapatkan daftar grup
@bot.on(events.NewMessage(pattern='/get_group'))
async def handle_get_group(event):
    await get_group_list(bot, event)

# Command /setup_task untuk mengatur label dan konfigurasi
@bot.on(events.NewMessage(pattern='/setup_task'))
async def handle_setup_task(event):
    await setup_task(bot, event)

# Command /filter untuk mengatur filter pesan
@bot.on(events.NewMessage(pattern='/filter'))
async def handle_filter(event):
    await set_filter(bot, event)

# Command /blacklist untuk mengatur blacklist pesan
@bot.on(events.NewMessage(pattern='/blacklist'))
async def handle_blacklist(event):
    await set_blacklist(bot, event)

# Command /replace untuk mengatur replace pesan
@bot.on(events.NewMessage(pattern='/replace'))
async def handle_replace(event):
    await set_replace(bot, event)

# Jalankan bot
bot.run_until_disconnected()