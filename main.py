import asyncio

from aiogram import Bot, Dispatcher
from aiogram import types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, FSInputFile
from kb import start_kb
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.fsm.context import FSMContext

from config import TOKEN
import logging
from handlers import game

logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filename="logs.txt"
    )
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router=game.router)
    await dp.start_polling(bot)

@dp.message(CommandStart(deep_link=True))
async def handler(message: Message, state: FSMContext, command: CommandObject):
    await message.delete()
    args = command.args
    payload = decode_payload(args)
    await game.start_game(callback = None, state = state ,world = payload, msg = message)

@dp.message(CommandStart())
async def start(message: Message):
    photo = FSInputFile("start.jpg")
    await bot.send_photo(reply_markup= start_kb.start_kb(),photo=photo, chat_id=message.chat.id)
    return

@dp.message(Command('w'))
async def ref(message: Message):
    ref = await create_start_link(bot, "Пизда", encode = True)
    await message.answer(ref)



if __name__ == '__main__':
    try:
        asyncio.run(main())   
    except KeyboardInterrupt:
        print("Nothing")    