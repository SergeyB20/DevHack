from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from Forms import form
import pyzbar.pyzbar as pyzbar
import  cv2, ssl, re, requests, urllib.request
from data_base import data, good_url, bad_url
from pyzbar.pyzbar import decode
from PIL import Image


TOKEN = '6109652125:AAFkN7ksm37Rm3GPVlr3r9Z2R4luowzxwHU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
rating = 5
abra = {}


@dp.message_handler(commands=['start'])
async def get_text_messages(message: types.Message, state: FSMContext):
    btn = types.KeyboardButton(text='меню')
    keyboard.add(btn)
    await bot.send_message(message.chat.id, '👋Привет! Я телеграмм-бот🤖, который проверяет ссылки и QR-коды на безопасность, что бы начать со мной рабоать напиши в чат «меню»❤️', reply_markup=keyboard)
    await form.meny.set()

@dp.message_handler(state= form.meny)
async def meny2(message: types.Message, state: FSMContext):
  text = message.text
  if text == 'меню':
    btn1 = types.KeyboardButton('проверка ссылки')
    btn2 = types.KeyboardButton('проверка QR')
    q = ReplyKeyboardMarkup().add(btn1, btn2)
    await bot.send_message(message.chat.id, f'Меню:\n\n🏎️проверка ссылки\n\n⚙️проверка QR', reply_markup=q)
    await form.type.set()
    executor.start_polling(dp) 
