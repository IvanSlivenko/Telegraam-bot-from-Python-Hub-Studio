import asyncio
import aiohttp
from const import TOKEN, URL_TELEGRAM

url = f"{URL_TELEGRAM}{TOKEN}/"


async def send_message(chat_id, text):
    async  with aiohttp.ClientSession() as session:
        params = {'chat_id': chat_id, 'text': text}
        async with session.post(url + 'sendMessage',data=params) as response:
            await response.json()

async def handle_updates(update):
    message = update.get('message', False)
    if message:
        chat_id = message['chat']['id']
        text = message.get('text', False)
        if text:
            await send_message(chat_id,f'Ехо:{text}')
        else:
            await send_message(chat_id,'Я працюю лише з текстом')

async def get_updates():
    offset = None
    async with aiohttp.ClientSession() as session:
        while True:
            params = {'timeout': 10, 'offset': offset}
            async with session.post(url + 'getUpdates', data=params) as response:
                updates = await response.json()
                if len(updates['result']) > 0:
                    offset = updates['result'][-1]['update_id'] + 1
                    for update in updates['result']:
                        await handle_updates(update)

                        # for_print = update.copy()
                        # for_print['message']['from']['id'] = 1234567890
                        # for_print['message']['chat']['id'] = 9987654321
                        print(update)

async def main():
    await get_updates()

asyncio.run(main())