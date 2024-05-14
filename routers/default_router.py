from aiogram import Router, F
from aiogram.types import (Message, CallbackQuery)
from aiogram.fsm.context import FSMContext
from aiogram import types

from callbacks.age_choice_callback import AgeChoiceCallback
from callbacks.area_choice_callback import AreaChoiceCallback
from callbacks.sex_choice_callback import SexChoiceCallback
from common import bot, parsing_service, visualization_service
from helpers.area_mapper import to_country_name
from helpers.states import States

default_router = Router()


@default_router.message(F.text == '/test')
async def test(msg: Message):
    url = (
        'https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS=00&areatype=state&cancer=001'
        '&race=00&sex=0&age=001&year=1&type=incd&sortVariableName=rate&sortOrder=default&output=0#results')

    data = await parsing_service.parseUrl(url)

    input_file = await visualization_service.formPieChart(data)

    await bot.send_photo(msg.chat.id, input_file)


@default_router.message(F.text == '/start')
async def start(msg: Message):
    buttons = [[types.InlineKeyboardButton(text='start', callback_data='start')]]

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.send_message(msg.chat.id,
                           'welcome to cancer stats visualizer !\nall data has been taken from '
                           'www.statecancerprofiles.cancer.gov',
                           reply_markup=markup)


@default_router.callback_query(lambda call: call.data == 'start')
async def start(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.area_choice)

    buttons = [[types.InlineKeyboardButton(text='United States', callback_data=AreaChoiceCallback(id='00').pack())],
               [types.InlineKeyboardButton(text='California', callback_data=AreaChoiceCallback(id='06').pack()),
                types.InlineKeyboardButton(text='Florida', callback_data=AreaChoiceCallback(id='12').pack()),
                types.InlineKeyboardButton(text='Texas', callback_data=AreaChoiceCallback(id='48').pack())],
               [types.InlineKeyboardButton(text='New York', callback_data=AreaChoiceCallback(id='36').pack()),
                types.InlineKeyboardButton(text='Pennsylvania', callback_data=AreaChoiceCallback(id='42').pack()),
                types.InlineKeyboardButton(text='Illinois', callback_data=AreaChoiceCallback(id='17').pack())]]

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(text='choose area', chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=markup)


@default_router.callback_query(AreaChoiceCallback.filter())
async def sex_filter(call: CallbackQuery, callback_data: AreaChoiceCallback, state: FSMContext):
    area_id = callback_data.id

    await state.set_state(States.sex_choice)
    await state.update_data(area_id=area_id)

    buttons = [[types.InlineKeyboardButton(text='Males', callback_data=SexChoiceCallback(id=1).pack()),
                types.InlineKeyboardButton(text='Females', callback_data=SexChoiceCallback(id=2).pack())],
               [types.InlineKeyboardButton(text='Both Sexes', callback_data=SexChoiceCallback(id=0).pack())]]

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(text='choose sex filter', chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=markup)


@default_router.callback_query(SexChoiceCallback.filter())
async def age_filter(call: CallbackQuery, callback_data: SexChoiceCallback, state: FSMContext):
    sex_filter = callback_data.id

    await state.set_state(States.age_choice)
    await state.update_data(sex_filter=sex_filter)

    buttons = [[types.InlineKeyboardButton(text='<50', callback_data=AgeChoiceCallback(id='009').pack()),
                types.InlineKeyboardButton(text='50+', callback_data=AgeChoiceCallback(id='136').pack()),
                types.InlineKeyboardButton(text='<65', callback_data=AgeChoiceCallback(id='006').pack()),
                types.InlineKeyboardButton(text='65+', callback_data=AgeChoiceCallback(id='157').pack())],
               [types.InlineKeyboardButton(text='All ages', callback_data=AgeChoiceCallback(id='001').pack())]]

    markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await bot.edit_message_text(text='choose age filter', chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=markup)


@default_router.callback_query(AgeChoiceCallback.filter())
async def for_chart(call: CallbackQuery, callback_data: AgeChoiceCallback, state: FSMContext):
    data = await state.get_data()

    area_id = data.get('area_id')
    sex_filter = data.get('sex_filter')

    age_filter = callback_data.id

    areatype = 'county'
    year = ''
    ignore_area = to_country_name(area_id)

    if area_id == '00':
        areatype = 'state'
        year = '&year=0'
        ignore_area = None

    url = (
        f'https://www.statecancerprofiles.cancer.gov/incidencerates/index.php?stateFIPS={area_id}&areatype={areatype}&cancer=001'
        f'&race=00&sex={sex_filter}&age={age_filter}{year}&type=incd&sortVariableName=rate&sortOrder=default&output=0#results')

    await bot.send_message(call.message.chat.id, f'trying to parse {url}')

    data = await parsing_service.parseUrl(url, ignore_area)

    sex_caption = ''
    age_caption = ''

    if sex_filter == 1:
        sex_caption = '(Males)'
    elif sex_filter == 2:
        sex_caption = '(Females)'

    if age_filter == '009':
        age_caption = '<50'
    elif age_filter == '136':
        age_caption = '50+'
    elif age_filter == '006':
        age_caption = '<65'
    elif age_filter == '157':
        age_caption = '65+'

    caption = f'Average United Stated Annual Incidence by state {sex_caption} {age_caption}'

    if ignore_area:
        caption = f'Average {ignore_area} Annual Incidence by country {sex_caption} {age_caption}'

    input_file = await visualization_service.formPieChart(data, caption)

    await bot.send_photo(call.message.chat.id, input_file)
