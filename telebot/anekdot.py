from json import load
import telebot
import bs4
import requests
from gtts import gTTS
from telebot import types # для указание типов
bot = telebot.TeleBot("5311177854:AAEdXcRwgbbx4Mrd-d5Bk7nBiwpp-uYqX70")

# функция берёт анекдот с сайта и записывает его в переменную
def getanekdot():
    z=''
    s=requests.get('http://anekdotme.ru/random')
    b=bs4.BeautifulSoup(s.text, "html.parser")
    p=b.select('.anekdot_text')
    for x in p:        
        s=(x.getText().strip())
        z=z+s+'\n\n'
    return s
    
# Получаем анекдот и записываем его в аудио файл 
def play():
    anek=getanekdot()
    tts = gTTS(text=anek, lang='ru')  

    # преобразуем текст в речь, используя google-переводчик
    # и сохраняем получившеюся речь в mp3 файл
    tts.save('text.OGG')
    return open('text.OGG', 'rb'), anek


@bot.message_handler(content_types=["text"])
def handle_text(message):
    msg=message.text
    msg=msg.lower()
    # создаём кнопку, которая пишет слово Дай
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("дай")
    markup.add(btn1)
    if (u'дай' in msg):
        audio, anek=play()
        bot.send_voice(message.chat.id, audio)
        bot.send_message(message.chat.id, anek, reply_markup=markup)           
    else:
        bot.send_message(message.from_user.id, u'Напишите мне слово "Дай"', reply_markup=markup)

bot.polling(none_stop=True, timeout=123)
