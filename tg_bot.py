import json
import traceback
import time
from json import JSONDecodeError
import random

import requests
import telebot  # pip install PyTelegramBotAPI
from threading import Thread
from datetime import datetime, timedelta

api_key_tg = ""
bot = telebot.TeleBot(api_key_tg)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.send_message(message.chat.id, "Что делаем?")
    except:
        traceback.print_exc()
        pass


@bot.message_handler(commands=['test'])
def start_message(message):
    try:
        bot.send_message(message.chat.id, "Я жив")
    except:
        traceback.print_exc()
        pass


@bot.message_handler(commands=['close'])
def start_message(message):
    global closed
    try:
        if message.chat.id == admin:
            if closed:
                closed = False
                bot.send_message(message.chat.id, "Открыто")
            elif not closed:
                closed = True
                bot.send_message(message.chat.id, "Закрыто")
        else:
            bot.send_message(message.chat.id, "Нет доступа")
    except:
        traceback.print_exc()
        pass


def send_text_message(message, text):
    for mes in message:
        if not closed:
            bot.send_message(mes, text, parse_mode='Markdown')
        else:
            if mes == admin:
                bot.send_message(mes, text, parse_mode='Markdown')


def bot_polling():
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        traceback.print_exc()
        time.sleep(60)


op = Thread(target=bot_polling, args=())
op.start()

closed = True
message = []
admin = 0
