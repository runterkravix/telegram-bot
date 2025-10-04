import os
import random
import asyncio
from telethon import TelegramClient

# Load credentials from Render/Railway environment variables
api_id_A = int(os.getenv("API_ID_A"))
api_hash_A = os.getenv("API_HASH_A")

api_id_B = int(os.getenv("API_ID_B"))
api_hash_B = os.getenv("API_HASH_B")

group = os.getenv("GROUP")  # Group username or ID

# Create sessions for both accounts
client_A = TelegramClient("accountA", api_id_A, api_hash_A)
client_B = TelegramClient("accountB", api_id_B, api_hash_B)

# Load messages from file
def load_messages():
    try:
        with open("message_bank.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Hello", "How are you", "Yes", "No", "Ok"]

messages = load_messages()

async def chat_loop():
    await client_A.start()
    await client_B.start()

    print("✅ Both accounts started. Chatting in group:", group)

    turn = 0  # 0 = A, 1 = B

    while True:
        sender = client_A if turn == 0 else client_B
        name = "A" if turn == 0 else "B"

        # pick random message
        msg = random.choice(messages)

        # format style
        if name == "A":
            msg = msg.capitalize()   # A starts with capital
        else:
            msg = msg.lower()        # B all lowercase

        # 70% chance to reply (use reply feature)
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

        # switch turn
        turn = 1 - turn

        # wait 20–30 sec before next
        await asyncio.sleep(random.randint(20, 30))

async def main():
    await asyncio.gather(chat_loop())

with client_A, client_B:
    client_A.loop.run_until_complete(main())
