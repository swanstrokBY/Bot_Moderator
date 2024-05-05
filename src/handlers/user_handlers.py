from aiogram import Router, Bot, F
from aiogram.types import Message

from filters import ProfinityFilter, LenMessageFilter, LinksFilter

user_router = Router()


@user_router.message(F.media_group_id, F.photo)
async def filter_photo_handler(message: Message, bot: Bot):
    pass


@user_router.message(F.text, LinksFilter())
async def links_filter_handler(message: Message, bot: Bot):
    """Проверяет есть ли ссылки в сообщении"""
    await bot.send_message(chat_id=message.from_user.id,
                           text='⚠️ В вашем сообщении содержатся ссылки! ⚠️')
    # await message.delete()


@user_router.message(F.text, ProfinityFilter())
async def profinity_handler(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.from_user.id,
                           text='🤬 Не ругайся!')
    await message.delete()


@user_router.message(F.text, LenMessageFilter())
async def len_msg_check_handler(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.from_user.id,
                           text='⚠️ Количество символов в сообщении превышает допустимую норму (800) ⚠️')
    await message.delete()
