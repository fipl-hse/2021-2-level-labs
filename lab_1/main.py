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

    alphabet = 'abcdefghijklmnopqrstuvwxyzäöüßāīūēō'
    text = input('Введите строку: ')
    for i in text:
        if i not in alphabet:
            text = text.replace(i, '')
    import re
    text_1 = re.sub(r'[^\w\s]', '', text)
    text_2 = re.sub(r'[\d]', '', text_1)
    a = text_2.split(' ')
    a = [item.lower() for item in a]
    
    return a

def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    a = """0123456789=+'";:?/\|><.,@#№$%^&*()-_~`"""
    oth = list(a)
    tokens = list(input('Введите список токенов: ').split())
    swords = list(input('Введите список стоп-слов: ').split())
    n_tokens = []

    for x in swords:
        if x in oth:
            print(tokens)

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

    return n_tokens

remove_stop_words()


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    a = """0123456789=+'";:?/\|><.,@#№$%^&*()-_~`"""
    oth = list(a)
    tokens = list(input('Введите список токенов: ').split())

    for i in tokens:
        if i in oth:
            return None

    dict = {}
    for key in tokens:
        key = key.lower()
        if key in dict:
            value = dict[key]
            dict[key] = value + 1
        else:
            dict[key] = 1

    fin = sorted(dict, key=lambda x: int(dict[x]), reverse=True)
    
    return fin


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    
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
    dlist = []
    for key in freq_dict.keys():
        dictList.append(key)
    dlist_1 = dlist[:num]
    
    return dlist_1


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    
    if not (isinstance(language, str)
            and isinstance(text, str)
            and isinstance(stop_words, list)):
        return None

    elif not (all(isinstance(s, str) for s in stop_words) or stop_words == []):
        return None
    
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    lang_prof = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    
    return lang_prof


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None
    else:
        unknown_profile_top_n = get_top_n_words(unknown_profile['freq'], top_n)
        profile_to_compare_top_n = get_top_n_words(profile_to_compare['freq'], top_n)
        common = 0

        for i in unknown_profile_top_n:
            if i in profile_to_compare_top_n:
                common +=1 
        len_prof= len(profile_to_compare_top_n)
        res = round((common/len_prof), 2)
        
        return res


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_1, dict)
            and isinstance(profile_2, dict)
            and isinstance(top_n, int)):
        return None
    
    comp_1 = compare_profiles(unknown_profile, profile_1, top_n)
    comp_2 = compare_profiles(unknown_profile, profile_2, top_n)

    if comp_1 > comp_2:
        language = profile_1['name']
        return language

    elif comp_2 > comp_1:
        language = profile_2['name']
        return language

    elif comp_1 == comp_2:
        language = sorted(profile_1['name'], profile_2['name'])
        return language


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """

    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None

    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    common = []
    for word in top_n_words_compare:
        if word in top_n_words_unknown:
            common.append(word)
    sorted_common = sorted(common)

    score = round(len(common) / len(top_n_words_unknown), 2)

    max_length_word = max(profile_to_compare["freq"].keys(), key=len)
    min_length_word = min(profile_to_compare["freq"].keys(), key=len)

    length_of_tokens = []
    for token in profile_to_compare["freq"].keys():
        length_of_tokens.append(len(token))
    average_token_length = sum(length_of_tokens)/len(profile_to_compare["freq"].keys())

    report = {'name': profile_to_compare["name"],
              'common': common,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    
    return report


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    
    if not (
            isinstance(unknown_profile, dict)
            and isinstance(profiles, list)
            and isinstance(languages, list)
            and isinstance(top_n, int)):
        return None

    reports = []
    for profile in profiles:
        if profile["name"] in languages or not languages:
            report = compare_profiles_advanced(unknown_profile, profile, top_n)
            reports.append(report)
    reports = sorted(reports, key=lambda x: x["score"], reverse=True)

    if not reports:
        return None

    list_with_only_scores = []
    for element_dict in reports:
        list_with_only_scores.append(element_dict["score"])
        max_scores = max(list_with_only_scores)
        number_of_max_scores = list_with_only_scores.count(max_scores)
        reports = sorted(reports[:number_of_max_scores], key=lambda x: x["name"])
        
    return reports[0]["name"]

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
