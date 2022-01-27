import os
import time
from unicodedata import name
import telebot
import sqlite3 as sl
from datetime import datetime
from telebot.types import Message
import threading
from pystray import MenuItem as item
import pystray
from PIL import Image

bot = telebot.TeleBot('5066423829:AAHBWY-zsULrIF3uDBeO30EQT_hIrHmBrd0', parse_mode=None) 

image = Image.open(r"d:\projects\IT\vlsu_project\src\icon.ico")


def time_now():
    dt = datetime.now()
    return(dt.strftime("%D | %H:%M"))
    
request = '''INSERT INTO users
            (id, name, reg_date, playcount, score)
            VALUES
            (?,?,?,?,?);'''

    

try:
    connection = sl.connect(r'd:\projects\IT\vlsu_project\src\test_base.db',check_same_thread=False)
    cursor = connection.cursor()
except sl.Error as err:
    print(err)


@bot.message_handler('start')
def start(message):
    try:
        print(message.from_user.id,message.from_user.username,time_now(),0,0)
        cursor.execute(request,(message.from_user.id,message.from_user.username,time_now(),0,0))
        answer = cursor.fetchall()
        print(answer)
        connection.commit()
    except:
        print('Пользователь существует!')
def close_app():
    #toaster.show_toast('Уведомление','Бот закрыт!',duration=3)
    icon.notify('Закрытие...')
    time.sleep(2)
    icon.remove_notification()
    os._exit(1)
def poll():
    while True:
        try:
            bot.polling()
        except:
            print('Невозможно подключиться к серверу Telegram')
            for i in range(15,0, -1):
                print('До рестарта {} секунд    '.format(i),end='\r')
                time.sleep(1)
def send_test(message):
    bot.send_message()
menu = pystray.Menu(item('Отправить сообщение администратору', send_test),item('Закрыть', close_app))
icon = pystray.Icon("GameBot", image, "GameBot", menu)
icon_thread = threading.Thread(target=icon.run, name='systray_thread')
poll_thread = threading.Thread(target=poll, name='polling_thread')
poll_thread.start()
icon_thread.start()
time.sleep(1)
icon.notify('Бот запущен!')
time.sleep(3)
icon.remove_notification()  