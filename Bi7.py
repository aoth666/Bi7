import requests
import time
import itertools
import os
from colorama import Fore, init
import os
init(autoreset=True)

MESSAGES_FILE = "names.txt"
DELAY = 0

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        print(f"[!] File '{MESSAGES_FILE}' not found. Create it and add messages inside.")
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]

def send_message(channel_id, token, content):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {"content": content}
    try:
        r = requests.post(url, headers=headers, json=payload)
        return r
    except Exception as e:
        print(f"[!] Connection error: {e}")
        return None
os.system("clear")
def main():
    print(Fore.LIGHTRED_EX + """\n██╗  ██╗██╗██╗     ██╗     ███████╗██████╗  ██████╗     ██╗ ██╗   ██╗██╗ █████╗   ███╗
██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗██╔════╝  ██████████╗ ██╔╝██║██╔══██╗ ████║
█████═╝ ██║██║     ██║     █████╗  ██████╔╝╚█████╗   ╚═██╔═██╔═╝██╔╝ ██║╚█████╔╝██╔██║
██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗ ╚═══██╗  ██████████╗███████║██╔══██╗╚═╝██║
██║ ╚██╗██║███████╗███████╗███████╗██║  ██║██████╔╝  ╚██╔═██╔══╝╚════██║╚█████╔╝███████╗
╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝    ╚═╝ ╚═╝        ╚═╝ ╚════╝ ╚══════╝\n""")

    token = input(Fore.LIGHTRED_EX + "Enter user token: " + Fore.LIGHTGREEN_EX ).strip()
    channel_id = input(Fore.LIGHTRED_EX + "Enter channel ID: " + Fore.LIGHTGREEN_EX).strip()

    messages = load_messages()
    if not messages:
        print("[-] No messages found in names.txt.")
        return

    print(f"[*] Loaded {len(messages)} messages. Starting loop...")
    try:
        for msg in itertools.cycle(messages):
            r = send_message(channel_id, token, msg)
            if r is None:
                continue
            if r.status_code == 200:
                print(f"[+] Sent: {msg}")
            elif r.status_code == 429:
                retry = r.json().get("retry_after", 1)
                print(f"[!] Rate limited. Waiting {retry} sec.")
                time.sleep(retry)
            else:
                print(f"[-] Error {r.status_code}: {r.text}")
            time.sleep(DELAY)
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")

if __name__ == "__main__":
    main()
