import json

from aiogram import Bot

from bs4 import BeautifulSoup

import requests

with open('appsettings.json', 'r') as f:
    config = json.load(f)

bot_settings = config['BotSettings']
bot = Bot(token=bot_settings['Token'])

url = config['ParseUrl']
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
