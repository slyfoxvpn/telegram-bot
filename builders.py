from aiogram import types

def keyboard_builder(country_flag, country_name):
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=f"{country_flag} Тариф Lite (10 GB) - 150 ₽ / mo", callback_data=f'{country_name}_srv_10')],
        [types.InlineKeyboardButton(text=f"{country_flag} Тариф Lite (20 GB) - 250 ₽ / mo", callback_data=f'{country_name}_srv_20')],
        [types.InlineKeyboardButton(text=f"{country_flag} Тариф Lite (40 GB) - 400 ₽ / mo", callback_data=f'{country_name}_srv_30')],
        [types.InlineKeyboardButton(text=f"{country_flag} Тариф Lite (∞ GB) - 550 ₽ / mo", callback_data=f'{country_name}_srv_unlimited')],
        [types.InlineKeyboardButton(text="◀️ Назад", callback_data='back_to_all_products')]
    ])

def payments_builder():
    pass