from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
import translators as ts
from gtts import gTTS
import os
from pathlib import Path


HEB = 'פםןוטארקףךלחיעכגדשץתצמנהבסז'
RUS = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
ENG = 'abcdefghijklmnopqrstuvwxyz'


class Translate(StatesGroup):
    phrase = State()


async def greet_translate(message: types.Message):
    await bot.send_message(message.from_user.id, 'Режим "Переводчик". Напишите фразу на русском, английском или иврите.', reply_markup=ReplyKeyboardRemove())
    await message.delete()
    await Translate.phrase.set()
    await bot.send_message(message.from_user.id, '(Для выхода в главное меню нажмите /stop)')


async def get_phrase(message: types.Message, state=FSMContext):
    phrase = message.text
    try:
        audio_info = transl(phrase, message.from_user.id)
        translated_audio, audio_path, text = audio_info[0], audio_info[1], audio_info[2]
        await bot.send_message(message.from_user.id, text)
        await bot.send_audio(message.from_user.id, translated_audio)
        os.remove(audio_path)
    except:
        await bot.send_message(message.from_user.id, 'Ошибка ввода: не начинайте фразу для перевода с пробелов, цифр или знаков препинания. Фраза должна начинаться с буквы того языка, с которого будет осуществляться перевод')
    await bot.send_message(message.from_user.id, '(Для выхода нажмите /stop)')


def transl(text, id):
    msg = text.strip().lower()
    if msg[0] in HEB:
        from_language = 'iw'
        to_language = 'ru'
    elif msg[0] in RUS:
        from_language = 'ru'
        to_language = 'iw'
    elif msg[0] in ENG:
        from_language = 'en'
        to_language = 'iw'


    text = ts.google(msg, from_language=from_language, to_language=to_language)
    my_audio = gTTS(text=text, lang=to_language)
    script_dir = Path(__file__).parent
    dir_path = (script_dir / f"translate_audio/{id}").resolve()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_name = f"translation.mp3"
    path = (dir_path / file_name).resolve()
    my_audio.save(path)
    phrase = open(path, 'rb')
    return phrase, path, text


def register_handlers_translate(dp: Dispatcher):
    dp.register_message_handler(greet_translate, lambda msg: msg.text.lower() == 'перевод')
    dp.register_message_handler(get_phrase, state=Translate.phrase)