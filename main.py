from instagrapi import Client
import time

username = 'pawankumarpawankumar1046'
password = 'Punit123'

base_reply = '𝐓𝐔𝐌𝐇𝐀𝐑𝐀 𝐏𝐀𝐏𝐀 💀_𝐔𝐍𝐊𝐖𝐎𝐍_𝟐𝟐💀𝐍𝐀𝐀𝐌 𝐓𝐀𝐎 𝐒𝐔𝐍𝐀 𝐇𝐄 𝐇𝐎𝐆𝐀 👹'
last_seen = {}
cooldown_tracker = {}
ignored_groups = set()
COOLDOWN_SECONDS = 10

def login():
    client = Client()
    client.login(username, password)
    print("[+] Logged in as", username)
    return client

def check_group_and_reply(api):
    threads = api.direct_threads()
    for thread in threads:
        if thread.id in ignored_groups:
            continue

        if not thread.is_group or not thread.messages:
            continue

        last_msg = thread.messages[0]

        # Apna message ignore karo
        if last_msg.user_id == api.user_id:
            continue

        now = time.time()
        sender_id = last_msg.user_id

        # Same message pe dobara reply na ho
        if thread.id not in last_seen or last_seen[thread.id] != last_msg.id:
            # Cooldown check
            if sender_id in cooldown_tracker and now - cooldown_tracker[sender_id] < COOLDOWN_SECONDS:
                continue

            try:
                # User mention karne ki koshish
                try:
                    user_info = api.user_info(sender_id)
                    sender_username = user_info.username
                    reply_text = f"@{sender_username} {base_reply}"
                except:
                    reply_text = base_reply

                api.direct_send(reply_text, thread_ids=[thread.id])
                last_seen[thread.id] = last_msg.id
                cooldown_tracker[sender_id] = now
                print(f"[GC] Replied in group: {thread.thread_title}")

            except Exception as e:
                if "403" in str(e):
                    print(f"[!] Removed from group: {thread.thread_title}, skipping…")
                    ignored_groups.add(thread.id)
                else:
                    print(f"[-] Error replying in {thread.thread_title}: {e}")

def main():
    api = login()
    while True:
        check_group_and_reply(api)
        time.sleep(2)

if __name__ == '__main__':
    main()
