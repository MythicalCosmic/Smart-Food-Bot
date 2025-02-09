from aiogram.types import Message
from aiogram import Router
from database.database import SessionLocal, User
from keyboards.keyboard import * 
from utils.utils import *
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.full_name

    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    
    if user:
        if user.step == "menu" or "ask_location" or "location": 
            await message.answer("👋 Assalomu alaykum! \n\n"
                                "🍽️ Menuga xush kelibsiz! \n", reply_markup=menu_keys)
        else:
            await message.answer("📞 Iltimos, telefon raqamingizni yuboring:", reply_markup=keyboard)
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
    else:
        await message.answer("⚠️ Xatolik: Avval /start ni bosing.")

    await message.answer("📝 Buyurtma berish bo'limiga xush kelibsiz!\n\n"
                         "📍 Iltimos, Manzilingizni yuboring.", reply_markup=location_keyboard)
    

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
                             "🛒 Buyurtma berish uchun pastagi tugmani bosing",reply_markup=web_app_keyboard)
    else:
        await message.answer("⚠️ Xatolik: Avval /start ni bosing.")

    session.close()