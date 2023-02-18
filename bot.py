import telebot
from telebot import types
bot = telebot.TeleBot('6148105017:AAEqPdBYRg3z5K9RLq9AUbeRd1Y1e4L3nno')

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    help = types.KeyboardButton('Помощь')
    markup.add(help)
    bot.send_message(message.chat.id, 'Привет, это Telegram-Bot для проверки безопасности сайта\nВыбери команду для начала работы', reply_markup=markup)

bot.polling()
