import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters import Text
from weather.weatherBot import weather_from_Bot
from news.newsBot import check_for_new_news
from dotenv import load_dotenv
import os

CITY = ''
fresh_news = ''
news_fresh = {}



load_dotenv()
bot = Bot(token=os.getenv('TG_BOT_TOKEN'))
dispatcher_tgb = Dispatcher(bot)

cb_ikb_b_choose_city = CallbackData('pref1', 'action1')
ikb_b_choose_city = InlineKeyboardMarkup(row_width=2)
ikb_b_choose_city_button1 = InlineKeyboardButton(text='Санкт-Петербург?', callback_data=cb_ikb_b_choose_city.new('wthr_SPb'))
ikb_b_choose_city_button2 = InlineKeyboardButton(text='Другой?', callback_data=cb_ikb_b_choose_city.new('wthr_other'))
ikb_b_choose_city_button3 = InlineKeyboardButton(text= 'Начало!', callback_data=cb_ikb_b_choose_city.new('wthr_start'))
ikb_b_choose_city.add(ikb_b_choose_city_button1, ikb_b_choose_city_button2).add(ikb_b_choose_city_button3)

cb_ikb_b_type_news = CallbackData('pref2','action2')
ikb_b_type_news = InlineKeyboardMarkup()
ikb_b_type_news_button1 = InlineKeyboardButton(text='Свежие новости?', callback_data=cb_ikb_b_type_news.new('nws_fresh'))
ikb_b_type_news_button2 = InlineKeyboardButton(text='Последние 5 новостей?', callback_data=cb_ikb_b_type_news.new('nws_five'))
ikb_b_type_news_button3 = InlineKeyboardButton(text='Все новости!', callback_data=cb_ikb_b_type_news.new('nws_all'))
ikb_b_type_news.add(ikb_b_type_news_button1, ikb_b_type_news_button2).add(ikb_b_type_news_button3)

kb_b_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_b_start_button1 = KeyboardButton('Погода!')
kb_b_start_button2 = KeyboardButton('Новости!')
kb_b_start_button3 = KeyboardButton('Закончить работу!')
kb_b_start.add(kb_b_start_button1).insert(kb_b_start_button2).add(kb_b_start_button3)

async def on_startup(_):
    print('запущен')

@dispatcher_tgb.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id = message.chat.id ,text='Добро пожаловать в наш телеграмм бот!',  reply_markup=kb_b_start)

@dispatcher_tgb.message_handler(Text(equals='Погода!'))
async def weather_command(message: types.Message):
    await bot.send_message(chat_id = message.chat.id, text = 'В каком городе вы хотите посмотеть погоду?', reply_markup = ikb_b_choose_city)

@dispatcher_tgb.message_handler(Text(equals='Закончить работу!'))
async def weather_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='*_*')
    await bot.send_message(chat_id=message.chat.id, text=f'Goodbye!\n/start', parse_mode='HTML')

@dispatcher_tgb.message_handler(Text(equals='Новости!'))
async def what_news(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Что вы хотите почитать?', reply_markup=ikb_b_type_news)


@dispatcher_tgb.callback_query_handler(cb_ikb_b_type_news.filter())
async def what_news(callback: types.CallbackQuery, callback_data: dict):
    with open('news/news_dict.json') as file:
        all_news = json.load(file)
        global fresh_news
        global news_fresh
    if callback_data['action2'] == 'nws_fresh':
        await callback.message.delete()
        fresh_news = check_for_new_news()
        if fresh_news is not None:
            for k, v in sorted(fresh_news.items()):
                news_fresh = f"<b>{v['date_time']}</b>\n{hlink(v['articl_title'], v['articl_url'])}"
                await callback.message.answer(news_fresh, reply_markup=kb_b_start, parse_mode='html')
        else:
            await callback.message.answer('Нет свежих новостей!(', reply_markup=kb_b_start)
    elif callback_data['action2'] == 'nws_all':
        await callback.message.delete()
        for k, v in sorted(all_news.items()):
            news_all = f"<b>{v['date_time']}</b>\n{hlink(v['articl_title'], v['articl_url'])}"
            await callback.message.answer(news_all, reply_markup=kb_b_start, parse_mode='html')
    elif callback_data['action2'] == 'nws_five':
        await callback.message.delete()
        for k, v in sorted(all_news.items())[-5:]:
            news_five = f"<b>{v['date_time']}</b>\n{hlink(v['articl_title'], v['articl_url'])}"
            await callback.message.answer(news_five, reply_markup=kb_b_start, parse_mode='html')
    # except:
    #     await callback.message.answer('Технические неполадки у сайта!(')

@dispatcher_tgb.callback_query_handler(cb_ikb_b_choose_city.filter())
async def what_city(callback: types.CallbackQuery, callback_data: dict):
    global CITY
    if callback_data['action1'] == 'wthr_SPb':
        await callback.message.delete()
        CITY = 'Санкт-Петербург'
        await callback.message.answer(weather_from_Bot(CITY), reply_markup=kb_b_start)
    elif callback_data['action1'] == 'wthr_other':
        await callback.message.delete()
        await callback.message.answer(text='Введите город, в котором хотите посмотреть погоду:')
        @dispatcher_tgb.message_handler()
        async def new_city(message: types.Message):
            global CITY
            CITY = message.text
            await callback.message.answer(weather_from_Bot(CITY), reply_markup=kb_b_start)
    elif callback_data['action1'] == 'wthr_start':
        await callback.message.delete()
        await callback.message.answer(text='Добро пожаловать в наш телеграмм бот!',  reply_markup=kb_b_start)


if __name__ == '__main__':
    executor.start_polling(dispatcher_tgb, on_startup = on_startup, skip_updates=True)
