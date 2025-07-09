from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
import time
from telethon.tl.types import InputMessagesFilterVideo

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")

source_channel = int(os.getenv("SOURCE_CHANNEL"))
target_channel = int(os.getenv("TARGET_CHANNEL"))
start_id = os.getenv("VIDEO_ID_START")
end_id = os.getenv("VIDEO_ID_END")
reverse = os.getenv("REVERSE", "false").lower() == "true"

start_id = int(start_id) if start_id else None
end_id = int(end_id) if end_id else None

client = TelegramClient(StringSession(string_session), api_id, api_hash)

with client:
    print("✅ Userbot Logged In!")

    count = 0
    if start_id and end_id:
        ids_range = range(start_id, end_id - 1, -1 if reverse else 1)
        for msg_id in ids_range:
            try:
                message = client.get_messages(source_channel, ids=msg_id)
                if message and message.media:
                    print(f"📤 Forwarding video ID {msg_id}")
                    client.send_file(
                        target_channel,
                        file=message.media,
                        caption=message.text or ""
                    )
                    count += 1
                    time.sleep(0.3)
            except Exception as e:
                print(f"❌ Failed at ID {msg_id}: {e}")
    else:
        print("🔍 No ID range provided. Scanning all videos...")
        messages = client.iter_messages(source_channel, filter=InputMessagesFilterVideo)
        if reverse:
            messages = list(messages)[::-1]

        for message in messages:
            try:
                if message and message.media:
                    print(f"📤 Forwarding video ID {message.id}")
                    client.send_file(
                        target_channel,
                        file=message.media,
                        caption=message.text or ""
                    )
                    count += 1
                    time.sleep(0.3)
            except Exception as e:
                print(f"❌ Failed to forward message {message.id}: {e}")

    print(f"✅ Done! Total {count} videos forwarded.")
