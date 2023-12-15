import asyncio
import logging
import re
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
# from config_reader import config
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject, StateFilter
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import string
username = ''

# Finale State Machine Class
class FSM(StatesGroup):
    register_username_state = State()
    register_password_state = State()

# Username validation
# Rules: A-Z, a-z, 0-9, "_", "-"
allowed_symbols_list = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)] + ['_', '-']
def username_valid(username):
    for char in username:
        if char not in allowed_symbols_list:
            return False
    return True

# Password validation
# Rules: greater than min_len, less than max_len, at least 1 letter, 1 digit and 1 special symbol
def password_valid(password):
    min_len = 10
    max_len = 64
    if len(password) < min_len:
        return False
    elif len(password) > max_len:
        return False
    elif not any(char.isalpha() or char.isdigit() for char in password):
        return False
    for char in password:
        if char in string.punctuation:
            return True
    return False

# Init bot
logging.basicConfig(level=logging.INFO) # Enable logging
# bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="Markdown")
bot = Bot(token='5460754777:AAE5kuh4WBE9WljuYrhxB8cpjx7zGPPCYkg', parse_mode="Markdown")
dp = Dispatcher()


# 'start' with auth code (if exist)
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'auth_(\d+)'))))
async def cmd_start(message: Message, command: CommandObject):
    auth_id = command.args.split("_")[1]
    # Some post to the database to link auth_id and telegram user id
    global username
    username = '' # Request to the database to get username
    print(f"Auth with {auth_id}")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Главное меню", callback_data='main_menu')]
    ])
    await message.answer(f'Вы вошли в аккаунт как {username}!', reply_markup=keyboard)


# 'start' with ref code (if exist)
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'ref_(\d+)'))))
async def cmd_start(message: Message, command: CommandObject):
    ref_id = command.args.split("_")[1]
    print(f"Ref from {ref_id}")
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Продолжить авторизацию", callback_data='auth')]
    ])
    await message.answer(f'Вы активировали реферальную ссылку!', reply_markup=keyboard)


# 'start' default handler
@dp.message(F.text, CommandStart())
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗃️ Авторизоваться", callback_data='auth')],
        [types.InlineKeyboardButton(text="Главное меню (УДАЛИТЬ ПРИ РЕЛИЗЕ)", callback_data='main_menu')]
    ])
    await message.answer("*Привет! На связи команда SlyFox 🦊\nДавайте найдем ваш аккаунт.*", reply_markup=keyboard)


# Auth
@dp.callback_query(lambda c: c.data == 'auth')
async def callback_query_handler_auth(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Вход", callback_data='login')],
        [types.InlineKeyboardButton(text="Регистрация", callback_data='register')]
    ])
    await bot.edit_message_text(text="Выберите, что хотите сделать ниже:", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


# Login
@dp.callback_query(lambda c: c.data == 'login')
async def callback_query_handler_login(callback_query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Перейти на сайт", url='example.com/gettglink')]
    ])
    await bot.edit_message_text(text="Пройдите авторизацию на сайте и перезапустите бота по полученной ссылки", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


# Register
@dp.callback_query(lambda c: c.data == 'register', StateFilter(None))
async def callback_query_handler_register(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(text="Придумайте логин: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await state.set_state(FSM.register_username_state)

# Username input
@dp.message(FSM.register_username_state)
async def register_username_input(message: Message, state: FSMContext):
    if not username_valid(message.text):
        await message.answer('В сообщении содержится символы, отличные от A-Z a-z 0-9 "_" "-" '
                             'Попробуйте еще раз', parse_mode='HTML')
        return None
    elif False: # Check username in database
        await message.answer('Имя пользователя уже занято! \nПопробуйте еще раз')
        return None
    # Some other checks
    global username
    username = message.text
    await message.answer('Успех! \nПридумайте пароль: ')
    await state.set_state(FSM.register_password_state)

# Password input
@dp.message(FSM.register_password_state)
async def register_password_input(message: Message, state: FSMContext):
    if not password_valid(message.text):
        await message.answer('Пароль должен быть больше 10 символов и меньше 64, содержать хотя-бы одну букву, одну цифру и один специальный символ '
                             'Попробуйте еще раз', parse_mode='HTML')
        return None
    # Some other checks
    # Some post to the database to write a new account and link with telegram
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Главное меню", callback_data='main_menu')]
    ])
    await message.answer(f'Вы зарегестрировались как {username}!',  reply_markup=keyboard)
    await state.clear()


# Main munu
@dp.callback_query(lambda c: c.data == 'main_menu')
async def callback_query_handler_main_menu(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗃️ Локации и тарифы", callback_data='germany_srv')],
        [types.InlineKeyboardButton(text="⚙️ Настройки аккаунта", callback_data='individual')]
    ])
    await bot.edit_message_text("*Главное меню:*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)


# All products code
@dp.callback_query(lambda c: c.data == 'all_products')
async def callback_query_handler_all_product(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇩🇪 Германия, Франкфурт - от 150 ₽", callback_data='germany_srv')],
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


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())