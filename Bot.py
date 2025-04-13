import logging
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration (fill these in)
API_ID = 1234567                     # Your API ID from my.telegram.org
API_HASH = 'your_api_hash_here'      # Your API HASH from my.telegram.org
BOT_TOKEN = 'your_bot_token_here'    # Your bot token from @BotFather

# Initialize clients
userbot = TelegramClient(StringSession(), API_ID, API_HASH)
bot_account = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Store our bot's ID
our_bot_id = None

async def get_bot_id():
    global our_bot_id
    me = await bot_account.get_me()
    our_bot_id = me.id
    logger.info(f"Configured bot ID: {our_bot_id}")

@userbot.on(events.NewMessage())
async def message_monitor(event):
    msg = event.message
    if msg.sender.bot:  # Check if message is from any bot
        try:
            # Log message details
            logger.info(
                f"Bot message detected\n"
                f"Chat ID: {event.chat_id}\n"
                f"Sender ID: {msg.sender.id}\n"
                f"Message: {msg.text}\n"
                f"Time: {msg.date}\n"
                "Scheduled for deletion in 10 seconds..."
            )

            # Wait 10 seconds before deletion
            await asyncio.sleep(10)
            
            # Delete the message
            await msg.delete()
            logger.info(f"Message deleted successfully from chat {event.chat_id}")
            
            # Check if it's another bot's message and notify
            if msg.sender.id != our_bot_id:
                logger.info(
                    "NOTIFICATION: Deleted message from another bot!\n"
                    f"Bot ID: {msg.sender.id}\n"
                    f"Chat ID: {event.chat_id}\n"
                    f"Message time: {msg.date}"
                )
                
        except Exception as e:
            logger.error(f"Failed to delete message: {str(e)}")

async def main():
    await get_bot_id()
    await userbot.start()
    logger.info("Userbot started! Monitoring messages...")
    await userbot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
