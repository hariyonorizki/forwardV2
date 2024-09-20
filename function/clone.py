async def clone_messages(bot, event):
    user_id = event.sender_id
    await event.respond("Masukkan nama grup asal:")
    source_event = await bot.wait_for(events.NewMessage(from_user=user_id))
    source_chat = source_event.text

    await event.respond("Masukkan nama grup tujuan:")
    destination_event = await bot.wait_for(events.NewMessage(from_user=user_id))
    destination_chat = destination_event.text

    # Ambil client berdasarkan session user
    client = TelegramClient(f'sessions/session_{user_id}', os.getenv('API_ID'), os.getenv('API_HASH'))

    async with client:
        source = await client.get_entity(source_chat)
        destination = await client.get_entity(destination_chat)

        messages = await client.get_messages(source, limit=10)
        for message in messages:
            if message.text:
                await client.send_message(destination, message.text)
            elif message.media:
                await client.send_file(destination, message.media)

        await event.respond(f"Cloning pesan dari {source_chat} ke {destination_chat} selesai.")