from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import Karzinka
from db import get_cart, clear_cart
from inline_buttons import buyurtma, buying
from reply import contact_phone, location_button
from config import admins

k_router = Router()

@k_router.callback_query(F.data == "karzinka")
async def show_cart(call: CallbackQuery):
    user_id = call.from_user.id
    items = get_cart(user_id)
    if not items:
        await call.message.answer("🛒 Savatingiz bo‘sh.", reply_markup=buyurtma)
        return

    text = "🧾 Savatingiz:\n\n"
    total_sum = 0
    for row in items:
        _, _, _, product_name, total_price, count = row
        total_sum += total_price
        unit_price = total_price // count if count else total_price
        text += f"• {product_name} — {count} x {unit_price} so'm = {total_price} so'm\n"

    text += f"\n💰 Jami: {total_sum} so'm"
    await call.message.answer(text, reply_markup=buyurtma)

@k_router.callback_query(F.data == "tozalash")
async def clear_user_cart(call: CallbackQuery):
    user_id = call.from_user.id
    clear_cart(user_id)
    await call.message.answer("🗑 Savat tozalandi.", reply_markup=buyurtma)

@k_router.callback_query(F.data == "zakaz")
async def zakaz_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📞 Iltimos, telefon raqamingizni yuboring:", reply_markup=contact_phone)
    await state.set_state(Karzinka.contact)

@k_router.message(F.contact, Karzinka.contact)
async def get_contact(message: Message, state: FSMContext):
    telefon = message.contact.phone_number
    await state.update_data({"telefon": telefon})
    await message.answer("📍 Iltimos, joylashuvingizni yuboring:", reply_markup=location_button)
    await state.set_state(Karzinka.manzil)

@k_router.message(F.location, Karzinka.manzil)
async def get_location(message: Message, state: FSMContext):
    loc = message.location
    await state.update_data({"la": loc.latitude, "lo": loc.longitude})
    await state.set_state(Karzinka.tasdiqlash)

    user_id = message.from_user.id
    items = get_cart(user_id)
    if not items:
        await message.answer("🛒 Savatingiz bo‘sh.", reply_markup=None)
        await state.clear()
        return

    text = "📦 Buyurtma — tasdiqlash uchun ma'lumotlar:\n\n"
    total_sum = 0
    for row in items:
        _, _, _, product_name, total_price, count = row
        unit_price = total_price // count if count else total_price
        text += f"• {product_name} — {count} x {unit_price} so'm = {total_price} so'm\n"
        total_sum += total_price

    data = await state.get_data()
    telefon = data.get("telefon")
    text += f"\n☎️ Telefon: {telefon}\n💰 Jami: {total_sum} so'm"

    await message.answer(text, reply_markup=buying)

@k_router.callback_query(F.data == "ha", Karzinka.tasdiqlash)
async def confirm_order(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    data = await state.get_data()
    telefon = data.get("telefon")
    la = data.get("la")
    lo = data.get("lo")

    items = get_cart(user_id)
    if not items:
        await call.message.answer("🛒 Savatingiz bo‘sh.")
        await state.clear()
        return

    text = "📨 Yangi buyurtma:\n\n"
    total_sum = 0
    for row in items:
        _, _, _, product_name, total_price, count = row
        unit_price = total_price // count if count else total_price
        text += f"• {product_name} — {count} x {unit_price} so'm = {total_price} so'm\n"
        total_sum += total_price

    text += f"\n☎️ Telefon: {telefon}\n💰 Jami: {total_sum} so'm"

    try:
        for admin in admins:
            await call.bot.send_location(chat_id=admin, latitude=la, longitude=lo)
            await call.bot.send_message(chat_id=admin, text=text)
    except Exception as e:
        print("Adminga yuborishda xato:", e)

    clear_cart(user_id)
    await call.message.answer("✅ Buyurtma yuborildi. Rahmat!")
    await state.clear()

@k_router.callback_query(F.data == "yoq", Karzinka.tasdiqlash)
async def cancel_order(call: CallbackQuery, state: FSMContext):
    await call.message.answer("❌ Buyurtma bekor qilindi.", reply_markup=None)
    await state.clear()














