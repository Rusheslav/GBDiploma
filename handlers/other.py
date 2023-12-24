from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from keyboard import menu


async def cancel_handler(message: types.Message, state=FSMContext):  
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    await bot.send_message(message.from_user.id, 'Выберите режим обучения.', reply_markup=menu)
    await message.delete()

async def any_message(message : types.Message):
    await bot.send_message(message.from_user.id, 'Выберите режим обучения', reply_markup=menu)
    await message.delete()


def register_handlers_cancel(dp : Dispatcher):
    dp.register_message_handler(cancel_handler, state="*", commands='stop')
    dp.register_message_handler(any_message, commands='stop')

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(any_message)