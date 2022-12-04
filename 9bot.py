import logging
import os
import sys
# import time

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
headers = {
    'user-agent': 'Mediapartners-Google',
}

cached_page = {}
sent_memes = []
last_meme = ''
cur = ''
timestamp = ''


def get_api_response():
    global cur, timestamp
    try:
        url = URL + '?' + cur
        logging.info(f'Отправлени запрос URL: {url}')
        response = requests.get(url, headers=headers)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    else:
        data = response.json()
        cur = data.get('data').get('nextCursor')
        timestamp = data.get('meta').get('timestamp')
        return data


def get_page():
    global cached_page, cur
    page = []
    if cached_page:
        if last_meme == cached_page[-1].get(
                'images').get('image700').get('url'):
            data = get_api_response()
            for post in data.get('data').get('posts'):
                if post.get('type') == 'Photo':
                    page.append(post)
            cached_page = page
            return page
        else:
            return cached_page
    else:
        data = get_api_response()
        for post in data.get('data').get('posts'):
            if post.get('type') == 'Photo':
                page.append(post)
        cached_page = page
        return page


def get_new_image():
    global last_meme, sent_memes
    page = get_page()
    for post in page:
        if (
            post.get('promoted') == 0
            and post.get('type') == 'Photo'
            and post.get(
                'images').get('image700').get('url') not in sent_memes
        ):
            meme = post.get('images').get('image700').get('url')
            title = post.get('title')
            last_meme = meme
            sent_memes.append(last_meme)
            return (meme, title)


def new_meme(update, context):
    chat = update.effective_chat
    image, title = get_new_image()
    logging.info(f'отправляем мемас с адресом: {image}')
    context.bot.send_photo(chat.id, image, caption=title)


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
    updater = Updater(token=my_token)
    try:
        updater.dispatcher.add_handler(CommandHandler('start', wake_up))
        updater.dispatcher.add_handler(CommandHandler('meme', new_meme))
        updater.dispatcher.add_handler(MessageHandler(Filters.all, say_hi))
        updater.start_polling(poll_interval=2.0)
        updater.idle()
    except Exception as error:
        logging.error(f'Error in bot: {error}')


if __name__ == '__main__':
    main()
