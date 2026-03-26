from telebot import TeleBot, types
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

from my_parsers import Parser
from log import response_image_error


load_dotenv()
token_crypt = os.getenv('token_crypt')
URL_crypt = os.getenv('URL_crypt')
key = os.getenv('key')
cypher = Fernet(key)

token = cypher.decrypt(token_crypt).decode()
bot = TeleBot(token=token)
URL = cypher.decrypt(URL_crypt).decode()


def responce_image():
    parser = Parser(URL)
    image = parser.get_image()

    if image:
        return image
    else:
        response_image_error()
        image = parser.get_reserve_image()
        return image


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    chat_id = chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_new_cat = types.KeyboardButton(text='/kittens')
    keyboard.add(button_new_cat)
    bot.send_message(
        chat_id=chat_id,
        text=(f'Спасибо, что запустили меня {name} мурр. Я Кошко-бот.'
              'Посмотри фотографии которые я для тебя собрал, мурр'
            ),
        reply_markup=keyboard
        )


@bot.message_handler(commands=['kittens'])
def kitty(message):
    chat = message.chat
    chat_id = chat.id
    image = responce_image()
    bot.send_photo(chat_id=chat_id, photo=image)


def run_bot():
    bot.polling()


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    print(message)
    chat_id = chat.id
    bot.send_message(
        chat_id=chat_id,
        text=('Я Кошко-бот.'
              ' Посмотри фотографии которые я для тебя собрал, мурр'
            )
        )


if __name__ == '__main__':
    run_bot()
