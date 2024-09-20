import os
import re
import time
from telethon import TelegramClient, events

# Menyimpan status tugas clone dan forward
active_forwarding_tasks = set()
active_cloning_tasks = set()

async def handle_clone_command(bot, event):
    user_id = event.sender_id
    message_text = event.text

    pattern = r'/clone\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+>(\d+)'
    match = re.match(pattern, message_text)

    if not match:
        await event.respond("❌ Format salah! Gunakan: /clone {TASK LABEL} {DELAY} {SOURCE ID} {MESSAGE ID} {LIMIT} > {DESTINATION ID}")
        return

    task_label, delay, source_id, start_message_id, limit, destination_id = match.groups()
    delay = int(delay)
    limit = int(limit)

    # Cek apakah task_label ada
    if task_label not in tasks:
        await event.respond("❌ Task label tidak ditemukan! Gunakan /setup_task terlebih dahulu.")
        return

    # Jika ada proses forward yang sedang berjalan, tunda clone
    if active_forwarding_tasks:
        await event.respond("🔄 Menunggu proses forward selesai sebelum memulai clone...")
        active_cloning_tasks.add((user_id, task_label, delay, source_id, start_message_id, limit, destination_id))
        return

    # Mulai proses cloning
    await event.respond(f"✅ Memulai proses clone dengan label '{task_label}'...")
    await clone_messages(bot, user_id, task_label, delay, source_id, start_message_id, limit, destination_id)

async def clone_messages(bot, user_id, task_label, delay, source_id, start_message_id, limit, destination_id):
    active_cloning_tasks.add((user_id, task_label, delay, source_id, start_message_id, limit, destination_id))

    client = TelegramClient(f'sessions/session_{user_id}', os.getenv('API_ID'), os.getenv('API_HASH'))

    async with client:
        # Ambil pesan dari grup sumber
        messages = await client.get_messages(int(source_id), limit=None, min_id=int(start_message_id))
        cloned_count = 0

        for message in messages:
            if cloned_count >= limit:
                break

            if message.text or message.media:
                if message.text:
                    await client.send_message(int(destination_id), message.text)
                elif message.media:
                    await client.send_file(int(destination_id), message.media)

                cloned_count += 1
                print(f"Clone pesan ke {destination_id} > {task_label}")
                time.sleep(delay)

        await event.respond(f"✅ Proses clone selesai. {cloned_count} pesan telah dikloning ke {destination_id}.")
        active_cloning_tasks.remove((user_id, task_label, delay, source_id, start_message_id, limit, destination_id))

        # Cek apakah ada tugas cloning yang tertunda
        if active_cloning_tasks:
            next_task = active_cloning_tasks.pop()
            await clone_messages(bot, user_id, *next_task)