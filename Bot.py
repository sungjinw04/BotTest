from pyrogram import Client, filters
import asyncio

API_ID = 28620311  # Replace with your API ID
API_HASH = "3b5c4ed0598e48fc1ab552675555e693"  # Replace with your API hash
BOT_TOKEN = "7658143490:AAGbhmQSu9_eVq9hpjEt2DRD-iZMX8dRq04"  # Replace with your bot token

app = Client("test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to start the bot
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Bot is running. Add me to a group as admin to begin logging bot messages.")

# Command to trigger scan in group
@app.on_message(filters.command("scanbots"))
async def scan_bot_messages(client, message):
    chat_id = message.chat.id
    await message.reply("Scanning for recent bot messages...")

    found = 0
    async for msg in client.get_chat_history(chat_id, limit=100):
        if msg.from_user and msg.from_user.is_bot:
            found += 1
            with open("bot_messages.txt", "a") as f:
                f.write(f"Bot Message ID: {msg.id} | From: {msg.from_user.first_name} (ID: {msg.from_user.id})\n")
    
    await message.reply(f"Scan complete. Found {found} bot messages.")

app.run()

