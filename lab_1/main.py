"""
Lab 1
Language detection
"""
import re
def tokenize(text):
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if isinstance(text, str):
        for symbol in text:
            if not (symbol.isalpha() or symbol.isspace()):
                text = text.replace(symbol, '')
        text = text.lower().split()
        return text
    else:
        return None
    
  
 def remove_stop_words(tokens, stop_words):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not all(isinstance(s, str) for s in tokens):
        return None
    else:
        if isinstance(tokens, list) and isinstance(stop_words, list):
            cleaned_tokens = []
            for token in tokens:
                if not token in stop_words:
                    cleaned_tokens.append(token)
            return cleaned_tokens
        elif isinstance(tokens, list) and not isinstance(stop_words, list):
            return tokens


def calculate_frequencies(tokens):
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    freq_dict = {}
    if isinstance(tokens, list) and all(isinstance(s, str) for s in tokens):
        for token in tokens:
            if token in freq_dict:
                freq_dict[token] += 1
            else:
                freq_dict[token] = 1
        return freq_dict
    else:
        return None


def get_top_n_words(freq_dict, top_n):
     """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict):
        return None
    if not all(isinstance(v, int) for v in freq_dict.values()):
        return None
    if not isinstance(top_n, int):
        return None
    sorted_list = [w[0] for w in sorted(freq_dict.items(), key=lambda v: v[1], reverse = True)]
    if top_n < len(sorted_list):
        return sorted_list[:top_n]
    elif top_n >= len(sorted_list):
        return sorted_list


def create_language_profile(language, text, stop_words):
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        tokens = tokenize(text)
        cleaned_tokens = remove_stop_words(tokens, stop_words)
        freq_dict = calculate_frequencies(cleaned_tokens)
        language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
        return language_profile
    else:
        return None
 

def compare_profiles(unknown_profile, profile_to_compare, top_n):
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        freq_list1 = unknown_profile['freq']
        top_n1 = get_top_n_words(freq_list1, top_n)
        freq_list2 = profile_to_compare['freq']
        top_n2 = get_top_n_words(freq_list2, top_n)

        profiles_in_common = []
        for w in top_n1:
            if w in top_n2:  
                profiles_in_common.append(w)
        result = round(len(profiles_in_common) / len(top_n1), 2)
        return result
    else:
        return None
 

def detect_language(unknown_profile, profile_1, profile_2, top_n):
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) and isinstance(profile_2, dict) and isinstance(top_n, int):
        compare_1 = compare_profiles(unknown_profile, profile_1, top_n)
        compare_2 = compare_profiles(unknown_profile, profile_2, top_n)
        if compare_1 > compare_2:
            return profile_1['name']
        elif compare_2 > compare_1:
            return profile_2['name']
        else:
            return max(profile_1['name'], profile_2['name'])
    
    
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
