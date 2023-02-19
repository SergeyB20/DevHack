from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
import requests
from fake_useragent import UserAgent
from PIL import Image
from pyzbar.pyzbar import decode
from PIL import Image
from Forms import form
from urllib.parse import urlparse 



TOKEN = '6109652125:AAFkN7ksm37Rm3GPVlr3r9Z2R4luowzxwHU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
rating = 5
abra = {}


@dp.message_handler(commands=['start'], state = form.type)
async def get_text_messages(message: types.Message, state: FSMContext):
    btn1 = types.KeyboardButton(text='проверка ссылки', resize_keyboard=True)
    btn2 = types.KeyboardButton(text='проверка QR', resize_keyboard=True)
    keyboard.add(btn1, btn2)
    await bot.send_message(message.chat.id, f'👋Привет, {message.from_user.username}! Я телеграмм-бот🤖, который проверяет ссылки и QR-коды на безопасность, что бы начать со мной работать выбери нужную команду', reply_markup=keyboard)
    await form.type.set()

@dp.message_handler(state= form.type)
async def meny1(message: types.Message, state: FSMContext):
  text = message.text
  if text == 'проверка QR':
    await bot.send_message(message.chat.id, f'Пришли мне изображение QR-кода')
    await form.qr.set()
  if text == 'проверка ссылки':
    await bot.send_message(message.chat.id, f'отправь мне ссылку на проверку')
    await form.href.set()
  if text == '/start':
    await form.start.set()
@dp.message_handler(content_types=["photo"], state= form.qr)
async def download_photo(message: types.Message):
 await message.photo[-1].download('img/am.jpg')
 try:
    
    decocdeQR = decode(Image.open('img/am.jpg'))
    a = (decocdeQR[0].data.decode('ascii'))
    await bot.send_message(message.chat.id, f'Вот ссылка вашего QR кода {a}, для дальнейшей работы отправте эту ссылку мне')
    await form.href.set()   
 except:
    await bot.send_message(message.chat.id,'Невозможно распознать qr, занова выберите нужное действие')
    await form.type.set()                  
@dp.message_handler(state= form.href)
async def meny_fun(message: types.Message, state: FSMContext):
  url = message.text
  btn1 = types.KeyboardButton('меню')
  q = ReplyKeyboardMarkup().add(btn1)
  if url == '/start':
    await form.start.set()
  abra['url'] = url
  print(abra['url'])
  await form.type.set()
  try:
        response = requests.get(abra['url'], headers={'User-Agent': UserAgent().chrome})
        parsed_url = urlparse(abra['url'])
        n  = len(parsed_url.netloc.split('.')) 
        if response.status_code == 200:
            global rating
            rating = 5
            a = '✅HTTPS доступно'
        else:
            rating = rating - 1
            a = '❌HTTPS Недоступно'
        try:
            r = requests.get(abra['url'], verify=True)
            ssl_cert = '✅Ссылка имеет SSL сертификат'
        except requests.exceptions.SSLError:
            rating -= 1
            ssl_cert = '❌Ссылка не имеет SSL сертификата'
        if n > 2:
                
                b = '❌Ссылка имеет подозрительные домена'
                rating -= 1
        else:
             b = '✅Ссылка не имеет подозрительные домена'
  except requests.exceptions.RequestException:
        await bot.send_message(message.chat.id, f'неверный URL, попробуйте ввести еще раз')
        await form.href.set()
  finally:
        r = requests.get(abra['url'], headers={'User-Agent': UserAgent().chrome})
        if r.history:
            rating = rating - 1
            rs =  '❌Запрос был перенаправлен'
            abra['lastpos'] = r.status_code, r.url
        else:
            rs =  '✅Запрос не был перенаправлен'
        if rating <= 2:
            btn1 = types.KeyboardButton(text='проверка ссылки',resize_keyboard=True)
            btn2 = types.KeyboardButton(text='проверка QR',resize_keyboard=True)
            q = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1,btn2)
            await bot.send_message(message.chat.id, f'Скорее всего эта ссылка не безопасна.\nХарактеристика:\n{a}\n{rs}\n{b}\n Рейтинг: {rating}/5⭐️', reply_markup=q)
            
            await form.type.set()
        if rating > 2:
            btn1 = types.KeyboardButton(text='проверка ссылки',resize_keyboard=True)
            btn2 = types.KeyboardButton(text='проверка QR',resize_keyboard=True)
            q = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1,btn2)
            await bot.send_message(message.chat.id, f'Отлично! Ссылка оказалась безопасной.\nХарактеристика:\n{ssl_cert}\n{a}\n{rs}\n{b}\n Рейтинг: {rating}/5⭐️ ', reply_markup=q)
            
            await form.type.set()
executor.start_polling(dp)