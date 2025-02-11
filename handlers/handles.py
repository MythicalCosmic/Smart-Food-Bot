from aiogram.types import Message
from aiogram import Router
from keyboards.keyboard import *
from utils.utils import *
from aiogram.filters import Command
from database.database import *

router = Router()


def go_back_one_step(user, session):
    step_order = ["start", "menu", "ask_location", "location"]
    if user.step in step_order:
        prev_index = max(0, step_order.index(user.step) - 1)
        user.step = step_order[prev_index]
        session.commit()


def get_reply_markup_for_step(step):
    if step == "menu":
        return menu_keys
    elif step == "ask_location":
        return location_keyboard
    elif step == "location":
        return web_app_keyboard
    elif step == "order_of_user":
        return menu_keys
    else:
        return keyboard


@router.message(Command("start"))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.full_name

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user:
        if user.step in ["menu", "ask_location", "location"]:
            await message.answer("👋 Assalomu alaykum! \n\n"
                                 "🍽️ Menuga xush kelibsiz! \n", reply_markup=menu_keys)
    else:
        add_user(telegram_id, username, name, step="start")
        await message.answer(
            "👋 Assalomu alaykum! \n"
            "🤖 Men Smart Food botman! \n\n"
            "📞 Iltimos, telefon raqamingizni yuboring:",
            reply_markup=keyboard
        )
    session.close()


@router.message(lambda message: message.contact)
async def handle_phone_number(message: Message):
    telegram_id = message.from_user.id
    phone_number = message.contact.phone_number

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user:
        user.phone_number = phone_number
        user.step = "menu"
        session.commit()

        await message.answer(
            f"✅ Rahmat! Sizning ma'lumotlaringiz saqlandi! \n\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Ism: {user.name}\n"
            f"🏷️ Username: {user.username}\n"
            f"📞 Telefon: {user.phone_number}\n\n"
            "🎉 Smart Food botga xush kelibsiz!",
            reply_markup=menu_keys
        )
    else:
        await message.answer("⚠️ Xatolik: Avval /start ni bosing.")
    session.close()


@router.message(lambda message: message.text == "🛒 Buyurtma Berish")
async def handle_order(message: Message):
    session = SessionLocal()
    telegram_id = message.from_user.id
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        user.step = "ask_location"
        session.commit()
        await message.answer("📝 Buyurtma berish bo'limiga xush kelibsiz!\n\n"
                             "📍 Iltimos, Manzilingizni yuboring.", reply_markup=location_keyboard)
    else:
        await message.answer("⚠️ Xatolik: Avval /start ni bosing.")
    session.close()



@router.message(lambda message: message.location)
async def handle_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    telegram_id = message.from_user.id

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user:
        user.latitude = latitude
        user.longitude = longitude
        user.step = "location"
        session.commit()
        await message.answer("🌍 Rahmat! Lokatsiyangiz saqlandi! \n"
                             "🛒 Buyurtma berish uchun pastagi tugmani bosing", reply_markup=web_app_keyboard)
    else:
        await message.answer("⚠️ Xatolik: Avval /start ni bosing.")
    session.close()


@router.message(lambda message: message.text == "🛍️ Mening buyurtmalarim")
async def handle_order_of_user(message: Message):
    session = SessionLocal()
    telegram_id = message.from_user.id

    user = session.query(User).filter_by(telegram_id=telegram_id).first()

    if user:
        orders = session.query(Order).filter_by(user_id=user.id).all()
        user.step = "order_of_user"
        session.commit()

        if orders:
            response_text = "🍟 Sizning buyurtmalaringiz:\n\n"
            await message.answer(response_text)
            for order in orders:
                product = session.query(Product).filter_by(id=order.product_id).first()
                product_name = product.product_name if product else "Noma'lum mahsulot"
                order_text = (
                    f"🔖 Buyurtma ID: {order.id}\n"
                    f"🍽 Mahsulot Nomi: {product_name}\n"
                    f"📌 Buyurtma turi: {order.type}\n"
                )

                await message.answer(order_text, reply_markup=back_from_order_of_user)
        else:
            await message.answer("📭 Sizda hali buyurtmalar mavjud emas.")

    else:
        await message.answer("⚠️ Xatolik: Avval /start ni bosing.")

    session.close()


@router.message()
async def fallback_handler(message: Message):
    await message.answer("⚠️ Noto‘g‘ri buyruq kiritildi. Iltimos, menyudan tanlang:", reply_markup=menu_keys)