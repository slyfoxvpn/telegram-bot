import asyncio
import logging
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config_reader import config
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, reply_keyboard_markup


logging.basicConfig(level=logging.INFO) # Enable logging
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="Markdown") # Bot init
dp = Dispatcher() # Dispatcher (?)


# Main start function
async def start_main(message: Message, auth_id=None, ref_id=None):
    if auth_id:
        await message.answer(f"Auth with {auth_id}")
    elif ref_id:
        await message.answer(f"Ref from {ref_id}")
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=[
            [types.KeyboardButton(text="❔❓Как это сделать?")],
        ], resize_keyboard=True, input_field_placeholder="Денис денисочка")

        await message.answer("*Привет! На связи команда SlyFox.\nДавайте найдем ваш аккаунт.*")
        await message.answer("🦊", reply_markup=keyboard)


# Start functions dor sereval cases
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'auth_(\d+)')))) # Start with auth id
async def start_auth(message: Message, command: Command):
    auth_id = command.args.split("_")[1]
    await start_main(message, auth_id=auth_id)

@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'ref_(\d+)')))) # Start with ref id
async def start_ref(message: Message, command: Command):
    ref_id = command.args.split("_")[1]
    await start_main(message, ref_id=ref_id)

@dp.message(F.text, CommandStart())
async def start_default(message: types.Message): # Start for other cases
    await start_main(message)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())