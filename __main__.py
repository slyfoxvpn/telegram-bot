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
import builders


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
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗃️ Авторизоваться", callback_data='auth')],
        [types.InlineKeyboardButton(text="Главное меню (УДАЛИТЬ ПРИ РЕЛИЗЕ)", callback_data='main_menu')]
    ])
    await message.answer("*Привет! На связи команда SlyFox 🦊\nДавайте найдем ваш аккаунт.*", reply_markup=keyboard)


# Main munu
@dp.callback_query(lambda c: c.data == 'main_menu')
async def callback_query_handler_main_menu(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗃️ Локации и тарифы", callback_data='germany_srv')],
        [types.InlineKeyboardButton(text="⚙️ Настройки аккаунта", callback_data='account_settings')]
    ])
    await bot.edit_message_text("*Главное меню:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# Main munu
@dp.callback_query(lambda c: c.data == 'account_settings')
async def callback_query_handler_account_settings(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗃️ Выбрать язык (Language)", callback_data='change_language')],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data='back_to_main_menu')]
    ])
    await bot.edit_message_text("*Главное меню:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# All products code
@dp.callback_query(lambda c: c.data == 'all_products')
async def callback_query_handler_all_product(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇩🇪 Германия, Франкфурт - от 150 ₽", callback_data='germany_srv')],
        [types.InlineKeyboardButton(text="🏳️ Заказать индивидуальный сервер", callback_data='individual')],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data='back_to_main_menu')]
    ])
    await bot.edit_message_text("*Список доступных продуктов:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# Callback query for germany_srv
@dp.callback_query(lambda c: c.data == 'germany_srv')
async def callback_query_handler_germany_srv(callback_query: types.CallbackQuery):
    keyboard = builders.keyboard_builder(country_flag="🇩🇪", country_name="germany")
    await bot.edit_message_text(text="*Список доступных тарифов на локации 🇩🇪 Германия, Франкфурт:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# Callback query for germany_srv_10
@dp.callback_query(lambda c: c.data == 'germany_srv_10')
async def callback_query_handler(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇩🇪 Тинькофф", url="https://www.tinkoff.ru/")],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data='back_to_germany_srv')]
    ])
    await bot.edit_message_text(text="*Список доступных тарифов на локации 🇩🇪 Германия, Франкфурт:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# Callback query for individual
@dp.callback_query(lambda c: c.data == 'individual')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Вы можете заказать индивидуальный тариф на любой из 12 доступных локаций. На этом сервере будет расположен лишь ваш аккаунт. Вы можете добавлять и удалять неограниченное колличество ключей.')
    await bot.answer_callback_query(callback_query.id)


# Back to main menu
@dp.callback_query(lambda c: c.data == 'back_to_main_menu')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query_handler_main_menu(callback_query=callback_query)
    await bot.answer_callback_query(callback_query.id)


# Back to all products handler
@dp.callback_query(lambda c: c.data == 'back_to_all_products')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query_handler_all_product(callback_query=callback_query)
    await bot.answer_callback_query(callback_query.id)


# Back to all germany_srv handler
@dp.callback_query(lambda c: c.data == 'back_to_germany_srv')
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query_handler_germany_srv(callback_query=callback_query)
    await bot.answer_callback_query(callback_query.id)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())