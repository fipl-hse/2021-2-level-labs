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
    if not isinstance (text, str): 
       return None
    else:
       text = text.lower()
       text = re.sub(r'[^\w\s]', '', text)
       text = text.split()
       return text
def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
     Removes stop words
     :param tokens: a list of tokens
     :param stop_words: a list of stop words
     :param stop_words.words(language): a list of stop words
     :return: a list of tokens without stop words
     """
    if not all(isinstance(s, str) for s in stop_words):
        return tokens

    if checkIfTokensAreValid(tokens):
        filteredTokens = [x for x in tokens if x not in stop_words]
        print(filteredTokens)
        return filteredTokens        
    else:
        return None

def checkIfTokensAreValid(tokens: list) -> bool:
    """
    Checks if list contains letter-only strings without any numbers or special characters. 
    :param tokens: a list of strngs (tokens)
    :return: boolean value indicating whether list contains letter-only strings without any special characters
    """
    if all(isinstance(s, str) for s in tokens):
        for token in tokens:
            if not token.isalpha():
                return False
    return True


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None 
    freq_dict = {}
    
    for token in tokens:
        if not isinstance(token, str):
             return None
        if token not in freq_dict:
             freq_dict[token] = 1
        else:
             freq_dict[token] += 1
    return freq_dict


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
   if not isinstance (freq_dict, dict):
        return None
    freq_dict = sorted(freq_dict.items(), key=lambda x: -x[1])
    most_common_words = list(freq_dict)
    most_common_words =  most_common_words [:top_n]
    return most_common_words
    


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
     if not isinstance(language, str) or not text or not isinstance(stop_words, list):
         return None
    new_tokens = tokenize(text)
    new_tokens = remove_stop_words(new_tokens, stop_words)
    freq_dict = calculate_frequencies(new_tokens)
    profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return profile



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
