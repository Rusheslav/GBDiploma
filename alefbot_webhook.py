import logging
from aiogram.utils.executor import start_webhook
from create_bot import dp, bot
from handlers import verbs, letters, translate, words, milon, other

# webhook settings
WEBHOOK_HOST = f'https://alefbet.ru'
WEBHOOK_PATH = f'/alefbot/alefbot_webhook.py'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = '3001'

async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print('Бот онлайн')

async def on_shutdown(dispatcher):
    await bot.delete_webhook()


other.register_handlers_cancel(dp)
verbs.register_handlers_verbs(dp)
letters.register_handlers_letters(dp)
translate.register_handlers_translate(dp)
words.register_handlers_words(dp)
milon.register_handlers_milon(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
