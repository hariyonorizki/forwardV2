import os
import mysql.connector
from telethon import TelegramClient
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)
cursor = db.cursor()

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Ensure the 'sessions' directory exists
if not os.path.exists('sessions'):
    os.makedirs('sessions')

async def connect_user(bot, event):
    user_id = event.sender_id
    session_name = f'sessions/session_{user_id}'
    session_file = f'{session_name}.session'

    client = TelegramClient(session_name, os.getenv('API_ID'), os.getenv('API_HASH'))

    await client.connect()
    if not await client.is_user_authorized():
        await event.respond("Silakan masukkan nomor telepon Anda:")
        phone_event = await bot.wait_for(events.NewMessage(from_user=user_id))
        phone = phone_event.text

        # Save and encrypt phone number
        encrypted_phone = cipher_suite.encrypt(phone.encode())
        with open(f'{session_file}_phone', 'wb') as f:
            f.write(encrypted_phone)

        await client.send_code_request(phone)
        await event.respond("Masukkan kode OTP (format: 1 2 3 4 5):")
        otp_event = await bot.wait_for(events.NewMessage(from_user=user_id))
        code = otp_event.text.replace(' ', '')

        try:
            await client.sign_in(phone, code)
            await event.respond("Berhasil login!")
            
            # Save session in database
            cursor.execute("INSERT INTO sessions (user_id, session_data) VALUES (%s, %s)", (user_id, session_name))
            db.commit()
        except Exception as e:
            await event.respond(f"Login gagal: {str(e)}")
    else:
        await event.respond("Anda sudah login.")