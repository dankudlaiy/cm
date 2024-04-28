from aiogram import Router, F
from aiogram.types import (Message, CallbackQuery)
from common import bot, soup

default_router = Router()


@default_router.message(F.text == '/start')
async def start(msg: Message):
    table = soup.find('table', attrs={'class': 'table'})
    rows = table.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [element.text.strip() for element in cols]
        data.append(cols)

    for item in data:
        print(item)

    await bot.send_message(msg.chat.id, "table been parsed !")
