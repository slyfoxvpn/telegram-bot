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


# 'start' with auth code (if exist)
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'auth_(\d+)'))))
async def cmd_start(message: Message, command: CommandObject):
    auth_id = command.args.split("_")[1]
    await message.answer(f"Auth with {auth_id}")


# 'start' with ref code (if exist)
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'ref_(\d+)'))))
async def cmd_start(message: Message, command: CommandObject):
    ref_id = command.args.split("_")[1]
    await message.answer(f"Ref from {ref_id}")


# 'start' default handler
@dp.message(F.text, CommandStart())
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="❔❓Как это сделать?")],
    ], resize_keyboard=True, input_field_placeholder="Денис денисочка")

    await message.answer("*Привет! На связи команда SlyFox.\nДавайте найдем ваш аккаунт.*")
    await message.answer("🦊", reply_markup=keyboard)


# Я хотел объединить это, но чет не работает
# @dp.message(CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'auth_(\d+)'))))
# async def cmd_start(message: types.Message, command: None):
#     if command and command.args:
#         auth_number = command.args.split("_")[1]
#         await message.answer(f"*Вы успешно авторизовались, используя код {auth_number}.*")
#     else:
#         await message.answer("*Привет! На связи команда SlyFox.*")

#     await message.answer("🦊")


# @dp.message(F.text, Command("admin"))
# async def adm(message: types.Message):
#     if (message.chat.id == 1826617805):
#         await message.answer("Введите код администратора:")
        

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())