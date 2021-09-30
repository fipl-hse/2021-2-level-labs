"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    return true

def tokenize():
    alphabet = 'abcdefghijklmnopqrstuvwxyzäöüßāīūēō'
    s = input('Введите строку: ')
    for i in s:
        if i not in alphabet:
            s = s.replace(i, '')
    import re
    s_1 = re.sub(r'[^\w\s]', '', s)
    s_2 = re.sub(r'[\d]', '', s_1)
    a = s_2.split(' ')
    a = [item.lower() for item in a]
    print (a)

tokenize ()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    pass

def remove_stop_words():
    a = """0123456789=+'";:?/\|><.,@#№$%^&*()-_~`"""
    oth = list(a)
    tokens = list(input('Введите список токенов: ').split())
    swords = list(input('Введите список стоп-слов: ').split())
    n_tokens = []

    for x in swords:
        if x in oth:
            print (tokens)

    for i in tokens:
        if i in oth:
            return None

    if isinstance(tokens, list) and isinstance(swords, list):
        if all(isinstance(s, str) for s in tokens):
             for i in tokens:
                 if i not in swords:
                     n_tokens.append(i)
        else:
            return None
    else:
        return None

    print(n_tokens)

remove_stop_words()


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    pass

def calculate_frequencies():
    a = """0123456789=+'";:?/\|><.,@#№$%^&*()-_~`"""
    oth = list(a)
    tokens = list(input('Введите список токенов: ').split())

    for i in tokens:
        if i in oth:
            return None

    Dict = {}
    for key in tokens:
        key = key.lower()
        if key in Dict:
            value = Dict[key]
            Dict[key] = value + 1
        else:
            Dict[key] = 1

    fin = sorted(Dict, key=lambda x: int(Dict[x]), reverse=True)
    print(fin)

calculate_frequencies()


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    pass

def  get_top_n_words():
    num = int(input('Число слов в топе: '))
    freq_dict = {}
    while True:
        print('Введите токен (нажмите enter после ввода крайнего токена): ')
        k = input()
        if k == '':
            break
        print('Ведите частотность: ')
        v = input()
        freq_dict[k] = v
    dictList = []
    for key in freq_dict.keys():
        dictList.append(key)
    print(dictList[:num])
get_top_n_words()


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
