import asyncio
import logging
import os
import re
import time
from uuid import uuid4
from dotenv import load_dotenv
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#from readers.config_reader import config
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
#import builders.location_and_tariffs_builder as location_and_tariffs_builder
#from readers.language_reader import LanguageManager
#from aiogram.fsm.storage.memory import MemoryStorage
#from aiogram.dispatcher import FSMContext



load_dotenv() # Load .env
TOKEN = os.getenv("BOT_TOKEN") # Load secret token from .env
TECHINCAL_SUPPORT_ID = os.getenv("TECHINCAL_SUPPORT_ID")


logging.basicConfig(level=logging.INFO) # Enable logging
bot = Bot(token=TOKEN, parse_mode="Markdown") # Bot init
dp = Dispatcher() # Dispatcher (?)


# 'start' with auth code (if exist)
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'auth_(\d+)'))))
async def cmd_start(message: Message, command: CommandObject):
    auth_id = command.args.split("_")[1]
    await message.answer(f"Started with: auth:code@{auth_id}")
    
    # Создаем объект CallbackQuery для передачи в callback_query_main_menu
    callback_query = types.CallbackQuery(
        id=str(uuid4()),  # Преобразуйте id в строку
        from_user=message.from_user,
        chat_instance=str(message.chat.id),  # Преобразуйте chat_instance в строку
        message=message,
        data='main_menu'
    )

    # Вызываем callback_query_main_menu
    await callback_query_main_menu(callback_query)


# 'start' with ref code (if exist)
@dp.message(F.text, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'ref_(\d+)'))))
async def cmd_start(message: Message, command: CommandObject):
    ref_id = command.args.split("_")[1]
    await message.answer(f"Started with: referal:code@{ref_id}")


# 'start' default handler
@dp.message(F.text, CommandStart())
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="С чистого листа", callback_data='main_menu')], # Sign up
        [types.InlineKeyboardButton(text="Привязать аккаунт", url=f"https://tgc.slyfoxvpn.ru/auth?id={message.from_user.id}")], # tgc - telegram connect feature
        [types.InlineKeyboardButton(text="Привязать аккаунт adm", url=f"https://t.me/slyfoxvpn_bot?start=auth_3784242393")]

    ])
    
    await message.answer(f"*Привет! На связи Алиса из команды SlyFox 🦊\n\nЯ слежу за безопасностью вашей сети и не даю вашим данным попасть в руки злоумышленников.\n\nДавайте знакомится!*", reply_markup=keyboard)


# 'group test'
@dp.message(F.text, Command(prefix="/", commands=["test"]))
async def group_test(message: Message):
    chat_id = TECHINCAL_SUPPORT_ID # Замените на ID вашей группы
    await bot.send_message(chat_id, "Hello")


# Callback query for main menu
@dp.callback_query(lambda c: c.data == 'main_menu')
async def callback_query_main_menu(callback_query: types.CallbackQuery):
    account_linked = True

    if (account_linked):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📦 Управлять подпиской", callback_data='subscription')],
            [types.InlineKeyboardButton(text="❓ Техническая поддержка", callback_data='technical_support')],
            [types.InlineKeyboardButton(text="🦊 Перейти на сайт", url=f"https://tgc.slyfoxvpn.ru/auth?id={callback_query.from_user.id}")] # tgc - telegram connect feature
        ])
    else:
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="📦 Управлять подпиской", callback_data='subscription')],
            [types.InlineKeyboardButton(text="❓ Техническая поддержка", callback_data='technical_support')],
            [types.InlineKeyboardButton(text="🔗 Привязать аккаунт", url=f"https://tgc.slyfoxvpn.ru/link?id={callback_query.from_user.id}")] # tgc - telegram connect feature
        ])

    try:
        await bot.edit_message_text(text="*Главное меню! Куда отправимся? 🚀*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    except TelegramBadRequest:
        await bot.send_message(text="*Главное меню! Куда отправимся? 🚀*", reply_markup=keyboard, chat_id=callback_query.from_user.id)

    await bot.answer_callback_query(callback_query.id) # Answer to query


# technical_support
@dp.callback_query(lambda c: c.data == 'technical_support')
async def callback_query_technical_support(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❌ Отменить", callback_data="main_menu")], # tgc - telegram connect feature
    ])

    await bot.edit_message_text(text="*Вы можете обратится в техническую поддержку по любом вопросу. Советуем для начала ознакомится с нашей FAQ - там может находится уже готовый ответ на ваш вопрос.\n\nНиже напишите ваше обращение одним сообщением, приложите сжатую фотографию если необходимо.*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id) # Answer to query
    

# Subscription
@dp.callback_query(lambda c: c.data == 'subscription')
async def callback_query_subscription(callback_query: types.CallbackQuery):
    subscription_is = False

    if (subscription_is):
        date_out = "10.02.2024"
        date_object = datetime.strptime(date_out, "%d.%m.%Y")
        formatted_date = date_object.strftime("%d %B %Y года")

        date_one_line = datetime.strptime("10.02.2024", "%d.%m.%Y").strftime("%d %B %Y года")

        price = 250.00
        balance = 500.00
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🗓 Продлить подписку", callback_data='renew_subscription')],
            [types.InlineKeyboardButton(text="🔸 Управлять уровнями", callback_data='subscription_level_manage')],
            [types.InlineKeyboardButton(text="🔄 Обновить", callback_data='update_subscription'), types.InlineKeyboardButton(text="🗃️ Главное меню", callback_data="main_menu")], # tgc - telegram connect feature
        ])

        await bot.edit_message_text(text=f"*🦊 Тариф: Стандартный*\n\n*🗓 Дата списания: {date_one_line}*\n\n*💳 Баланс: {balance}₽*\n*💰 Стоимость текущей подписки: {price}₽*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    else:
        balance = 250.00

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🗓 Приобрести подписку", callback_data='list_of_subscriptions')],
            [types.InlineKeyboardButton(text="🔸 Пробный период", callback_data='f')],
            [types.InlineKeyboardButton(text="🔄 Обновить", callback_data='update_subscription'), types.InlineKeyboardButton(text="🗃️ Главное меню", callback_data="main_menu")], # tgc - telegram connect feature
        ])

        await bot.edit_message_text(text=f"*🦊 У вас нет оформленной подписки.*\n\n*💳 Баланс: {balance}₽*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


    await bot.answer_callback_query(callback_query.id) # Answer to query


@dp.callback_query(lambda c: c.data == 'list_of_subscriptions')
async def callback_query_list_of_subscriptions(callback_query: types.CallbackQuery):

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Пробный (30₽ / 1 день)", callback_data='l')],
        [types.InlineKeyboardButton(text="Стандартный (250₽ / 30 дней)", callback_data='l')],
        [types.InlineKeyboardButton(text="Приватный (500₽ / 30 дней)", callback_data='k')],
        #[types.InlineKeyboardButton(text="Личный (799₽ / 30 дней)", callback_data='k')],
        #[types.InlineKeyboardButton(text="Сравнить планы", callback_data='k')],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data='subscription')],

    ])

    await bot.edit_message_text(
        text=f"""**Список доступных подписок:**
        
*Тариф Пробный 
(30₽ / 1 день)*

📈 Неограниченная скорость передачи
♾ Неограниченное колличество трафика
💻 До 1 устройства одновременно
🏳️ Одна поддерживаемая страна

*Тариф Стандартный 
(8,3₽ / 1 день)* \*

📈 Неограниченная скорость передачи
♾ Неограниченное колличество трафика
💻 До 3 устройств одновременно
🚩 Множество стран на выбор

*Тариф Приватный 
(16,6₽ / 1 день)* \*

📈 Неограниченная скорость передачи
♾ Неограниченное колличество трафика
👥 На одном сервере с вами не больше 2 других человек
💻 До 5 устройств одновременно
🛡️ Блокировка рекламы
✅ Приорететная поддержка
🚩 Множество стран на выбор

__\* Цена при оплате за 30 дней__""",
        reply_markup=keyboard,
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id)


    #await bot.edit_message_text(text=f"*Список доступных подписок:*\n\n*Пробный (30₽ / 1 день)*\n- Неограниченная скорость передачи.*\n- До 1-го устройства одновременно\n*- Безлимитный трафик*\n", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

    await bot.answer_callback_query(callback_query.id) # Answer to query




# Subscription level manage
@dp.callback_query(lambda c: c.data == 'subscription_level_manage')
async def callback_query_subscription_level_manage(callback_query: types.CallbackQuery):
    balance = 500.00
    price = 500.00

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Сменить уровень подписки", callback_data='renew_subscription')],
        [types.InlineKeyboardButton(text="📦 Управлять подпиской", callback_data='subscription')],
        [types.InlineKeyboardButton(text="🗃️ Главное меню", callback_data="main_menu")], # tgc - telegram connect feature
    ])

    await bot.edit_message_text(text=f"*🦊 Текущий уровень подписки: 🌟🌟🌟*\n\n*💳 Баланс: {balance}₽*\n*💰 Стоимость текущей подписки: {price}₽*\n\n*Вы можете изменить свой уровень подписки.\n\nКак это работает?\n\nЕсли вы увеличиваете уровень подписки - списывается оставшаяся разница до следующего списания.\n\nЕсли вы понижаете уровень подписки - ваша текущая будет действовать до конца списания, а затем будем изменна на более низкий уровень.\n\nУчтите, что при этом ваш текущий ключ будет обновлен.\n\nПодписку можно изменять раз в 3 дня.*", reply_markup=keyboard, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id) # Answer to query


# Update subscription
@dp.callback_query(lambda c: c.data == 'update_subscription')
async def callback_query_update_subscription(callback_query: types.CallbackQuery):
    await bot.edit_message_text(text=f"*🔄 Получаю актуальную информацию..*", reply_markup=None, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    
    time.sleep(0.5) # Timeout
    
    await callback_query_subscription(callback_query=callback_query)
    await bot.answer_callback_query(callback_query.id) # Answer to query


# Ignore other type
@dp.message(F.photo)
async def cmd_start(message: types.Message):
    await message.reply(f"Я пока не умею различать фотографии, но мне очень интересно посмотреть, что там у вас 📸🦊")


@dp.message(F.video)
async def cmd_start(message: types.Message):
    await message.reply(f"Я пока не умею различать видео, но мне очень интересно посмотреть, что там у вас 🎥🦊")


@dp.message(F.video_note)
async def cmd_start(message: types.Message):
    await message.reply(f"Я пока не умею различать видео, но мне очень интересно посмотреть, что там у вас 🎥🦊")


@dp.message(F.audio)
async def cmd_start(message: types.Message):
    await message.reply(f"Вы что-то сказали? Извините, я понимаю только на лисьем! Фр-фр 🔊🦊")


@dp.message(F.voice)
async def cmd_start(message: types.Message):
    await message.reply(f"Вы что-то сказали? Извините, я понимаю только на лисьем! Фр-фр 🔊🦊")


@dp.message(F.document)
async def cmd_start(message: types.Message):
    await message.reply(f"Документы? Сложно и скучно. Оставлю это своему юристу 📄🦊")


@dp.message(F.location)
async def cmd_start(message: types.Message):
    await message.reply(f"Воу, куда это вас занесло? Как там погодка? 📍🦊")


@dp.message(F.contact)
async def cmd_start(message: types.Message):
    await message.reply(f"Я не могу различать номера, но надеюсь, вы порекомендуете SlyFox VPN этому контакту за меня 👤🦊")


# Start the process of polling new updates
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


    # 🌟 - 30 рублей за один день безлимитного использования, один IP адресс
# 🌟🌟 - Тариф стандартный, 30 дней, 250 рублей, без ограничений по трафику, техподдержка только в телеграм или на сайте (позже), до 2-ух IP адресов одновременно, доступна одна страна
# 🌟🌟🌟 - Тариф премиальный, 30 дней, 500 рублей, техническая поддержка во всех соцсетях (позже), до 5-ти IP адресов одновременно, блокировщик рекламы, все поддерживыемые страны доступны