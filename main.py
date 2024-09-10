from typing import Final
import asyncio
import telebot
from googleAPI import upload_file, get_disk_list, clear_disk
import telebot
from telebot import types # для указание типов
import os
from config import TOKEN, BOT_USERNAME
import json


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'C:/Users/Aleksey/PycharmProjects/FileUploaderBot/received/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Сохраняю файл")
    except Exception as e:
        bot.reply_to(message, e)
    try:
        link = upload_file(src)
        bot.reply_to(message, text=link)
        os.remove(src)
    except UnboundLocalError as e:
        print(e)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("? Список файлов")
    btn2 = types.KeyboardButton("❓ Удалить все файлы")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот для загрузки файлов на Googlee Disk".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "? Список файлов"):
        ls = get_disk_list()["files"]
        for i in ls:
            bot.send_message(message.chat.id, text=str(i["name"]))
    elif (message.text == "❓ Удалить все файлы"):
        clear_disk()
        bot.send_message(message.chat.id, text="Успешно")
    else:
        bot.send_message(message.chat.id, text="Команды не существует")


bot.polling(none_stop=True)