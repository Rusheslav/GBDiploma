from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

verbs_button = KeyboardButton('Глаголы')
letters_button = KeyboardButton('Буквы')
translate_button = KeyboardButton('Перевод')
words_button = KeyboardButton('Слова')
milon_button = KeyboardButton('Словарь')

menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.row(milon_button, verbs_button).row(letters_button, words_button).row(translate_button)