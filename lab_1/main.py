"""
Lab 1
Language detection
"""
import re
def tokenize(text):
    while isinstance(text, str):
        tokens = []
        contemp_string = ''
        text = text.lower()
        text = re.sub(r'[^\w\s]','', text)
        text = text.split()
        for token in text:
            if token.isalpha() or token.isdigit():
                tokens.append(token)
            elif token.isalnum():
                for symbol in token:
                    if symbol.isalpha():
                        contemp_string += symbol
                tokens.append(contemp_string)
                contemp_string = ''
        return tokens
    else:
        return None


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
