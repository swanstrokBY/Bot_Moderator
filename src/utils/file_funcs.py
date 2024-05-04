import json


async def get_profanity_wordlist() -> list:
    """Возвращает список с недопустимыми словами из файла"""
    with open('utils/profanity.json', 'r') as f:
        profanity_list = json.load(f)
        return profanity_list


async def add_wordlist_to_file(wordlist: list) -> None:
    """Функция записывает отсортированный список слов в файл"""
    with open('utils/profanity.json', 'w') as f:
        json.dump(sorted(wordlist), f, ensure_ascii=False, indent=4)


async def check_word_in_file(data: str) -> list | None:
    """Проверяет есть ли слово в файле, если нет то добавляет слово в список"""
    profanity_list = await get_profanity_wordlist()
    len_old_list = len(profanity_list)
    wordlist = data.lower().strip().split(',')

    for word in wordlist:
        moderate_word = word.strip()
        if moderate_word not in profanity_list:
            profanity_list.append(moderate_word)

    if len_old_list != len(profanity_list):
        return profanity_list
    else:
        return None


async def put_new_words_to_file(data: str) -> None:
    """Добавляет новые данные в файл"""
    wordlist = await check_word_in_file(data=data)
    if wordlist:
        await add_wordlist_to_file(wordlist=wordlist)
