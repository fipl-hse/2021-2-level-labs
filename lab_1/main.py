"""
Lab 1
Language detection
"""


def tokenize(text: str) -> list or None:

    english_text = """A man walks into a bar and orders a glass of water. 
                          The bartender points a gun at him and the man thanks him and leaves.
                          Why did the man thank the bartender?"""

    german_text = """Stell dir vor, du bist der Kapitän eines Frachtschiffes, das 30 Meter lang und 5 Meter breit ist.
                         Voll beladen hat es einen Tiefgang von 2 Metern, nicht beladen nur von einem Meter. 
                         Seine Höchstgeschwindigkeit betägt 18 Knoten. Wie alt ist der Kapitän?"""

    unknown_text = """A man is lying in his bed, trying to sleep. 
                          He picks up the phone and makes a call.
                          He waits for a while and hangs up before anyone could answer the phone.
                          Then he sleeps peacefully."""
    import re

    english_text_lower = english_text.lower()
    german_text_lower = german_text.lower()
    unknown_text_lower = unknown_text.lower()

    english_text_lower = re.sub(r'[^a-z ]', '', str(english_text_lower))
    english_text_tokens = english_text_lower.split()

    german_text_lower = re.sub(r'[^a-zäöüß ]', '', str(german_text_lower))
    german_text_tokens = german_text_lower.split()

    unknown_text_lower = re.sub(r'[^a-zäöüß ]', '', str(unknown_text_lower))
    unknown_text_tokens = unknown_text_lower.split()

    print(english_text_tokens)
    print(german_text_tokens)
    print(unknown_text_tokens)


    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """



def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    pass


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
