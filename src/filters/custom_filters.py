import re

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram.types import Message
from pymorphy2 import MorphAnalyzer

from src.utils import get_profanity_wordlist

morph = MorphAnalyzer(lang="ru")


class ProfinityFilter(Filter):
    """Фильтр нецензурной лексики"""

    async def __call__(self, message: Message, bot: Bot) -> bool:
        profanity_list = await get_profanity_wordlist()
        text = ''

        if message.content_type == ContentType.TEXT:
            text = message.text.lower().strip().split()
        elif message.content_type == ContentType.PHOTO:
            if message.caption:
                text = message.caption.lower().strip().split()

        for word in text:
            word = word.strip(' !,?.\t\n')
            parsed_word = morph.parse(word)[0]
            normal_form = parsed_word.normal_form

            if normal_form in profanity_list:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='🤬 Не ругайся!')
                await message.delete()
                return False
        else:
            return True


class LenMessageFilter(Filter):
    """Фильтр проверяющий сообщение на допустимую длину"""

    def __init__(self):
        self.max_len = 8

    async def __call__(self, message: Message, bot: Bot) -> bool:
        text = ''
        if message.content_type == ContentType.TEXT:
            text = message.text
        elif message.content_type == ContentType.PHOTO:
            if message.caption:
                text = message.caption

        if len(text) < self.max_len:
            return True
        else:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='⚠️ Количество символов в сообщении превышает допустимую норму (800) ⚠️')
            await message.delete()
            return False


class LinksFilter(Filter):
    """Фильтр проверяющий сообщение на наличие ссылок"""

    def __init__(self):
        # self.pattern = r'(?:https?://|www\.)?\w+\.\w+(?:/\w+)*/?' # Реагирует на ссылки без (http/https/www)
        self.pattern = r'(?:https?://|www\.)\w+\.\w+(?:/\w+)*/?'

    async def __call__(self, message: Message, bot: Bot) -> bool:
        text = ''
        if message.content_type == ContentType.TEXT:
            text = message.text
        elif message.content_type == ContentType.PHOTO:
            if message.caption:
                text = message.caption

        links_list = re.findall(self.pattern, text, flags=re.IGNORECASE)

        if links_list:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='⚠️ В вашем сообщении содержатся ссылки! ⚠️')
            await message.delete()
            return False
        else:
            return True
