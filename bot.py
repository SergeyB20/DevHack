from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from Forms import form
import pyzbar.pyzbar as pyzbar
import  cv2, ssl, re, requests, urllib.request
from data_base import data, good_url, bad_url



TOKEN = '6109652125:AAFkN7ksm37Rm3GPVlr3r9Z2R4luowzxwHU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
keyboard = types.ReplyKeyboardMarkup()
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

@dp.message_handler(state= form.type)
async def meny1(message: types.Message, state: FSMContext):
  text = message.text
  btn1 = types.KeyboardButton('меню')
  q = ReplyKeyboardMarkup().add(btn1)
  if text == 'меню':
    await bot.send_message(message.chat.id, f'Меню:\n\n🏎️проверка ссылки\n\n⚙️проверка QR', reply_markup=q)
    await form.meny.set()
  if text == 'проверка QR':
    await bot.send_message(message.chat.id, f'Пришли мне изображение QR-кода', reply_markup=q)
    await form.qr.set()
  if text == 'проверка ссылки':
    await bot.send_message(message.chat.id, f'отправь мне ссылку на проверку', reply_markup=q)
    await form.href.set()

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state= form.qr)
async def download_photo(message: types.Message):
    image = cv2.imread("qr_code.png")
    codes = pyzbar.decode(image)
    for code in codes:
        abra['url'] = code.data.decode("utf-8")

@dp.message_handler(state= form.href)
async def meny_fun(message: types.Message, state: FSMContext):
  url = message.text
  btn1 = types.KeyboardButton('меню')
  q = ReplyKeyboardMarkup().add(btn1)
  if url == 'меню':
    await bot.send_message(message.chat.id, f'Меню:\n\n🏎️проверка ссылки\n\n⚙️проверка QR', reply_markup=q)
    await form.meny.set()
  else:
    abra['url'] = url
    print(abra['url'])
    try:
        response = requests.get(abra['url'])
        if response.status_code == 200:
            rating = 5
        else:
            rating = rating - 1
    except requests.exceptions.RequestException:
        await bot.send_message(message.chat.id, f'неверный URL, попробуйте ввести еще раз')
        await form.href.set()
    try:
        ssl_cert = ssl.get_server_certificate((abra['url'], 443))
        print(ssl_cert)
        await bot.send_message(message.chat.id, 'SSL сертификат для ссылки {} присутствует.'.format(abra['url']))
    except urllib.request.HTTPError:
        await bot.send_message(message.chat.id, 'SSL сертификат для ссылки {} отсутствует.'.format(abra['url']))
        rating = rating - 1
    finally:
        r = requests.get(abra['url'])
        if r.history:
            await bot.send_message(message.chat.id, 'Запрос был перенаправлен')
            for resp in r.history:
                print(resp.status_code, resp.url)
            abra['lastpos'] = r.status_code, r.url
            await form.end.set()
        else:
            rating = rating - 1
            await bot.send_message(message.chat.id, 'Запрос не был перенаправлен')
            await form.end.set()
        if rating == 2:
            btn1 = types.KeyboardButton('меню')
            q = ReplyKeyboardMarkup().add(btn1)
            await bot.send_message(message.chat.id, f'К сожалению ссылка не прошла проверку на безопасность :(\n Рейтинг: {rating}/5⭐️', reply_markup=q)
            bad_url.append(abra['url'])
            await form.meny.set()
        if rating > 2:
            btn1 = types.KeyboardButton('меню')
            q = ReplyKeyboardMarkup().add(btn1)
            await bot.send_message(message.chat.id, f'Ура! Ссылка прошла проверку и оказалась безопасной, теперь можно спокойно переходить по ней!\n Рейтинг: {rating}/5⭐️ ', reply_markup=q)
            good_url.append(abra['url'])
            await form.meny.set()
executor.start_polling(dp) 
