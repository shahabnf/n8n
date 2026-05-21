#!/usr/bin/env python3
import requests
import os
import json

BOT_TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
SAVE_FILE = "/home/runner/files/last_update_id.txt"

# 1. Ensure the directory exists to avoid write errors
os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        try:
            last_saved_id = int(f.read().strip())
        except ValueError:
            last_saved_id = 0
else:
    last_saved_id = 0

# 2. Fetch updates
params = {"offset": last_saved_id + 1}
try:
    response = requests.get(URL, params=params, timeout=10)
    data = response.json()
except Exception as e:
    print(json.dumps({"status": "error", "message": f"Network error: {str(e)}"}))
    exit(0) # Exit cleanly so n8n doesn't red-screen on a simple network blink

# If no updates, exit calmly
if not data.get("result"):
    print(json.dumps({"status": "no_new_updates"}))
    exit(0)

# 3. Process the messages and ALWAYS update the pointer to the latest update_id
# This prevents getting stuck in an infinite loop on non-stock messages
highest_update_id = last_saved_id
stock_triggered = False
triggered_data = {}

for update in data["result"]:
    current_id = update["update_id"]
    if current_id > highest_update_id:
        highest_update_id = current_id

    # Handle standard group/private messages OR channel posts safely
    msg_obj = update.get("message") or update.get("channel_post")
    if msg_obj:
        text = msg_obj.get("text", "").lower().strip()
        if text == "stock":
            stock_triggered = True
            triggered_data = {"update_id": current_id, "text": msg_obj.get("text", ""), "status": "valid"}

# 4. Save the highest ID we saw during this run
with open(SAVE_FILE, "w") as f:
    f.write(str(highest_update_id))

# 5. Return JSON back to n8n
if stock_triggered:
    print(json.dumps(triggered_data))
else:
    print(json.dumps({"status": "skipped", "last_processed_id": highest_update_id}))
