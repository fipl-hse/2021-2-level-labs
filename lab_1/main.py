"""
Lab 1
Language detection
"""

en_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
de_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z', 'ß', 'ö', 'ü', 'ä']
stop_words = ['the', 'a', 'is']


def tokenize(text):
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    # Validate input
    if not isinstance(text, str):
        return None

    result = []
    word = ''
    for char in text.lower():
        if char in de_alphabet:
            word = word + char
        elif char == ' ':
            if len(word) > 0:
                result.append(word)
                word = ''

    if len(word) > 0:
        result.append(word)

    if len(result) > 0:
        return result

    return None


def remove_stop_words(tokens, st_words):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param st_words: a list of stop words
    :return: a list of tokens without stop words
    """

    # Check stop words
    st_word_valid = []
    if isinstance(st_words, list):
        for stop_word in st_words:
            if isinstance(stop_word, str):
                if stop_word in stop_words:
                    st_word_valid.append(stop_word)

    # Check tokens
    if type(tokens) != list or len(tokens) == 0:
        return None

    tokens_valid = []
    for word in tokens:
        if not isinstance(word, str):
            return None

        if word not in st_word_valid:
            tokens_valid.append(word)

    return tokens_valid


def calculate_frequencies(tokens):
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    # Check tokens validity
    if isinstance(tokens, list):
        for word in tokens:
            if not isinstance(word, str):
                return None
    else:
        return None

    # Creation of dictionary [token, freq]
    token_dict = {}
    for key in tokens:
        key = key.lower()
        if key in token_dict:
            value = token_dict[key]
            token_dict[key] = value + 1
        else:
            token_dict[key] = 1

    return token_dict


def get_top_n_words(freq_dict, top_n):
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict):
        return None

    top_list = []
    if top_n > 0:
        ind = 0
        for i in sorted(freq_dict.items(), reverse=True, key=lambda pair: pair[1]):
            top_list.append(i[0])
            ind = ind + 1
            if ind == top_n:
                return top_list

    return top_list


def create_language_profile(language: str, text: str, stop_words: list):
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language,str) and isinstance(text, str) \
        and isinstance(stop_words, list):
        return None
    else:
        profile = {}
        tokens = tokenize(text)
        tokens = remove_stop_words(tokens, stop_words)
        dictionary = calculate_frequencies(tokens)
        profile['name'] = language
        profile['freq'] = dictionary
        profile['n_words'] = len(profile['freq'].keys())
        return profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int):
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict) and \
            isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        return None
    else:
        unknown_prof_tokens = get_top_n_words(unknown_profile['freq'], top_n)
        compare_prof_tokens = get_top_n_words(profile_to_compare['freq'], top_n)
        common_tokens = 0
        for i in unknown_prof_tokens:
            if i in compare_prof_tokens:
                common_tokens = common_tokens + 1
        common_freq_words = common_tokens / len(unknown_prof_tokens)
        common_freq_words = round(common_freq_words, 2)
        return common_freq_words


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int):
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile,dict) or not isinstance(profile_1, dict) \
        or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None
    else:
        profile_1_word = compare_profiles(unknown_profile, profile_1, top_n)
        profile_2_word = compare_profiles(unknown_profile, profile_2, top_n)
        if profile_1_word > profile_2_word:
            return profile_1['name']
        if profile_2_word > profile_1_word:
            return profile_2['name']
        if profile_1['name'] > profile_2['name']:
            return profile_1['name']
        else:
            return profile_2['name']


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int):
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not isinstance(unknown_profile,dict) and isinstance(profile_to_compare['freq'], top_n) \
        and isinstance(top_n, int):
        return None
    common_tokens = []
    for common_top_word in enumerate(get_top_n_words(profile_to_compare['freq'], top_n)):
        if common_top_word[1] in get_top_n_words(unknown_profile['freq'], top_n):
            common_tokens.append(common_top_word[1])
    words = list(profile_to_compare['freq'].keys())
    score = compare_profiles(unknown_profile, profile_to_compare, top_n)
    max_length_word = 'x'
    for word_max in enumerate(words):
        if len(word_max[1]) > len(max_length_word):
            max_length_word = word_max[1]
    min_length_word = 10000 * 'x'
    for word_min in enumerate(words):
        if len(word_min[1]) < len(min_length_word):
            min_length_word = word_min[1]
    all_letters = 0
    for all_letter in enumerate(words):
        all_letters = all_letters + len(all_letter[1])
    average_token_length = all_letters / len(words)
    sorted_common = common_tokens.copy()
    sorted_common.sort()
    report = {'name': profile_to_compare['name'],
              'common': common_tokens,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    return report


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int):
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """



