from telethon.tl.types import Channel, Chat

# Fungsi untuk mendapatkan daftar channel
async def get_channel_list(bot, event):
    user_id = event.sender_id
    client = TelegramClient(f'sessions/session_{user_id}', os.getenv('API_ID'), os.getenv('API_HASH'))

    async with client:
        dialogs = await client.get_dialogs()
        channel_list = []

        for dialog in dialogs:
            if isinstance(dialog.entity, Channel) and dialog.entity.megagroup is False:
                channel_list.append((dialog.entity.title, dialog.entity.id))

        if channel_list:
            message = "Channel List:\n"
            for idx, (name, channel_id) in enumerate(channel_list, start=1):
                message += f"{idx} - {name} - ID: {channel_id}\n"
            await event.respond(message)
        else:
            await event.respond("Tidak ada channel yang ditemukan.")

# Fungsi untuk mendapatkan daftar grup
async def get_group_list(bot, event):
    user_id = event.sender_id
    client = TelegramClient(f'sessions/session_{user_id}', os.getenv('API_ID'), os.getenv('API_HASH'))

    async with client:
        dialogs = await client.get_dialogs()
        group_list = []

        for dialog in dialogs:
            if isinstance(dialog.entity, Channel) and dialog.entity.megagroup is True:
                group_list.append((dialog.entity.title, dialog.entity.id))
            elif isinstance(dialog.entity, Chat):
                group_list.append((dialog.entity.title, dialog.entity.id))

        if group_list:
            message = "Group List:\n"
            for idx, (name, group_id) in enumerate(group_list, start=1):
                message += f"{idx} - {name} - ID: {group_id}\n"
            await event.respond(message)
        else:
            await event.respond("Tidak ada grup yang ditemukan.")