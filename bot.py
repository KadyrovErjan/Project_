from venv import create

import telebot
from telebot import types
from telebot.types import ReactionTypeEmoji
import random
from datetime import datetime
import qrcode
from io import BytesIO
from deep_translator import GoogleTranslator
import Calculator



bot_token = '7887163796:AAEo1LHI3yySB-EmLwm-HU3l6q8DyCw2VvY'
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start_command(message):
    if name:
        bot.send_message(message.chat.id, f"Привет {name}! "
                                          f"Рад тебя снова видеть!")
    else:
        bot.send_message(message.chat.id, "Привет! Давай познакомимся,"
                                          "напиши команду /name")

@bot.message_handler(commands=['qr'])
def generate_qr(message):
    bot.send_message(message.chat.id, "Отправьте текст для генерации QR-кода")

    bot.register_next_step_handler(message, create_qr)


def create_qr(message):
    text = message.text
    qr = qrcode.make(text)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    bot.send_photo(message.chat.id, buffer, caption="Вот ваш QR-код!")


@bot.message_handler(commands=['translate'])
def translate_text(message):
    bot.send_message(message.chat.id, 'Введите текст для перевода')
    bot.register_next_step_handler(message, perform_translation)


def perform_translation(message):
    text = message.text
    translator = GoogleTranslator(source='auto')
    translated = translator.translate(text)

    bot.send_message(message.chat.id, f"Перевод: {translated}")

@bot.message_handler(commands=['calculator'])
def calculator_command(message):
    bot.send_message(message.chat.id, "Введите математическое выражение для вычисления")
    bot.register_next_step_handler(message, calculator_result)

def calculator_result(message):
    expression = message.text
    try:
        result = eval(expression)
        bot.send_message(message.chat.id, f"Результат: {result}")
    except Exception :
        bot.send_message(message.chat.id, "Ошибка в выражении")

@bot.message_handler(commands=['game'])
def start_game(message):
    global random_number
    random_number = random.randint(1, 10)

    bot.send_message(message.chat.id, "Я загадал число от 1 до 10. Попробуй угадать!")
    bot.register_next_step_handler(message, guess_number)


def guess_number(message):
    global random_number
    try:
        guess = int(message.text)
        if guess == random_number:
            bot.send_message(message.chat.id, f"Поздравляю ты угадал🎉 \nэто было число {random_number}")
        else:
            bot.send_message(message.chat.id, "Не угадал попробуй еще раз!😢")
            bot.register_next_step_handler(message, guess_number)
    except ValueError:
        bot.send_message(message.chat.id, "Введи число от 1 до 10 !!!😤")
        bot.register_next_step_handler(message, guess_number)

@bot.message_handler(commands=['photo'])
def send_photo(message):
    with open('images/Era.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo=photo, caption="Вот тебе фото с моей памяти")


@bot.message_handler(content_types=["sticker"])
def get_sticker_id(message):
    sticker_id = message.sticker.file_id

    bot.send_message(message.chat.id, f"ID вашего стикера: {sticker_id}")


@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    sticker_id = "CAACAgIAAxkBAAIFs2dT380dSLBmP_B_R_-mti55RUvQAAJgVAAC-W-ASbABMD0-7eMhNgQ"
    bot.send_sticker(message.chat.id, sticker_id)


@bot.message_handler(commands=['time'])
def send_time(message):
    current_time = datetime.now().strftime('%H:%M:%S')

    bot.send_message(message.chat.id, f"Сейчас время: {current_time}")
    bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('🫡')], is_big=False)


@bot.message_handler(commands=['reverse'])
def reverse_text(message):
    bot.send_message(message.chat.id, "Напиши мне слово я его переверну!")
    bot.register_next_step_handler(message, reverse_handler)


def reverse_handler(message):
    reversed_text = message.text[::-1]
    bot.send_message(message.chat.id, f"Ваш текст наоборот:\n{str(reversed_text).lower()}")


@bot.message_handler(commands=['reset'])
def reset_data(message):
    global name, surname, age
    name, surname, age = '', '', 0
    bot.send_message(message.chat.id, "Ваши данные сброшены. Напишите /name, чтобы начать заново")


@bot.message_handler(commands=['info'])
def info_command(message):
    if name and surname and age:
        bot.send_message(message.chat.id, f"Вот что я знаю о тебе: "
                                          f"\nИмя: {name}\nФамилия: {surname}"
                                          f"\nВозраст: {age}")
    else:
        bot.send_message(message.chat.id, "Я пока мало знаю о тебе!"
                                          "напиши команду /name "
                                          "чтобы познакомится")


random_number = 0
name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/name':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю, напиши команду /name")


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)
    bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, "Цифрами пожалуйста")
            break
    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = f'Тебе {str(age)} лет, тебя зовут {name}, а фамилия {surname}?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        # сохраняем в базу данных и т.д…
        bot.send_message(call.message.chat.id, 'Хорошо я у себя записал!!!')

    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Напиши тогда снова команду /name 😲🙂‍↔️😇')


bot.polling(non_stop=True, interval=0)

