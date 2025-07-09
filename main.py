import os
import time
from telethon.sync import TelegramClient
from telethon.tl.types import InputMessagesFilterVideo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === Required credentials ===
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_file = os.getenv("SESSION_NAME", "session")

# === Channel IDs and options ===
source_channel = int(os.getenv("SOURCE_CHANNEL"))
target_channel = int(os.getenv("TARGET_CHANNEL"))

# Optional range and direction
start_id = os.getenv("VIDEO_ID_START")
end_id = os.getenv("VIDEO_ID_END")
reverse = os.getenv("REVERSE", "false").lower() == "true"

# Convert to int if provided
start_id = int(start_id) if start_id else None
end_id = int(end_id) if end_id else None

client = TelegramClient(session_file, api_id, api_hash)

with client:
    print("🎬 Starting video forwarder bot...")
    count = 0

    # Determine ID range
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
        # No specific range, use full iter_messages
        print("🔍 No ID range provided. Scanning all videos...")
        messages = client.iter_messages(source_channel, filter=InputMessagesFilterVideo)
        if reverse:
            messages = list(messages)[::-1]  # reverse the iterator

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
