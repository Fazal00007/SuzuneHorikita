from telethon import TelegramClient, events
import requests
import io
from PIL import Image
from src import telethn as client
from src.events import register

@register(pattern="^/whatanime(.*)")
async def whatanime(event):
    
    if not event.reply_to_msg_id:
        await event.reply('Please reply to a photo or gif to use this command.')
        return

    
    reply = await event.get_reply_message()

    if not reply.photo and not reply.gif:
        await event.reply('Please reply to a photo or gif to use this command.')
        return

    if reply.photo:
        file = reply.photo[-1]
    else:
        file = reply.gif

    file_data = await client.download_media(file)

    image = Image.open(io.BytesIO(file_data))

    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)

    response = requests.post(
        'https://api.trace.moe/search',
        files={'image': buffer},
        headers={'Content-Type': 'multipart/form-data'}
    ).json()

    if response['result']:
        result = response['result'][0]
        await event.reply(f'Title: {result["anilist"]["title"]["romaji"]}\n'
                           f'Episode: {result["episode"]}\n'
                           f'Time: {result["from"]}-{result["to"]}\n'
                           f'Similarity: {result["similarity"]:.2%}\n'
                           f'MAL URL: https://myanimelist.net/anime/{result["anilist"]["id"]}')
    else:
        await event.reply('Sorry, I could not recognize this anime.')
