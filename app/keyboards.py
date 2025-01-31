from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup



main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Проверить IMEI'), KeyboardButton(text='API')],
        [KeyboardButton(text='Добавить пользователя')]
    ],
    resize_keyboard=True
)
