import os
import random
import asyncio
from telethon import TelegramClient

# Use session files for login (no API_ID/API_HASH needed)
client_A = TelegramClient("accountA", 0, "")
client_B = TelegramClient("accountB", 0, "")

group = os.getenv("GROUP")  # Group username or numeric ID

# Load messages from file
def load_messages():
    try:
        with open("message_bank.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Hello", "How are you", "Yes", "No", "Ok"]

messages = load_messages()

async def chat_loop():
    print("✅ Both accounts started. Chatting in group:", group)
    turn = 0  # 0 = A, 1 = B

    while True:
        sender = client_A if turn == 0 else client_B
        name = "A" if turn == 0 else "B"

        # Pick random message
        msg = random.choice(messages)

        # Capitalization rules
        msg = msg.capitalize() if name == "A" else msg.lower()

        # 70% chance to reply
        use_reply = random.random() < 0.7

        try:
            if use_reply:
                async for m in sender.iter_messages(group, limit=1):
                    if m:
                        await sender.send_message(group, msg, reply_to=m.id)
                        print(f"[{name}] replied: {msg}")
                        break
            else:
                await sender.send_message(group, msg)
                print(f"[{name}] said: {msg}")

        except Exception as e:
            print(f"Error sending message: {e}")

        # Switch turn
        turn = 1 - turn

        # Wait 20–30 seconds
        await asyncio.sleep(random.randint(20, 30))

async def main():
    await client_A.start()
    await client_B.start()
    await chat_loop()

# Run the bot
asyncio.run(main())
