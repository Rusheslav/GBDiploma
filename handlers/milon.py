from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from tabulate import tabulate
from handlers.dict import rus_heb


class Milon(StatesGroup):
    mila = State()


async def greet_milon(message: types.Message):
    await bot.send_message(message.from_user.id, 'Режим "Словарь". Введите слово (существительное, прилагательное, местоимение или числительное) на русском языке.', reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await Milon.mila.set()
    await bot.send_message(message.from_user.id, '(Для выхода нажмите /stop)')


async def get_mila(message: types.Message, state=FSMContext):
    mila = message.text.lower()
    await bot.send_message(message.from_user.id, translate(mila))
    await bot.send_message(message.from_user.id, '(Для выхода в главное меню нажмите /stop)')


def translate(msg):
    if "ё" in msg:
        msg = msg.replace("ё", "е")
    if msg in rus_heb.keys():
        reply = []
        for i in range(len(rus_heb[msg])):
            reply.append([rus_heb[msg][i][0]])
            reply.append([f'({rus_heb[msg][i][1]})'])
            reply.append([rus_heb[msg][i][2]])            
            if i != len(rus_heb[msg]) - 1:
                reply.append(['***'])
        return tabulate(reply, tablefmt = 'simple')
    return "Слово не найдено. Попробуйте другое слово"


def register_handlers_milon(dp: Dispatcher):
    dp.register_message_handler(greet_milon, lambda msg: msg.text.lower() == 'словарь')
    dp.register_message_handler(get_mila, state=Milon.mila)