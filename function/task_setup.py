import re
import os
import mysql.connector
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

# Dictionary untuk menyimpan task
tasks = {}

# Fungsi untuk membuat atau mengatur task
async def setup_task(bot, event):
    message_text = event.text.strip()
    
    # Contoh: /setup_task label1
    match = re.match(r'/setup_task\s+(\w+)', message_text)
    if match:
        label = match.group(1)
        tasks[label] = {
            'filter': 'all',     # Default: semua pesan diteruskan
            'blacklist': None,   # Default: tidak ada blacklist
            'replace': None      # Default: tidak ada replace
        }
        await event.respond(f"✅ Task '{label}' berhasil dibuat.")

        # Simpan task ke database
        cursor.execute("INSERT INTO tasks (label, filter, blacklist, replace) VALUES (%s, %s, %s, %s)", 
                       (label, 'all', None, None))
        db.commit()
    else:
        await event.respond("❌ Format salah! Gunakan: /setup_task <label>")

# Fungsi untuk mengatur filter pesan
async def set_filter(bot, event):
    message_text = event.text.strip()
    
    # Contoh: /filter label1 video,photo,document
    match = re.match(r'/filter\s+(\w+)\s+(.+)', message_text)
    if match:
        label = match.group(1)
        filter_types = match.group(2).split(',')

        if label in tasks:
            tasks[label]['filter'] = filter_types
            await event.respond(f"✅ Filter untuk '{label}' berhasil diatur: {', '.join(filter_types)}")

            # Update filter di database
            cursor.execute("UPDATE tasks SET filter = %s WHERE label = %s", (','.join(filter_types), label))
            db.commit()
        else:
            await event.respond("❌ Label tidak ditemukan! Gunakan /setup_task terlebih dahulu.")
    else:
        await event.respond("❌ Format salah! Gunakan: /filter <label> <filter_type>")

# Fungsi untuk mengatur blacklist pesan
async def set_blacklist(bot, event):
    message_text = event.text.strip()
    
    # Contoh: /blacklist label1 url
    match = re.match(r'/blacklist\s+(\w+)\s+(.+)', message_text)
    if match:
        label = match.group(1)
        blacklist_items = match.group(2).split(',')

        if label in tasks:
            tasks[label]['blacklist'] = blacklist_items
            await event.respond(f"✅ Blacklist untuk '{label}' berhasil diatur: {', '.join(blacklist_items)}")

            # Update blacklist di database
            cursor.execute("UPDATE tasks SET blacklist = %s WHERE label = %s", (','.join(blacklist_items), label))
            db.commit()
        else:
            await event.respond("❌ Label tidak ditemukan! Gunakan /setup_task terlebih dahulu.")
    else:
        await event.respond("❌ Format salah! Gunakan: /blacklist <label> <item>")

# Fungsi untuk mengatur replace pesan
async def set_replace(bot, event):
    message_text = event.text.strip()
    
    # Contoh: /replace label1 caption 'new caption'
    match = re.match(r'/replace\s+(\w+)\s+(caption|button)\s+(.+)', message_text)
    if match:
        label = match.group(1)
        replace_type = match.group(2)
        replace_value = match.group(3)

        if label in tasks:
            if replace_type == 'caption':
                tasks[label]['replace'] = {'caption': replace_value}
                await event.respond(f"✅ Caption replace untuk '{label}' berhasil diatur.")

                # Update replace di database
                cursor.execute("UPDATE tasks SET replace = %s WHERE label = %s", (replace_value, label))
                db.commit()
            elif replace_type == 'button':
                buttons = replace_value.split(' ')
                if len(buttons) == 2 or len(buttons) == 4:
                    tasks[label]['replace'] = {'button': buttons}
                    await event.respond(f"✅ Button replace untuk '{label}' berhasil diatur.")
                    
                    # Update replace di database
                    cursor.execute("UPDATE tasks SET replace = %s WHERE label = %s", (','.join(buttons), label))
                    db.commit()
                else:
                    await event.respond("❌ Format salah! Gunakan: /replace <label> button <ButtonLabel> <ButtonLink> [optional: <ButtonLabel> <ButtonLink>]")
        else:
            await event.respond("❌ Label tidak ditemukan! Gunakan /setup_task terlebih dahulu.")
    else:
        await event.respond("❌ Format salah! Gunakan: /replace <label> <caption|button> <value>")