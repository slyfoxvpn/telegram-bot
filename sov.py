import key_managament as keys
keys.init("https://193.176.179.177:30977/0Z6cpOQ4EV4hixKJfT_jWQ") # Initialize OutlineVPN API

import telebot
from telebot import types
bot_token = "6910038122:AAFMd5qHOGfOuz53H477YbKcayFZQMjQ-Pw"
bot = telebot.TeleBot(bot_token) # Initialize Telegram bot

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Initialize reply keyboard
    # Auth button
    auth_button = types.KeyboardButton('Войти/Зарегестрироваться')
    markup.add(auth_button)
    # Price button
    price_button = types.KeyboardButton('Цены')
    markup.add(price_button)
    # More info button
    moreinfo_button = types.KeyboardButton('Больше информации')
    markup.add(moreinfo_button)

    bot.send_message(message.from_user.id, "Приветственное сообщение", reply_markup=markup) # Sending welcome message with reply keyboard

@bot.message_handler(content_types=["text"])
def prices(message):
    match message.text:
        case "Цены":
            bot.send_message(message.from_user.id, "Список цен")
        case "Больше информации":
            bot.send_message(message.from_user.id, "Информация о впн, создателях, контакты связи")
        case "Войти/Зарегестрироваться":
            bot.send_message(message.from_user.id, "Дальше что-то")





bot.infinity_polling() # Run bot






# keys.get_all_keys() # Get all keys
# keys.new_key("Example1") # Create new key
# keys.get_key("Example1") # Get information about key
# keys.rename_key("Example1", "NewExampleName") # Rename from Example1 to NewExampleName
# keys.set_limit("NewExampleName", 2048) # Set limit to 2GB
# keys.remove_limit("NewExampleName")
# keys.remove_key("NewExampleName")