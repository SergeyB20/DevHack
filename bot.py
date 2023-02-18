import telebot
from telebot import types
bot = telebot.TeleBot('6148105017:AAEqPdBYRg3z5K9RLq9AUbeRd1Y1e4L3nno')

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Menu = types.KeyboardButton('Меню')
    markup.add(Menu)
    bot.send_message(message.chat.id, '👋Привет! Я телеграмм-бот🤖, который проверяет ссылки и QR-коды на безопасность, что бы начать со мной работать нажми на кнопку «меню»❤️', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    if message.text == 'Меню': 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        Check = types.KeyboardButton('Проверить безопасность сайта')
        Help = types.KeyboardButton('Помощь')
        markup.add(Check, Help)   
        bot.send_message(message.from_user.id, "Выберите команду для продолжения работы", reply_markup=markup)  
    elif message.text == 'Проверить безопасность сайта':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        link = types.KeyboardButton('ссылка')
        qr = types.KeyboardButton('QR-CODE')
        markup.add(link, qr)  
        bot.send_message(message.from_user.id, "Выберите, как вы хотите проверить сайт", reply_markup=markup)
    elif message.text =='Помощь':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu = types.KeyboardButton('Меню')
        markup.add(menu)  
        bot.send_message(message.from_user.id, "Здравствуйте, это телеграм бот для првоерки сайтов - вы можете так а можете так а так и так", reply_markup=markup)
    

bot.polling()
