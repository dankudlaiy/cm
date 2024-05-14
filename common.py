import json

from aiogram import Bot

from services.parsing_service import ParsingService
from services.visualization_service import VisualizationService

with open('appsettings.json', 'r') as f:
    config = json.load(f)

bot_settings = config['BotSettings']
bot = Bot(token=bot_settings['Token'])

parsing_service = ParsingService()
visualization_service = VisualizationService()
