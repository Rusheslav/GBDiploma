from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from random import randrange
from pathlib import Path


otiyot = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ך', 'ל', 'מ', 'ם', 'נ', 'ן', 'ס', 'ע', 'פ', 'ף', 'צ', 'ץ', 'ק', 'ר', 'ש', 'ת']


class Letters(StatesGroup):
    letter = State()


async def get_letter(message: types.Message, state=FSMContext):
    if message.text.lower() != 'буквы':
        data = await state.get_data()
        if message.text == data['ot']:
            await bot.send_message(message.from_user.id, "Верно!")
        else:
            await bot.send_message(message.chat.id, f"Неверно. Правильно: {data['ot']}")
    await bot.send_message(message.from_user.id, 'Какой печатной букве соответвтует следующее написание?', reply_markup=ReplyKeyboardRemove())
    letters = choose_ot()
    img, ot = letters[0], letters[1]
    await bot.send_photo(message.from_user.id, img)
    await Letters.letter.set()
    async with state.proxy() as data:
        data['ot'] = ot
    await bot.send_message(message.from_user.id, '(Для выхода в главное меню нажмите /stop)')


def choose_ot():
    i = randrange(len(otiyot))
    script_dir=Path(__file__).parent
    rel_path = f"letters_album/{i+1}.png"
    path = (script_dir / rel_path).resolve()
    pic = open(path, 'rb')
    ot = otiyot[i]
    return pic, ot


def register_handlers_letters(dp: Dispatcher):
    dp.register_message_handler(get_letter, lambda msg: msg.text.lower() == 'буквы')
    dp.register_message_handler(get_letter, state=Letters.letter)