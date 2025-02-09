from config.config import BOT_TOKEN 
from aiogram import Bot, Dispatcher
import asyncio
from handlers.handles import router  
from database.database import Base, engine

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)

async def main():
    Base.metadata.create_all(engine)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
