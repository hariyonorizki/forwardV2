import os

async def logout_user(bot, event):
    user_id = event.sender_id
    session_name = f'sessions/session_{user_id}'
    session_file = f'{session_name}.session'

    # Hapus file sesi jika ada
    if os.path.exists(session_file):
        os.remove(session_file)
        await event.respond("Logout berhasil, sesi telah dihapus.")
    else:
        await event.respond("Tidak ada sesi yang ditemukan.")