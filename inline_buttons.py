from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import get_products


menyu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒 Maxsulotlar", callback_data="menyu")],
    [InlineKeyboardButton(text="🧺 Karzinka", callback_data="karzinka")],
    [InlineKeyboardButton(text="📞 Admin bilan bog‘lanish", callback_data="admin")]
])






def MenyuButtons():
    buttons = []
    products = get_products()
    for id, maxsulot, price, image, dec in products:
        buttons.append([
            InlineKeyboardButton(
                text=f"{maxsulot} - {price} so‘m",
                callback_data=f"{id}|{maxsulot}|{price}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# def MenyuButtons():
#     markup = InlineKeyboardMarkup(inline_keyboard=[])
#     products = get_products()
#     for id, maxsulot, price, image, dec in products:  
#         markup.inline_keyboard.append([
#             InlineKeyboardButton(text=f"{maxsulot} - {price} so‘m", callback_data=f"{id}|{maxsulot}|{price}")
#         ])
#     markup.inline_keyboard.append([InlineKeyboardButton(text="⬅️ Ortga", callback_data="back")])
#     return markup


def MenuInline():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 4)],
        [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(4, 7)],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back")]
    ])
    return markup


buyurtma = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📦 Buyurtma berish", callback_data="zakaz")],
    [InlineKeyboardButton(text="🗑 Tozalash", callback_data="tozalash")],
    [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back")]
])


buying = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="ha"),
     InlineKeyboardButton(text="❌ Bekor qilish", callback_data="yoq")]
])





