import re
from telethon import TelegramClient, events

# Simpan aturan forwarding dalam dictionary (label -> source -> target)
forwarding_rules = {}

# Fungsi untuk menampilkan menu bantuan forwarding
async def show_forwarding_help(event):
    help_message = """
❇️ Forwarding Assistance Menu ❇️

Use this menu to configure auto message forwarding.

🛠 Before using this command, retrieve chat IDs using /getchannel, /getgroup, or /getuser.

Follow the format below when adding channels, users, or bots:
/forward ACTION LABEL SOURCE_CHAT_ID -> TARGET_CHAT_ID

🆘 Note: The LABEL should not contain spaces or special characters. Keep it simple.

===============
Examples

➡️ One-to-One Chat
/forward add work1 22222 -> 66666

➡️ Many-to-One Chat
/forward add work1 22222,33333 -> 66666

➡️ One-to-Many Chat
/forward add work1 22222 -> 66666,77777

➡️ Many-to-Many Chat
/forward add work1 22222,33333 -> 66666,77777
"""
    await event.respond(help_message)

# Fungsi utama untuk menangani perintah forward
async def handle_forward_command(bot, event):
    user_id = event.sender_id
    message_text = event.text

    # Jika user hanya mengetik /forward, tampilkan menu bantuan
    if message_text.strip() == '/forward':
        await show_forwarding_help(event)
        return

    # Parse perintah dari user
    pattern = r'/forward\s+(\w+)\s+(\w+)\s+([\d,]+)\s+->\s+([\d,]+)'
    match = re.match(pattern, message_text)

    if not match:
        await event.respond("❌ Format salah! Gunakan format yang benar seperti di menu bantuan.")
        return

    action, label, source_chats, target_chats = match.groups()

    # Pisahkan ID source dan target
    source_ids = source_chats.split(',')
    target_ids = target_chats.split(',')

    # Tangani perintah add untuk menambah aturan forwarding
    if action == 'add':
        forwarding_rules[label] = {
            'sources': source_ids,
            'targets': target_ids
        }
        await event.respond(f"✅ Forwarding rule '{label}' berhasil ditambahkan!")
        await forward_messages(bot, user_id, label)
    else:
        await event.respond("❌ Aksi tidak dikenal! Gunakan 'add' untuk menambah aturan.")

# Fungsi untuk menangani forwarding pesan sesuai aturan yang diberikan
async def forward_messages(bot, user_id, label):
    # Ambil aturan dari label
    rule = forwarding_rules.get(label)

    if not rule:
        return

    sources = rule['sources']
    targets = rule['targets']

    # Ambil client user
    client = TelegramClient(f'sessions/session_{user_id}', os.getenv('API_ID'), os.getenv('API_HASH'))

    async with client:
        @client.on(events.NewMessage(chats=sources))
        async def handler(event):
            message = event.message

            for target in targets:
                if message.text:
                    await client.send_message(int(target), message.text)
                elif message.media:
                    await client.send_file(int(target), message.media)
        
        await client.run_until_disconnected()