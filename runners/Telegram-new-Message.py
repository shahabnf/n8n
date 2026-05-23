#!/usr/bin/env python3
import requests
import os
import json
import sys

# Get Telegram token from command-line argument
if len(sys.argv) < 2:
    print(json.dumps({
        "status": "error",
        "message": "Telegram bot token argument missing"
    }))
    exit(1)

BOT_TOKEN = sys.argv[1]

URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
SAVE_FILE = "/home/runner/files/last_update_id.txt"

# Ensure directory exists
os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

# Read last processed update ID
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        try:
            last_saved_id = int(f.read().strip())
        except ValueError:
            last_saved_id = 0
else:
    last_saved_id = 0

# Fetch updates
params = {"offset": last_saved_id + 1}

try:
    response = requests.get(URL, params=params, timeout=10)
    data = response.json()
except Exception as e:
    print(json.dumps({
        "status": "error",
        "message": f"Network error: {str(e)}"
    }))
    exit(0)

# No updates
if not data.get("result"):
    print(json.dumps({
        "status": "no_new_updates"
    }))
    exit(0)

highest_update_id = last_saved_id
stock_triggered = False
triggered_data = {}

# Process updates
for update in data["result"]:
    current_id = update["update_id"]

    if current_id > highest_update_id:
        highest_update_id = current_id

    msg_obj = update.get("message") or update.get("channel_post")

    if msg_obj:
        text = msg_obj.get("text", "").lower().strip()

        if text == "stock":
            stock_triggered = True
            triggered_data = {
                "update_id": current_id,
                "text": msg_obj.get("text", "")
            }

# Save newest processed update ID
with open(SAVE_FILE, "w") as f:
    f.write(str(highest_update_id))

# Return simplified JSON back to n8n
if stock_triggered:
    print(json.dumps({
        "status": "update_message",
        "message": triggered_data.get("text", "")
    }))
else:
    print(json.dumps({
        "status": "no_new_updates"
    }))


