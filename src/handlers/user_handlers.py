from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from pymorphy2 import MorphAnalyzer

from src.utils import get_profanity_wordlist

user_router = Router()
morph = MorphAnalyzer(lang="ru")


@user_router.message(F.text)
async def profinity_filter(message: Message, bot: Bot):
    """Проверяет сообщение на недопустимые слова и если таковые имеются, отправляет пользователю предупреждение"""
    profanity_list = await get_profanity_wordlist()
    message_word_list = message.text.lower().strip().split()

    for word in message_word_list:
        word = word.strip(' !,?.\t\n')
        parsed_word = morph.parse(word)[0]
        normal_form = parsed_word.normal_form

        if normal_form in profanity_list:
            return await message.answer("🤬 Не ругайся!")
