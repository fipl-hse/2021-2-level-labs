"""
Lab 1
Language detection
"""
import re

def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """

    if not isinstance(text, str):
        return None

    text = re.split(r"[^\w\s]", text)
    text = "".join(text)
    text = text.lower()
    tokens = re.findall(r"\w+", text)
    return tokens


unknown_text = open('unknown.txt', encoding='utf-8').read()
en_text = open('en.txt', encoding='utf-8').read()
de_text = open('de.txt', encoding='utf-8').read()


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """

    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None

    filt_tokens = []
    for token in tokens:
        if token not in stop_words:
            filt_tokens.append(token)
    return filt_tokens

tokens_en = tokenize(en_text)
tokens_de = tokenize(de_text)
tokens_unknown = tokenize(unknown_text)

stop_words_en = ['a', 'an', 'the', 'and']
stop_words_de = ['der', 'das', 'die', 'ein', 'eine']
stop_words_unknown = []


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """

    if not isinstance(tokens, list):
        return None

    freq_dict = {}
    for word in tokens:
        if word not in freq_dict:
            freq_dict[word] = 1
        else:
            freq_dict[word] += 1
    return freq_dict

tokens_en = remove_stop_words(tokens_en, stop_words_en)
tokens_de = remove_stop_words(tokens_de, stop_words_de)
tokens_unknown = remove_stop_words(tokens_unknown, stop_words_unknown)


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """

    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return None

    words = len(freq_dict)
    freq_val = reversed(sorted(freq_dict.values()))
    sorted_freq = {}

    for i in freq_val:
        for k in freq_dict.keys():
            if freq_dict[k] == i:
                sorted_freq[k] = freq_dict[k]

    if top_n > words:
        top_words = sorted_freq
        return top_words
    if top_n < words:
        top_words = list(sorted_freq.keys())[:(top_n)]
        return top_words



freq_dict_en = calculate_frequencies(tokens_en)
freq_dict_de = calculate_frequencies(tokens_de)
freq_dict_unknown = calculate_frequencies(tokens_unknown)

new_dicts_en = {v: k for k, v in freq_dict_en.items()}
new_dicts_de = {v: k for k, v in freq_dict_de.items()}
new_dicts_unknown = {v: k for k, v in freq_dict_unknown.items()}

top_n_en = len(new_dicts_en)
top_n_de = len(new_dicts_de)
top_n_unknown = len(new_dicts_unknown)


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """

    if not isinstance(language, str) or not isinstance(text, str) or not isinstance(stop_words, list):
        return None

    for i in top_words_en:
        for en_word in freq_dict_en:
            if i == en_word:
                val_list = list(reversed(sorted(freq_dict_en.values())))
                en_top_n = dict(zip(top_words_en, val_list))
    for i in top_words_de:
        for de_word in freq_dict_de:
            if i == de_word:
                val_list = list(reversed(sorted(freq_dict_de.values())))
                de_top_n = dict(zip(top_words_de, val_list))
    for i in top_words_unknown:
        for unknown_word in freq_dict_unknown:
            if i == unknown_word:
                val_list = list(reversed(sorted(freq_dict_unknown.values())))
                unknown_top_n = dict(zip(top_words_unknown, val_list))

    en = {"name": language_en,
          "freq": en_top_n,
          "n_words": len(en_top_n)}

    de = {"name": language_de,
          "freq": de_top_n,
          "n_words": len(de_top_n)}

    unknown = {"name": language_unknown,
               "freq": unknown_top_n,
               "n_words": len(unknown_top_n)}

    language_profile = {}

    for word in stop_words:
        if word in text:
            language_profile = {"name": language}

        language_val = list(language_profile.values())
        en_val = list(en.values())
        de_val = list(de.values())

        for value in language_val:
            if value in en_val:
                en_profile = en
                return en_profile
            if value in de_val:
                de_profile = de
                return de_profile
            else:
                unknown_profile = unknown
                return unknown_profile

language_en = 'en'
language_de = 'de'
language_unknown = 'unknown'

en_text = str(tokenize(en_text))
de_text = str(tokenize(de_text))
unknown_text = str(tokenize(unknown_text))

en_stop_words = remove_stop_words(tokens_en, stop_words_en)
de_stop_words = remove_stop_words(tokens_de, stop_words_de)
unknown_stop_words = remove_stop_words(tokens_unknown, stop_words_unknown)

top_words_en = get_top_n_words(freq_dict_en, top_n_en)
top_words_de = get_top_n_words(freq_dict_de, top_n_de)
top_words_unknown = get_top_n_words(freq_dict_unknown, top_n_unknown)

top_n_en = len(get_top_n_words(freq_dict_en, top_n_en))
top_n_de = len(get_top_n_words(freq_dict_de, top_n_de))
top_n_unknown = len(get_top_n_words(freq_dict_unknown, top_n_unknown))

freq_dict_en = calculate_frequencies(tokens_en)
freq_dict_de = calculate_frequencies(tokens_de)
freq_dict_unknown = calculate_frequencies(tokens_unknown)


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_to_compare, dict) or not isinstance(top_n, int):
        return None

    unk = unknown_profile['freq']
    lan = profile_to_compare['freq']

    comp = []
    for i in unk:
        for word in lan:
            if i == word:
                comp.append(i)

    score = round(len(comp)/top_n, 1)
    return score

top_n_en = len(get_top_n_words(freq_dict_en, top_n_en))
top_n_de = len(get_top_n_words(freq_dict_de, top_n_de))
top_n_unknown = len(get_top_n_words(freq_dict_unknown, top_n_unknown))

en_profile = create_language_profile(language_en, en_text, en_stop_words)
de_profile = create_language_profile(language_de, de_text, de_stop_words)
unknown_profile = create_language_profile(language_unknown, unknown_text, unknown_stop_words)


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict) \
            or not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None

    if score_en > score_de:
        unknown_profile['name'] = profile_1['name']
        language_unknown = language_en
        return language_unknown
    if score_en < score_de:
        unknown_profile['name'] = profile_2['name']
        language_unknown = language_de
        return language_unknown
    else:
        lang = [language_en, language_de]
        prof = {profile_1: language_en, profile_2: language_de}
        lang.sort()
        for i in prof:
            if i == lang[0]:
                language_unknown = i
                return language_unknown

score_en = compare_profiles(unknown_profile, en_profile, top_n_en)
score_de = compare_profiles(unknown_profile, de_profile, top_n_de)

en_profile = create_language_profile(language_en, en_text, en_stop_words)
de_profile = create_language_profile(language_de, de_text, de_stop_words)
unknown_profile = create_language_profile(language_unknown, unknown_text, unknown_stop_words)

top_n_unknown = len(get_top_n_words(freq_dict_unknown, top_n_unknown))


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
