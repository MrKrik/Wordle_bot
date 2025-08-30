from aiogram import Bot, Dispatcher, Router
from aiogram import types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import random
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from main import bot
from kb import start_kb
router = Router()

# WRONG = "🟥"
# СORRECT = "🟩"
# MISS = "🟨"
# CLEAR = "⬜️"

class Game(StatesGroup):
    in_game = State()

@router.callback_query(F.data == "start_game")
async def start_game(callback: CallbackQuery | None, state: FSMContext | None, world: str = None, msg: Message = None, world_lenght: int = None):
    
    if world == None:
        world = generate_world(world_lenght=world_lenght)

    if callback != None:
        await callback.message.delete()

    game_text = "⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️ \n⬜️⬜️⬜️⬜️⬜️"
    if msg != None:
        game_msg = await msg.answer(game_text, reply_markup=start_kb.again_kb())
    else:
        game_msg = await callback.message.answer(game_text, reply_markup=start_kb.again_kb())

    await state.set_state(Game.in_game)

    await state.update_data(move=0)
    await state.update_data(world=world)
    await state.update_data(id=game_msg.message_id)
    await state.update_data(game_text=game_text)

    return

@router.message(Game.in_game)
async def game(message: types.Message, state: FSMContext):
    
    await message.delete()

    data = await state.get_data()

    

    result = compare_words(data["world"], message.text)
    result = ''.join(result)

    if data["move"] == 4 and result != "🟩🟩🟩🟩🟩":
        await state.clear()
        new_text = f"Вы проиграли ❌\n\nПравильное слово: {data["world"]}"
        await bot.edit_message_text(chat_id=message.chat.id,
                                 message_id=data['id'],
                                 text=new_text,
                                 reply_markup=start_kb.again_kb())
        return

    if result == "🟩🟩🟩🟩🟩":
        await state.clear()
        new_text = f"Вы выиграли ✔️\n\nПравильное слово: {data["world"]}"
        await bot.edit_message_text(chat_id=message.chat.id,
                                 message_id=data['id'],
                                 text=new_text,
                                 reply_markup=start_kb.again_kb())
        return

    game_message :str = data["game_text"]


    text = game_message.split(" ")
    text[data["move"]] = f"{message.text}\n{result}\n"
    new_text = ' '.join(text)

    await state.update_data(move=data["move"]+1)
    await state.update_data(game_text=new_text)

    await bot.edit_message_text(chat_id=message.chat.id,
                                 message_id=data['id'],
                                 text=new_text,
                                 reply_markup=start_kb.again_kb())

def compare_words(secret: str, guess: str) -> list[tuple[str, int]]:
    """
    Сравнивает предположение с загаданным словом по правилам Wordle.
    
    Возвращает список кортежей (буква, код):
    🟩 - буква на правильном месте (зеленый)
    🟨 - буква есть в слове, но в другой позиции (желтый)
    🟥 - буквы нет в слове (красный)
    """
    secret = secret.lower()
    guess = guess.lower()
    if len(secret) != len(guess):
        return "LEN"
    result = []
    secret_list = list(secret)
    guess_list = list(guess)
    for i in range(len(guess_list)):
        if guess_list[i] == secret_list[i]:
            result.append(("🟩"))
            secret_list[i] = None  # Помечаем, чтобы не учитывать повторно
            guess_list[i] = None
        else:
            result.append("🟥")  # Временно, потом проверим желтые
    
    # Теперь проверим буквы, которые есть, но не на своих местах (1)
    for i in range(len(guess_list)):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            result[i] = ("🟨")
            secret_list[secret_list.index(guess_list[i])] = None  # Удаляем из доступных
    
    return result


def generate_world(world_lenght: int):
    with open(f"russian_worlds/{world_lenght}.txt", "r", encoding="utf-8") as file:
        words = file.read().splitlines()

    random_word = random.choice(words)

    return random_word

