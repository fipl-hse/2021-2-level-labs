"""
Lab 1
Language detection
"""


def tokenize(text):
    text = text.lower()
    preprocessed = ''
    for i in range(len(text)):
        if text[i].isalnum() or text[i] == ' ':
            preprocessed += text[i]
    tokens = preprocessed.split()
    return tokens
text = input('Enter the text: ')
tokenize(text)



def remove_stop_words(tokens, stop_words):
    new_tokens = []
    for token in tokens:
        if token not in stop_words:
            new_tokens.append(token)
    print (new_tokens)
    return new_tokens

stop_words = ['a','the','is']
remove_stop_words(tokenize(text),stop_words)


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    pass


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    pass


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def calculate_distance(profile_1: dict, profile_2: dict, top_n: int) -> float or None:
    """
    Calculates the distance using top n words
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a proportion
    """
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :return: a language
    """
    pass


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :return: a language
    """
    pass


def create_report(unknown_profile: dict, profiles: list, languages: list) -> list or None:
    """
    Creates a report on language detection
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :return: a list of dictionaries with two keys – name, score
    """
    pass


def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    pass


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    pass
