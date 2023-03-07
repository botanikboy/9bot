import logging
import os
import sys
import time

import requests

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

from dotenv import load_dotenv


load_dotenv()

my_token = os.getenv('TOKEN')
handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(
    handlers=[handler],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

URL = 'https://9gag.com/v1/group-posts/meme/default/type/hot'
HEADERS = {'user-agent': 'Mediapartners-Google'}

cached_page = []
cur = ''
bot_time = time.time()


def get_api_response(cursor: str):
    if cursor is None:
        cursor = ''
    try:
        url = URL + '?' + cur
        logging.info(f'Отправлен запрос URL: {url}')
        response = requests.get(url, headers=HEADERS)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    else:
        # print(response)
        data = response.json()
        return data


def get_page():
    global cur
    page = []
    data = get_api_response(cur)
    cur = data.get('data').get('nextCursor')
    for post in data.get('data').get('posts'):
        if all([
            post.get('type') == 'Photo',
            post.get('promoted') == 0,
        ]):
            page.append(post)
    return page


def get_new_image():
    global cached_page
    if not cached_page:
        cached_page = get_page()
    meme = cached_page[0].get('images').get('image700').get('url')
    title = cached_page[0].get('title')
    cached_page.pop(0)
    return meme, title


def new_meme(update, context):
    chat = update.effective_chat
    image, title = get_new_image()
    logging.info(f'отправляем мемас с адресом: {image}')
    buttons = ReplyKeyboardMarkup([
        ['/meme'],
        ], resize_keyboard=True)
    context.bot.send_photo(
        chat.id,
        image,
        caption=title,
        reply_markup=buttons,
        )


def say_hi(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    print(update.message.text)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}, я ботик, и я умею только в мемасики.'
        )


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    print(update.message.text)
    buttons = ReplyKeyboardMarkup([
        ['/meme'],
        ], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что включил меня, {name}! жми кнопку',
        reply_markup=buttons,
        )


def main():
    global bot_time, cur
    if time.time() - bot_time > 172800:
        cur = ''
    updater = Updater(token=my_token)
    try:
        updater.dispatcher.add_handler(CommandHandler('start', wake_up))
        updater.dispatcher.add_handler(CommandHandler('meme', new_meme))
        updater.dispatcher.add_handler(MessageHandler(Filters.all, say_hi))
        updater.start_polling(poll_interval=4.0)
        updater.idle()
    except Exception as error:
        logging.error(f'Error in bot: {error}')


if __name__ == '__main__':
    main()
