import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from utils import set_commands, set_description, set_short_description
from handlers import admin_router, base_router, user_router
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    """Функция запускающая бота"""
    bot = Bot(token=os.getenv('TOKEN_BOT'), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    dp.include_routers(base_router, admin_router, user_router)

    await set_commands(bot=bot)
    await set_description(bot=bot)
    await set_short_description(bot=bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-5s TIME:%(asctime)s %(message)s')
    asyncio.run(main())
