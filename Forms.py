
from aiogram.dispatcher.filters.state import StatesGroup, State

class form(StatesGroup):
  start = State()
  meny = State()
  type = State()
  qr = State()
  url_func = State()
  href = State()
  checking = State()
  checking1 = State()
  checking2 = State()
  end = State()
