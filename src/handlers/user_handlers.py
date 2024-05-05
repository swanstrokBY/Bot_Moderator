from aiogram import Router, Bot, F
from aiogram.types import Message

from filters import ProfinityFilter, LinksFilter, LenMessageFilter

user_router = Router()

user_router.message.filter(
    F.chat.type.in_({"supergroup", "group"}),
    ProfinityFilter(),
    LinksFilter(),
    LenMessageFilter()
)


@user_router.message(F.media_group_id)
async def filter_photo_handler(message: Message):
    content = message.content_type
    print(content)


@user_router.message(F.text)
async def text_handler(message: Message, bot: Bot) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='Ваше сообщение добавлено в группу.')
