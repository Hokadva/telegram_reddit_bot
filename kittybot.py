from telebot import TeleBot, types
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import traceback

from models import SuperUserDatabase, DatabaseSubreddits
from my_parsers import Parser
from log import response_image_error


load_dotenv()

token_crypt = os.getenv('token_crypt')
URL_crypt = os.getenv('URL_crypt')
key = os.getenv('key')
cypher = Fernet(key)

token = cypher.decrypt(token_crypt).decode()
URL = cypher.decrypt(URL_crypt).decode()

bot = TeleBot(token=token)


@bot.message_handler(commands=['add_subreddit'])
def add_subreddit(message):
    chat_id = message.chat.id
    
    if not is_admin(message):
        bot.send_message(chat_id, "У вас нет прав для этой команды!")
        return
    
    msg = bot.send_message(
        chat_id,
        "Введите имя сабреддита (без r/). Например: cat. Отмена - отправьте /cancel"
    )

    bot.register_next_step_handler(msg, process_subreddit_name_step)


def process_subreddit_name_step(message):
    chat_id = message.chat.id
    subreddit_name = message.text.strip()
    
    if subreddit_name.lower() == '/cancel':
        bot.send_message(chat_id, "Операция отменена")
        return
    
    try:
        SUBREDITDATABASE = DatabaseSubreddits('database')
        SUBREDITDATABASE.add_record(subreddit_name)
        
        bot.send_message(
            chat_id,
            f"Сабреддит r/{subreddit_name} успешно добавлен!"
        )
        
    except Exception as e:
        print(f"Ошибка: {e}")
        print(traceback.format_exc())
        bot.send_message(
            chat_id,
            f"Ошибка при добавлении: {e}\nПопробуйте еще раз"
        )


@bot.message_handler(commands=['remove_subreddit'])
def remove_subreddit(message):
    chat_id = message.chat.id

    if not is_admin(message):
        bot.send_message(chat_id, "У вас нет прав для этой команды!")
        return

    try:
        SUBREDITDATABASE = DatabaseSubreddits('database')
        subreddits = SUBREDITDATABASE.print_database()
        if subreddits == '':
            bot.send_message(chat_id, "В базе нет сабреддитов для удаления")
            return

        print_subreddits(message)
        msg = bot.send_message(
            chat_id,
            f"Введите имя сабреддита для удаления (без r/).\n"
            f"Отмена - отправьте /cancel",
            parse_mode='Markdown'
        )

        bot.register_next_step_handler(msg, process_remove_subreddit_step)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(chat_id, f"Ошибка при получении списка: {e}")


def process_remove_subreddit_step(message):
    chat_id = message.chat.id
    subreddit_name = message.text.strip()
    if subreddit_name.lower() == '/cancel':
        bot.send_message(chat_id, "Операция отменена")
        return
    
    try:
        SUBREDITDATABASE = DatabaseSubreddits('database')
        all_subreddits = SUBREDITDATABASE.print_database()
        if subreddit_name not in all_subreddits:
            bot.send_message(
                chat_id,
                f"Сабреддит r/{subreddit_name} не найден в базе!\n"
                f"Проверьте имя и попробуйте снова"
            )
            return
        SUBREDITDATABASE.remove_record(subreddit_name)
        bot.send_message(
            chat_id,
            f"Сабреддит r/{subreddit_name} успешно удален!"
        )

    except Exception as e:
        print(f"Ошибка: {e}")
        print(traceback.format_exc())
        bot.send_message(
            chat_id,
            f"Ошибка при удалении: {e}\nПопробуйте еще раз"
        )


@bot.message_handler(commands=['cancel'])
def cancel_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Нет активных операций для отмены")


def responce_image():
    parser = Parser(URL)
    image = parser.get_image()

    if image:
        return image
    else:
        response_image_error()
        image = parser.get_reserve_image()
        return image


def is_admin(message):
    nickname = message.from_user.username
    user_id = message.from_user.id
    SUPERUSERDATABASE = SuperUserDatabase('database')
    return SUPERUSERDATABASE.is_admin(nickname, user_id)


def create_keyboard(text):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for buttons in text:
        button = types.KeyboardButton(text=f'/{buttons}')
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    chat_id = chat.id
    text = ['kittens']

    if is_admin(message):
        text += [
            'add_subreddit', 'print_subreddits', 'remove_subreddit'
            ]

    keyboard = create_keyboard(text)
    bot.send_message(
        chat_id=chat_id,
        text=(f'Спасибо, что запустили меня {name} мурр. Я Кошко-бот.'
              'Посмотри фотографии которые я для тебя собрал, мурр'
            ),
        reply_markup=keyboard
        )


@bot.message_handler(commands=['print_subreddits'])
def print_subreddits(message):
    chat = message.chat
    chat_id = chat.id
    if not is_admin(message):
        bot.send_message(
            chat_id=chat_id, text='У вас нет прав для данной операции'
            )
        return False

    SUBREDDITDATABASE = DatabaseSubreddits('database')
    lst = SUBREDDITDATABASE.text_database()
    bot.send_message(text=f'Список сабредитов: {lst}', chat_id=chat_id)


@bot.message_handler(commands=['kittens'])
def kitty(message):
    chat = message.chat
    chat_id = chat.id
    image = responce_image()
    bot.send_photo(chat_id=chat_id, photo=image)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(
        chat_id=chat_id,
        text=('Я Кошко-бот.'
              ' Посмотри фотографии которые я для тебя собрал, мурр'
            )
        )


def run_bot():
    print("Бот запущен...")
    bot.polling(non_stop=True)


if __name__ == '__main__':
    run_bot()
