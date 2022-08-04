import telebot
from telebot import types
import settings
import os

bot = telebot.TeleBot(settings.TOKEN)


# бот для передачі файлів між телеграмом та сервером на якому знаходиться бот

# Стартовая команда
@bot.message_handler(commands=['start'])
def starter(message):
    if message.from_user.username in settings.ADMIN_LIST:
        bot.send_message(message.chat.id, "Бот працює!")
    else:
        print("Не адмін")


@bot.message_handler(commands=['send'])
def sender(message):
    if message.from_user.username in settings.ADMIN_LIST:
        bot.send_message(message.chat.id, "Відправте файл")
        bot.register_next_step_handler(message, sender_two)
    else:
        print("Не адмін")


def sender_two(message):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_id_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)
    src = file_name
    with open(settings.SAVE_DIR + "/" + src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, "Файл завантажено")


@bot.message_handler(commands=['load'])
def loader(message):
    if message.from_user.username in settings.ADMIN_LIST:
        bot.send_message(message.chat.id, "Вкажіть назву файлу")
        bot.register_next_step_handler(message, loader_two)
    else:
        print("Не адмін")


def loader_two(message):
    with open(settings.SAVE_DIR + '/' + message.text, "rb") as misc:
        file = misc.read()
    bot.send_document(message.chat.id, file, visible_file_name=message.text)


if __name__ == "__main__":
    bot.polling()
