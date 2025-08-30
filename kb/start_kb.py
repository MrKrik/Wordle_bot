from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
def start_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Начать игру", callback_data=("start_game")))
    keyboard = builder.as_markup()
    return keyboard

def again_kb():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Новая игра", callback_data=("start_game")))
    keyboard = builder.as_markup()
    return keyboard