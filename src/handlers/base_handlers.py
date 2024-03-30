from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

base_router = Router()


@base_router.message(CommandStart())
async def start(message: Message):
    """Команда старта"""
    print(message.from_user.id)
    await message.answer('Привет!')


@base_router.message(Command('info'))
async def start(message: Message):
    """Команда вывода информации о боте"""
    text = ('Я - бот модератор.\n'
            'Моя функция наказывать тех пользователей, что нарушают правила поведения в группе.')
    await message.answer(text=text)
