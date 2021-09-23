"""
Lab 1
Language detection
"""

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
    try:
        text_new = ""
        for i in text:
            if i not in string.punctuation:
                text_new += i

        text_new = text_new.lower()
        text_new = text_new.split()

        return text_new
    except:
        return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    tokens_update = ""

    try:
        for word in tokens:
            if word not in stop_words:
                tokens_update += word + " "

        tokens_update = tokens_update.split()

        return tokens_update
    except:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    freq = {}
    try:
        for word in tokens:
            if word in list(freq.keys()):
                freq[word] += 1
            else:
                freq[word] = 1
        return freq
    except:
        return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    most_common = []
    freq_dict_temp = dict(freq_dict)
    chart = sorted(list(freq_dict.values()), reverse=True)
    chart = chart[:top_n]
    try:
        for i in chart:
            word = list(freq_dict_temp.keys())[list(freq_dict_temp.values()).index(i)]
            most_common.append(word)
            freq_dict_temp.pop(word)
        return most_common
    except:
        return None


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


with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'en.txt'), 'r', encoding='utf-8') as file_to_read:
    en_text = file_to_read.read()

with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'de.txt'), 'r', encoding='utf-8') as file_to_read:
    de_text = file_to_read.read()

with open(os.path.join(PATH_TO_TEXTS_FOLDER, 'unknown.txt'), 'r', encoding='utf-8') as \
        file_to_read:
    unknown_text = file_to_read.read()

english = tokenize(en_text)
stop_words_en = []
english = remove_stop_words(english, stop_words_en)
en_freq = calculate_frequencies(english)

german = tokenize(de_text)
stop_words_de = []
german = remove_stop_words(german, stop_words_de)
de_freq = calculate_frequencies(german)

unknown = tokenize(unknown_text)
stop_words_unknown = []
unknown = remove_stop_words(unknown, stop_words_unknown)
unknown_freq = calculate_frequencies(unknown)