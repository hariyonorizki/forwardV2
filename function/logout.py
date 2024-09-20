import os
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)
cursor = db.cursor()

async def logout_user(bot, event):
    user_id = event.sender_id
    session_name = f'sessions/session_{user_id}'
    session_file = f'{session_name}.session'

    # Hapus file sesi jika ada
    if os.path.exists(session_file):
        os.remove(session_file)
        
        # Delete session from database
        cursor.execute("DELETE FROM sessions WHERE user_id = %s", (user_id,))
        db.commit()

        await event.respond("Logout berhasil, sesi telah dihapus.")
    else:
        await event.respond("Tidak ada sesi yang ditemukan.")