from aiogram import Bot


async def set_description(bot: Bot):
    """Устанавливает описание бота, которое отображается при его открытии"""
    description_text = ("Привет, я бот-модератор группы.\n"
                        "В мои обязанности входит наблюдение за соблюдением пользователями правил группы."
                        "Если будешь нарушать правила, я буду тебя наказывать👮🏻.\n"
                        "Так что веди себя хорошо и мы не будем ссориться! 😇"
                        )

    await bot.set_my_description(description=description_text, language_code='ru')


async def set_short_description(bot: Bot):
    """Устанавливает информацию о боте, которое отображается при его открытии"""
    info_text = "Бот-модератор 👮🏻"
    await bot.set_my_short_description(short_description=info_text, language_code='ru')
    
