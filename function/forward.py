import os
import re
import time
from telethon import TelegramClient, events

# Dictionary untuk menyimpan aturan forwarding
forwarding_tasks = {}

async def handle_forward_command(bot, event):
    user_id = event.sender_id
    message_text = event.text

    pattern = r'/forward\s+(\w+)\s+(\d+)\s+([\d,]+)\s+>\s+([\d,]+)'
    match = re.match(pattern, message_text)

    if not match:
        await event.respond("❌ Format salah! Gunakan: /forward {TASK LABEL} {DELAY} {SOURCE_ID} > {DESTINATION_ID}")
        return

    task_label, delay, source_chats, target_chats = match.groups()
    delay = int(delay)

    # Cek apakah task_label ada
    if task_label not in tasks:
        await event.respond("❌ Task label tidak ditemukan! Gunakan /setup_task terlebih dahulu.")
        return

    source_ids = source_chats.split(',')
    target_ids = target_chats.split(',')

    # Mulai proses forwarding
    await event.respond(f"✅ Memulai forwarding dengan label '{task_label}'...")
    await forward_messages(bot, user_id, task_label, delay, source_ids, target_ids)

async def forward_messages(bot, user_id, task_label, delay, source_ids, target_ids):
    # Ambil pengaturan dari task
    task_config = tasks[task_label]

    client = TelegramClient(f'sessions/session_{user_id}', os.getenv('API_ID'), os.getenv('API_HASH'))

    async with client:
        @client.on(events.NewMessage(chats=source_ids))
        async def handler(event):
            message = event.message

            # Periksa filter, blacklist, dan replace di sini
            if should_forward_message(message, task_config):
                for target in target_ids:
                    if message.text:
                        await client.send_message(int(target), message.text)
                    elif message.media:
                        await client.send_file(int(target), message.media)

                print(f"Forward Pesan Berlangsung > {task_label}")
                time.sleep(delay)
                print(f"Forward Pesan Selesai > {task_label}")

async def should_forward_message(message, task_config):
    # Logika untuk filter dan blacklist
    # Misalnya: jika ada blacklist, periksa di sini
    if task_config['blacklist']:
        for item in task_config['blacklist']:
            if item in message.text:
                return False

    # Tambahkan logika untuk filter sesuai task_config['filter']

    return True