from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 21243324       # Replace with your API ID
api_hash = '2454c2f08e4e0eb978f3d8c50de27019'   # Replace with your API Hash
phone = +918436018461  # Replace with your phone number
client = TelegramClient('telegram_scrapper.py', api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code you received: '))

def fetch_telegram_data():
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
                 offset_date=last_date,
                 offset_id=0,
                 offset_peer=InputPeerEmpty(),
                 limit=chunk_size,
                 hash=0
             ))

    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup:  # Only target groups
                groups.append(chat)
        except:
            continue

    print('Choose a group to scrape messages from:')
    i = 0
    for group in groups:
        print(str(i) + '- ' + group.title)
        i += 1

    g_index = input("Enter a number: ")
    target_group = groups[int(g_index)]

    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)

    print('Saving to file...')
    with open("members.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

    print('Members scraped successfully.')

fetch_telegram_data()
client.disconnect()
