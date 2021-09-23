"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:
    if type(text) != str:
        return None
    text = text.lower()
    marks = '''1234567890!()-§[]{};?@#$%:'"/.,\^&*_<>№'''
    for i in text:
        if i in marks:
            text = text.replace(i,'')
    tokens = text.split()
    return tokens
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    tokens_right = []
    if type(tokens) != list or None in tokens: #предохраняет от пустых элементов в спике
        return None
    if type(stop_words) != list:
        return None
    for i in tokens:
        if i not in stop_words:
            tokens_right.append(i)
    return tokens_right
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """


def calculate_frequencies(tokens: list) -> dict or None:
    dictionary = {} #создаём словарь
    if type(tokens) != list or None in tokens: #является ли tokens списком
        return None
    for i in tokens: #проходимся по каждому токену
        if type(i) != str: #если эл-т списка tokens не явл. строкой, то возвр. None
            return None
        if i not in dictionary: #является ли элемент списка ключом в словаре
            dictionary[i] = 1 #если не явл., то созд. такой ключ со значением 1
        else:
            dictionary[i] = dictionary[i]+1 #если явл., то значение увеличивается на 1
    return dictionary
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    if type(freq_dict) != dict:
        return None
    sorted_freq_list = sorted(freq_dict.values()) #СПИСОК отсортированных от меньшего к большему значений словаря
    #который был принят на вход
    sorted_dict_N = {} #создала словарь
    sorted_freq_list = sorted_freq_list [::-1] #СПИСОК отсортированных от БОЛЬШЕГО к МЕНЬШЕМУ значений словаря
    #который был принят на вход
    for i in sorted_freq_list: #прохожусь по каждому элементу отсортированного списка
        for k in freq_dict.keys(): #для каждого ключа в списке ключей принятого на вход словаря:
            if freq_dict[k] == i: #если значение конкр. ключа k из принятого на вход словаря
                # совпадает с элементом из отсортированного списка
                sorted_dict_N[k] = freq_dict[k] # то в новом словаре создаётся та же пара ключ-значение
    TOP_N_list = sorted_dict_N.keys() #в этой переменной записаны ключи нового словаря
    TOP_N_list = list(TOP_N_list) #преобразование переменной в список
    TOP_N_list = TOP_N_list [:top_n] #вывод первых N по популярности слов
    return TOP_N_list


    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """


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
