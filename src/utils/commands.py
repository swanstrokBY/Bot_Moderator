from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    """Делает меню с указанными командами бота"""
    commands = [
        BotCommand(
            command='start',
            description='Запустить бота'
        ),
        BotCommand(
            command='info',
            description='Получить информацию о боте'
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

