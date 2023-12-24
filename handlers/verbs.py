from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from handlers.verbs_data import translate


class Verbs(StatesGroup):
    verb = State()


async def greet_verbs(message: types.Message):
    await bot.send_message(message.from_user.id, 'Режим "Словарь глаголов". Введите инфинитив на русском или иврите.', reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await Verbs.verb.set()
    await bot.send_message(message.from_user.id, '(Для выхода нажмите /stop)')


async def get_verbs(message: types.Message, state=FSMContext):
    verb = message.text.lower()
    try:
        reply = translate(verb)
        text, buttons = reply[0], reply[1]
        try:
            await bot.send_message(message.from_user.id, text, reply_markup=buttons)
        except:
            await bot.send_message(message.from_user.id, 'Кажется, вы допустили ошибку в написании. Попробуйте ещё раз')
    except:
        await bot.send_message(message.from_user.id, 'Произошла непредвиденная ошибка. Попробуйте ввести другое слово')
    await bot.send_message(message.from_user.id, '(Для выхода в главное меню нажмите /stop)')


def register_handlers_verbs(dp: Dispatcher):
    dp.register_message_handler(greet_verbs, lambda msg: msg.text.lower() == 'глаголы')
    dp.register_message_handler(get_verbs, state=Verbs.verb)
