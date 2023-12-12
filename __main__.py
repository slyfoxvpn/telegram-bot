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
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery


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
    await message.answer("", reply_markup=keyboard)

# Main munu
@dp.message(F.text, Command("Menu"))
async def all_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗃️ Локации и тарифы", callback_data='germany_srv')],
        [types.InlineKeyboardButton(text="⚙️ Настройки аккаунта", callback_data='individual')]
    ])
    await message.answer("*Главное меню:*", reply_markup=keyboard)


# All products code
@dp.callback_query(lambda c: c.data == 'all_products')
async def callback_query_handler_all_product(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇩🇪 Германия, Франкфурт - от 200 ₽", callback_data='germany_srv')],
        [types.InlineKeyboardButton(text="🏳️ Заказать индивидуальный сервер", callback_data='individual')]
    ])
    await bot.edit_message_text("*Список доступных продуктов:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# Callback query for germany_srv
@dp.callback_query(lambda c: c.data == 'germany_srv')
async def callback_query_handler(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇩🇪 Тариф Lite (10 GB) - 150 ₽ / mo", callback_data='germany_srv_10')],
        [types.InlineKeyboardButton(text="🇩🇪 Тариф Lite (20 GB) - 250 ₽ / mo", callback_data='germany_srv_20')],
        [types.InlineKeyboardButton(text="🇩🇪 Тариф Lite (40 GB) - 400 ₽ / mo", callback_data='germany_srv_40')],
        [types.InlineKeyboardButton(text="🇩🇪 Тариф Lite (∞ GB) - 550 ₽ / mo", callback_data='germany_srv_unlimited')],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data='back_to_all_products')]
    ])

    await bot.edit_message_text(text="*Список доступных тарифов на локации 🇩🇪 Германия, Франкфурт:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# Callback query for individual
@dp.callback_query(lambda c: c.data == 'individual')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
    await bot.answer_callback_query(callback_query.id)


# Back to all products handler
@dp.callback_query(lambda c: c.data == 'back_to_all_products')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query_handler_all_product(callback_query=callback_query)
    await bot.answer_callback_query(callback_query.id)


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