from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from random import randrange
from pathlib import Path
from gtts import gTTS
import os


words = ['אבא','אימא','אוניברסיטה','ביולוגיה','בית ספר','גאוגרפיה','היסטוריה','טלוויזיה','טלפון','ים','מוזיאון','מורה',
'מתמטיקה','סטודנט','סטודנטית','פסיכולוגיה','פיזיקה','פילוסופיה','קפטריה','תלמיד','תלמידה','מבוגר','צרפת','ספרד','רוסיה','ישראל']


class Words(StatesGroup):
    word = State()


async def get_word(message: types.Message, state=FSMContext):
    if message.text.lower() != 'слова':
        data = await state.get_data()
        if message.text == data['word']:
            await bot.send_message(message.from_user.id, "Верно!")
        else:
            await bot.send_message(message.from_user.id, f"Неверно. Правильно: {data['word']}")
    await bot.send_message(message.from_user.id, 'Как пишется следующее слово?', reply_markup=ReplyKeyboardRemove())
    word_audio = speak(message.from_user.id)
    audio, word, path = word_audio[0], word_audio[1], word_audio[2]
    await bot.send_audio(message.from_user.id, audio)
    os.remove(path)
    await Words.word.set()
    async with state.proxy() as data:
        data['word'] = word
    await bot.send_message(message.from_user.id, '(Для выхода в главное меню нажмите /stop)')


def speak(id):
    word = words[randrange(len(words))]
    my_audio = gTTS(text=word, lang='iw')
    script_dir = Path(__file__).parent
    dir_path = (script_dir / f"words_audio/{id}").resolve()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_name = f"word.mp3"
    path = (dir_path / file_name).resolve()
    my_audio.save(path)
    phrase = open(path, 'rb')
    return phrase, word, path


def register_handlers_words(dp: Dispatcher):
    dp.register_message_handler(get_word, lambda msg: msg.text.lower() == 'слова')
    dp.register_message_handler(get_word, state=Words.word)