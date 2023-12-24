from aiogram.utils import executor
from create_bot import dp
from handlers import verbs, letters, translate, words, milon, other


async def on_startup(_):
    print('Бот онлайн. Всё ок')


other.register_handlers_cancel(dp)
verbs.register_handlers_verbs(dp)
letters.register_handlers_letters(dp)
translate.register_handlers_translate(dp)
words.register_handlers_words(dp)
# milon.register_handlers_milon(dp)
other.register_handlers_other(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)