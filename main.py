import asyncio
from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button
from telethon.tl.functions.channels import JoinChannelRequest
import sqlite3

class CaptchaBotSolver:
    def __init__(self, api_id, api_hash, phone_number):
        self.client = TelegramClient(phone_number, api_id, api_hash)
        self.bot_db = "bot_database.db"
        self.load_bot_database()

    def load_bot_database(self):
        self.conn = sqlite3.connect(self.bot_db)
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS bots (username TEXT, method TEXT)''')
        self.conn.commit()

    def save_bot_info(self, username, method):
        self.c.execute("INSERT INTO bots (username, method) VALUES (?, ?)", (username, method))
        self.conn.commit()

    async def join_group_and_solve_captcha(self):
        await self.client.start()
        group_entity = await self.client.get_entity('https://t.me/LampMining')

        await self.client(JoinChannelRequest(channel=group_entity))
        await asyncio.sleep(5)

        async for message in self.client.iter_messages(group_entity, limit=10):
            if isinstance(message.reply_markup, Button):
                if len(message.reply_markup.rows) > 1 and len(message.reply_markup.rows[1]) > 1:
                    await self.client(Button.inline(2))
                    await asyncio.sleep(1)
                    break

        await self.client.run_until_disconnected()

if __name__ == '__main__':
    api_id = 'xxxxx'#conf info
    api_hash = 'xxxxx'#conf info
    phone_number = '+xxxxx'#conf info

    solver = CaptchaBotSolver(api_id, api_hash, phone_number)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(solver.join_group_and_solve_captcha())
