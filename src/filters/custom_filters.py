import re

from aiogram.filters import Filter
from aiogram.types import Message
from pymorphy2 import MorphAnalyzer

from src.utils import get_profanity_wordlist

morph = MorphAnalyzer(lang="ru")


class ProfinityFilter(Filter):
    """Фильтр нецензурной лексики"""

    async def __call__(self, message: Message) -> bool:
        profanity_list = await get_profanity_wordlist()
        message_word_list = message.text.lower().strip().split()

        for word in message_word_list:
            word = word.strip(' !,?.\t\n')
            parsed_word = morph.parse(word)[0]
            normal_form = parsed_word.normal_form

            if normal_form in profanity_list:
                return True
        else:
            return False


class LenMessageFilter(Filter):
    """Фильтр проверяющий сообщение на допустимую длину"""

    async def __call__(self, message: Message):
        return len(message.text) > 800


class LinksFilter(Filter):
    """Фильтр проверяющий сообщение на наличие ссылок"""

    def __init__(self):
        # self.pattern = r'(?:https?://|www\.)?\w+\.\w+(?:/\w+)*/?' # Реагирует на ссылки без (http/https/www)
        self.pattern = r'(?:https?://|www\.)\w+\.\w+(?:/\w+)*/?'

    async def __call__(self, message: Message):
        links_list = re.findall(self.pattern, message.text, flags=re.IGNORECASE)
        if links_list:
            return True
        else:
            return False
