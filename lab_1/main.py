"""
Lab 1
Language detection
"""



import re
def tokenize(text: str) -> list or None:
    if isinstance(text,str):
        text2=text.lower()
        token = re.sub(r'[^\w\s]','',text2)
        token2 = re.split(r'\s', token)
        for token in token2:
            if token == '':
                token2.remove(token)
        return token2
    return None

def remove_stop_words(token2: list, stop_words: list)-> list or None:
    if isinstance(token2, list) and isinstance(stop_words, list):
        for token in token2:
            if token in stop_words:
                token2.remove(token)
        return token2
    return None
                    
def calculate_frequencies(token2: list)-> dict or None:
    if isinstance(token2, list):
        for token in token2:
            if isinstance(token,str):
                freqdict = {}
                for x in token2:
                    if x in freqdict:
                        freqdict[x]+=1
                    else:
                        freqdict[x]=1
                return freqdict
            return None
    return None

            
def get_top_n_words(freqdict: dict, top_n:int)-> list or None:
    if isinstance(freqdict, dict) and isinstance(top_n, int):
        top_dict = dict(sorted(freqdict.items(), key=lambda kv: kv[1], reverse=True))
        freqdict = list(top_dict)
        return freqdict[:top_n]
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
