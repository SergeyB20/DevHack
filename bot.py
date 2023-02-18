import telebot
from telebot import types
import  ssl,requests, urllib.request
from pyzbar.pyzbar import decode
import cv2
from io import BytesIO
from PIL import Image



bot = telebot.TeleBot('6148105017:AAEqPdBYRg3z5K9RLq9AUbeRd1Y1e4L3nno')
@bot.message_handler(commands=['start']) 
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id, '👋Привет! Я телеграмм-бот🤖, который проверяет ссылки и QR-коды на безопасность, что бы начать со мной работать просто напиши свою ссылку❤️', reply_markup=markup)

@bot.message_handler(content_types=["photo"])
def decrypting(message):  
	
 

    
            

@bot.message_handler(content_types=['text'])
def check(message):
    url = message.text
    try:
        response = requests.get(url)
        if response.status_code == 200:
            rating = 5
        else:
            rating = rating - 1
            c = 1
    except requests.exceptions.RequestException:
        bot.send_message(message.chat.id, f'неверный URL, попробуйте ввести еще раз')
        
    try:
        r = requests.get(url)
        if (str(r.history)) == ('[<Response [302]>]'):
            bot.send_message(message.chat.id, 'Запрос был перенаправлен')
            rating = rating - 1
        else:
            
            bot.send_message(message.chat.id, 'Запрос не  был перенаправлен')
            
        if rating == 2:
           
            
            bot.send_message(message.chat.id, f'К сожалению ссылка не прошла проверку на безопасность :(\n Рейтинг: {rating}/5⭐️')
            if a == 1:
             bot.send_message(message.chat.id, 'Отсутствует SSL Сертификат')
            if b == 1:
                bot.send_message(message.chat.id, 'Ваш запрос был перенаправлен')
            if c == 1:
                bot.send_message(message.chat.id, 'Отсутствует поддержка HTTPS')
        if rating > 2:
            
            
            bot.send_message(message.chat.id, f'Ура! Ссылка прошла проверку и оказалась безопасной, теперь можно спокойно переходить по ней!\n Ваша ссылка прошла проверок - {rating}/5⭐️ ')
    except:
        print(1)
            
                
bot.polling()