"""
Lab 1
Language detection
"""
import re
import nltk

def tokenize(text: str) -> list or None:

    text = re.split(r"[^\w\s]", text)
    text = "".join(text)
    text = text.lower()
    tokens = re.findall(r"\w+", text)
    return tokens


unknown_text = open('unknown.txt', encoding='utf-8').read()
en_text = open('en.txt', encoding='utf-8').read()
de_text = open('de.txt', encoding='utf-8').read()


# print(tokenize(en_text))
# print(tokenize(de_text))
# print(tokenize(unknown_text))

def remove_stop_words(tokens: list, stop_words: list) -> list or None:

    filt_tokens = []
    for token in tokens:
        if token not in stop_words:
            filt_tokens.append(token)
            tokens = filt_tokens
    return tokens


tokens_en = tokenize(en_text)
tokens_de = tokenize(de_text)
tokens_unknown = tokenize(unknown_text)

stop_words_en = nltk.corpus.stopwords.words('english')
stop_words_de = nltk.corpus.stopwords.words('german')
stop_words_unknown = []


# print(remove_stop_words(tokens_en, stop_words_en))
# print(remove_stop_words(tokens_de, stop_words_de))
# print(remove_stop_words(tokens_unknown, stop_words_unknown))


def calculate_frequencies(tokens: list) -> dict or None:

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


# print(calculate_frequencies(tokens_en))
# print(calculate_frequencies(tokens_de))
# print(calculate_frequencies(tokens_unknown))

def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:

    words = len(freq_dict)
    freq_val = reversed(sorted(freq_dict.values()))
    sorted_freq = {}

    for i in freq_val:
        for k in freq_dict.keys():
            if freq_dict[k] == i:
                sorted_freq[k] = freq_dict[k]

    sf_val = [sorted_freq.values()]

    if top_n > words:
        top_words = sorted_freq
        return top_words
    if top_n < words:
        s = list(sorted_freq.keys())[:(top_n)]
        v = list(sorted_freq.values())
        top_words = dict(zip(s, v))
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


# print(get_top_n_words(freq_dict_en, top_n_en))
# print(get_top_n_words(freq_dict_de, top_n_de))
# print(get_top_n_words(freq_dict_unknown, top_n_unknown))


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
