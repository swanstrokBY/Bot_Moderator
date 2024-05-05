import os
from contextlib import suppress
from datetime import datetime, timedelta

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ChatPermissions
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv

from src.utils import get_profanity_wordlist, add_wordlist_to_file

load_dotenv()

admin_id = int(os.getenv('ADMIN_ID'))
admin_router = Router()
admin_router.message.filter(
    F.from_user.id == admin_id,
    F.chat.type.in_({"supergroup", "group"}),
)


@admin_router.message(Command('sort_file'))
async def sort_profanity_file(message: Message, bot: Bot):
    """Хэндлер сортирующий список недопустимых слов в файле"""
    await message.delete()
    wordlist = await get_profanity_wordlist()
    await add_wordlist_to_file(wordlist=wordlist)
    await bot.send_message(chat_id=admin_id,
                           text='Список недопустимых слов в файле отсортирован ☑️')


async def message_to_admin(text: str, bot: Bot) -> None:
    """Функция посылающая сообщение администратору"""
    await bot.send_message(chat_id=admin_id, text=text)


@admin_router.message(Command("ban"))
async def ban(message: Message, bot: Bot, command: CommandObject | None = None):
    """Функция банящая пользователя"""
    await message.delete()
    reply = message.reply_to_message

    if not reply:
        return await message.answer('👀 Я никого не нашел')

    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(chat_id=message.chat.id,
                                  user_id=reply.from_user.id)

        await bot.send_message(chat_id=reply.from_user.id,
                               text='🚫 Вас забанили за нарушение правил группы. 🚫')

        text_to_admin = (f"🚫 Пользователь: <b>{reply.from_user.first_name}</b> c "
                         f"tg_id: <i>{reply.from_user.id}</i> забанен за нарушение правил группы! 🚫")

        await message_to_admin(text=text_to_admin, bot=bot)


@admin_router.message(Command("unban"))
async def unban(message: Message, bot: Bot, command: CommandObject | None = None):
    """Функция разбанивающая пользователя"""
    await message.delete()
    user_id = int(command.args)

    with suppress(TelegramBadRequest):
        await bot.unban_chat_member(chat_id=message.chat.id,
                                    user_id=user_id,
                                    only_if_banned=True
                                    )

        await bot.send_message(chat_id=user_id,
                               text='😇 Вас разбанили, надеюсь в будущем вы больше не будете нарушать правила! 😇')

        text_to_admin = f"😇 Пользователь с tg_id: <i>{user_id}</i> разбанен! 😇"

        await message_to_admin(text=text_to_admin, bot=bot)


@admin_router.message(Command("mute"))
async def mute(message: Message, bot: Bot, command: CommandObject | None = None):
    """Функция мутящая пользователя"""
    await message.delete()
    reply = message.reply_to_message

    if not reply:
        return None

    with (suppress(TelegramBadRequest)):
        current_time = datetime.utcnow()
        datetime_until_mute = current_time + timedelta(days=30)

        await bot.restrict_chat_member(chat_id=message.chat.id,
                                       user_id=reply.from_user.id,
                                       until_date=datetime_until_mute,
                                       permissions=ChatPermissions(
                                           can_send_messages=False,
                                           can_send_photos=False
                                       )
                                       )

        await bot.send_message(chat_id=reply.from_user.id,
                               text='⚠️ Вам ограничили доступ к группе на один месяц за нарушение правил группы. '
                                    'При повторении нарушений с вашей стороны, вы будете забанены навсегда. ⚠️')

        text_to_admin = (f"⚠️ Пользователь: <b>{reply.from_user.first_name}</b>"
                         f"с tg_id: <i>{reply.from_user.id}</i> замучен на 1 месяц за нарушение правил группы! ⚠️")

        await message_to_admin(text=text_to_admin, bot=bot)


@admin_router.message(Command("unmute"))
async def unmute(message: Message, bot: Bot, command: CommandObject | None = None):
    """Функция разбанивающая пользователя"""
    await message.delete()
    user_id = int(command.args)
    print(user_id)

    with (suppress(TelegramBadRequest)):
        await bot.restrict_chat_member(chat_id=message.chat.id,
                                       user_id=user_id,
                                       permissions=ChatPermissions(
                                           can_send_messages=True,
                                           can_send_photos=True
                                       )
                                       )

        await bot.send_message(chat_id=user_id,
                               text='😇 Вас размутили, надеюсь в будущем вы больше не будете нарушать правила! 😇')

        text_to_admin = (f"😇 Пользователь с tg_id: <i>{user_id}</i> размучен! 😇")

        await message_to_admin(text=text_to_admin, bot=bot)
