from aiogram import Bot, Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

import re

router = Router()

class waiting(StatesGroup):
    waiting_word = State()

def validate_russian_word(word: str) -> bool:
    pattern = r'^[а-яёА-ЯЁ]+$'
    return bool(re.match(pattern, word))

@router.callback_query(F.data == "share")
async def share_world(callback: CallbackQuery, state: FSMContext, ):
    await state.set_state(waiting.waiting_word)
    await callback.message.delete()
    await callback.message.answer("Введите слово для друга:")

# Обработчик для получения слова от пользователя
@router.message(waiting.waiting_word, F.text)
async def process_word(message: Message, state: FSMContext, bot: Bot):
    word = message.text.strip()
    
    # Валидация слова
    if not validate_russian_word(word):
        await message.answer(
            "❌ Неверный формат!\n"
            "Пожалуйста, введите слово, состоящее только из русских букв.\n"
            "Пример: привет, дом, солнце"
        )
        return  # Не сбрасываем состояние, чтобы пользователь мог попробовать снова
    
    # Проверка длины слова (опционально)
    if len(word) < 2:
        await message.answer(
            "❌ Слишком короткое слово!\n"
            "Введите слово длиной от 2 букв."
        )
        return
    
    if len(word) > 8:
        await message.answer(
            "❌ Слишком длинное слово!\n"
            "Введите слово длиной до 9 букв."
        )
        return
    
    # Сохраняем слово в состоянии
    await state.update_data(chosen_word=word)
    
    # Создаем глубокую ссылку
    ref_link = await create_start_link(
        bot=bot, 
        payload=word,
        encode=True
    )
    
    await message.answer(
        f"✅ Отлично! Слово для друга: <b>{word}</b>\n\n"
        f"🔗 Ваша ссылка:\n<code>{ref_link}</code>\n\n"
        f"Отправьте эту ссылку другу!",
        parse_mode="HTML",
    )
    
    # Сбрасываем состояние
    await state.clear()

# Обработчик для некорректного ввода (не текст)
@router.message(waiting.waiting_word)
async def process_invalid_input(message: Message, state: FSMContext):
    await message.answer(
        "❌ Пожалуйста, введите текстовое слово, состоящее только из русских букв.\n"
        "Пример: привет, солнце, радость"
    )

