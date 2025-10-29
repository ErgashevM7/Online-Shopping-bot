from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from db import get_product_by_id, add_to_cart, get_products, get_cart, clear_cart
from inline_buttons import menyu, MenyuButtons, MenuInline, buyurtma
from reply import asosiy_button
from states import ProductStates
from admin import admin_tel_raqam,admin_tguser,admin_id
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from db import add_product
from aiogram import types




router = Router()

# 🧑‍💼 Faqat shu ID dagi foydalanuvchilar admin hisoblanadi
admins = [6396620190,5633405041]


@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_photo(
        photo="https://g2u-wp-prod.s3-ap-southeast-2.amazonaws.com/wp-content/uploads/2022/09/Online-shopping-hero.jpg",
        caption=f"Assalomu alaykum, {message.from_user.first_name}!\nQuyidagilardan birini tanlang:",
        reply_markup=menyu
    )

@router.callback_query(F.data == "menyu")
async def show_products_callback(call: CallbackQuery, state: FSMContext):
    products = get_products()
    if not products:
        await call.message.answer("❌ Bazada hali mahsulot yo‘q.")
        return

    await state.set_state(ProductStates.selecting)
    await call.message.answer("Quyidagilardan birini tanlang:", reply_markup=MenyuButtons())


@router.callback_query(ProductStates.selecting)
async def product_selected(call: CallbackQuery, state: FSMContext):
    data = call.data
    if data == "back":
        await state.clear()
        await call.message.answer("Asosiy menyu", reply_markup=menyu)
        return

    try:
        pid_str, name, price = data.split("|")
        pid = int(pid_str)
    except Exception:
        await state.clear()
        await call.answer("Noma'lum amal", show_alert=True)
        await call.message.answer("Asosiy menyu", reply_markup=menyu)
        return

    prod = get_product_by_id(pid)
    if prod:
        _, maxsulot, pr, image, dec = prod
        await state.update_data({"product_id": pid, "product_name": maxsulot, "product_price": pr})
        await state.set_state(ProductStates.choosing_amount)
        await call.message.answer_photo(
            photo=image,
            caption=f"📦 {maxsulot}\n💰 Narxi: {pr} so‘m (kg)\n\n📝 {dec}\n\nNechta olmoqchisiz?",
            reply_markup=MenuInline()
        )
    else:
        await call.answer("Mahsulot topilmadi", show_alert=True)

@router.callback_query(ProductStates.choosing_amount)
async def amount_chosen(call: CallbackQuery, state: FSMContext):
    data = call.data
    if data == "back":
        await state.set_state(ProductStates.selecting)
        await call.message.answer("Mahsulotlar:", reply_markup=MenyuButtons())
        return

    try:
        count = int(data)
    except:
        await call.answer("Noto‘g‘ri miqdor", show_alert=True)
        return

    info = await state.get_data()
    pid = info.get("product_id")
    name = info.get("product_name")
    price = info.get("product_price")

    if pid is None or name is None:
        await call.answer("Mahsulotni tanlang", show_alert=True)
        await state.set_state(ProductStates.selecting)
        return

    total = int(price) * count
    user_id = call.from_user.id

    add_to_cart(user_id=user_id, product_id=pid, product_name=name, total_price=total, count=count)
    await call.message.answer(
        f"✅ {name} dan {count} ta savatga qo‘shildi.\n"
        f"Savatingizni ko‘rish uchun '🧺 Karzinka' tugmasini bosing.",
        reply_markup=menyu
    )
    await state.set_state(ProductStates.selecting)
    await state.clear()

@router.callback_query(F.data == "karzinka")
async def show_cart(call: CallbackQuery):
    user_id = call.from_user.id
    cart_items = get_cart(user_id)

    if not cart_items:
        await call.message.answer("🛒 Savatingiz bo‘sh.", reply_markup=menyu)
        return

    text = "🧺 Sizning savatingiz:\n\n"
    total = 0
    for item in cart_items:
        # item: (id, user_id, product_id, product_name, total_price, count)
        text += f"{item[3]} — {item[5]} ta — {item[4]} so‘m\n"
        total += item[4]
    text += f"\n💰 Jami: {total} so‘m "

    await call.message.answer(text, reply_markup=buyurtma)

@router.callback_query(F.data == "tozalash")
async def clear_user_cart(call: CallbackQuery):
    user_id = call.from_user.id
    clear_cart(user_id)
    await call.message.answer("🗑 Savat tozalandi.", reply_markup=menyu)

@router.callback_query(F.data == "admin")
async def show_admin_info(call: CallbackQuery):
    text = (
        "📞 <b>Admin bilan bog‘lanish:</b>\n\n"
        f"👤 Telegram: {admin_tguser}\n"
        f"📱 Telefon: {admin_tel_raqam}\n\n"
        "Iltimos, faqat kerakli holatlarda yozing 🙂"
    )
    await call.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "back")
async def back_to_main_menu(call: CallbackQuery):
    await call.message.answer_photo(
        photo="https://g2u-wp-prod.s3-ap-southeast-2.amazonaws.com/wp-content/uploads/2022/09/Online-shopping-hero.jpg",
        caption="🏠 Asosiy menyu:\nQuyidagilardan birini tanlang 👇",
        reply_markup=menyu
    )










class AddProduct(StatesGroup):
    name = State()
    price = State()
    desc = State()
    image = State()

@router.message(Command("add"))
async def start_add_product(message: Message, state: FSMContext):
    if message.from_user.id not in admins:
        await message.answer("⛔ Bu buyruq faqat adminlar uchun.")
        return
    await message.answer("📝 Mahsulot nomini kiriting:")
    await state.set_state(AddProduct.name)

@router.message(AddProduct.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 Narxini kiriting (so‘mda):")
    await state.set_state(AddProduct.price)

@router.message(AddProduct.price)
async def add_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Iltimos, faqat raqam kiriting.")
        return
    await state.update_data(price=int(message.text))
    await message.answer("📜 Mahsulot tavsifini kiriting:")
    await state.set_state(AddProduct.desc)

@router.message(AddProduct.desc)
async def add_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    await message.answer("🖼 Endi mahsulot rasmi yuboring:")
    await state.set_state(AddProduct.image)



# @router.message(AddProduct.image)
# async def add_image(message: types.Message, state: FSMContext):
#     image_url = message.text  # foydalanuvchi URL yuboradi
#     await state.update_data(image=image_url)
#     await message.answer("📝 Mahsulot haqida qisqacha izoh yozing:")
#     await state.set_state(AddProduct.description)

# @router.message(AddProduct.image)
# async def add_image(message: Message, state: FSMContext):
#     if not message.photo:
#         await message.answer("❗ Iltimos, rasm yuboring.")
#         return

#     photo = message.photo[-1]
#     file_id = photo.file_id

#     data = await state.get_data()
#     name = data["name"]
#     price = data["price"]
#     desc = data["desc"]

  
#     add_product(name, price, file_id, desc)

#     await message.answer(f"✅ Mahsulot qo‘shildi:\n\n📦 {name}\n💰 {price} so‘m\n📝 {desc}")
#     await state.clear()



@router.message(AddProduct.image)
async def add_image(message: Message, state: FSMContext):
    # Agar foydalanuvchi rasm yuborsa
    if message.photo:
        photo = message.photo[-1]
        image = photo.file_id  # Telegram file_id saqlanadi
    else:
        # Agar foydalanuvchi rasm ssilkasini yuborsa
        image = message.text.strip()
        # Tekshiramiz: bu URLmi?
        if not (image.startswith("http://") or image.startswith("https://")):
            await message.answer("❗ Iltimos, rasm yuboring yoki to‘g‘ri rasm URL manzilini kiriting.")
            return

    # Oldingi ma'lumotlarni olish
    data = await state.get_data()
    name = data["name"]
    price = data["price"]
    desc = data["desc"]

    # Bazaga yozamiz
    add_product(name, price, image, desc)

    # Tasdiq xabari
    await message.answer_photo(
        photo=image,
        caption=f"✅ Mahsulot qo‘shildi!\n\n📦 {name}\n💰 {price} so‘m\n📝 {desc}"
    )

    await state.clear()
