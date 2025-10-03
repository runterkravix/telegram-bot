import random
import asyncio
from telethon import TelegramClient

# ---------------- CONFIG ----------------
# Account A credentials
api_id_A = 1234567         # replace with your API ID for A
api_hash_A = "your_api_hash_A"

# Account B credentials
api_id_B = 7654321         # replace with your API ID for B
api_hash_B = "your_api_hash_B"

# Telegram group username or ID
group = "yourgroupusername"  # e.g. mygroup or -1001234567890

# Delay between messages in seconds
MIN_DELAY = 20
MAX_DELAY = 30

# Probability to use Telegram reply feature
REPLY_PROBABILITY = 0.7

# Message bank file
MESSAGES_FILE = "messages_bank.txt"
# ----------------------------------------

# Load messages
with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
    messages = [line.strip() for line in f if line.strip()]

# Initialize clients
clientA = TelegramClient("sessionA", api_id_A, api_hash_A)
clientB = TelegramClient("sessionB", api_id_B, api_hash_B)

async def chat_loop():
    turn = 0
    last_msg = None  # to reply to previous message

    while True:
        msg = random.choice(messages)

        # Apply text style
        if turn % 2 == 0:
            msg = msg.capitalize()  # Person A
        else:
            msg = msg.lower()      # Person B

        # Decide reply vs normal (70% chance)
        use_reply = random.random() < REPLY_PROBABILITY and last_msg is not None

        if turn % 2 == 0:
            # Person A sends
            if use_reply:
                last_msg = await clientA.send_message(group, msg, reply_to=last_msg.id)
            else:
                last_msg = await clientA.send_message(group, msg)
        else:
            # Person B sends
            if use_reply:
                last_msg = await clientB.send_message(group, msg, reply_to=last_msg.id)
            else:
                last_msg = await clientB.send_message(group, msg)

        turn += 1
        await asyncio.sleep(random.randint(MIN_DELAY, MAX_DELAY))

async def main():
    await clientA.start()
    await clientB.start()
    print("Both accounts started. Chatting now...")
    await chat_loop()

if __name__ == "__main__":
    asyncio.run(main())
