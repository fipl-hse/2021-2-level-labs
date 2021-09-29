"""
Lab 1
Language detection
"""

import re
def tokenize(text: str) -> list or None:
    if isinstance(text,str):
        text2=text.lower()
        token = re.sub(r'[^\w\s\d+]','',text2)
        token2 = re.split(r'\s', token)
        for token in token2:
            if token == '':
                token2.remove(token)
        return token2
    return None

def remove_stop_words(token2: list, stop_words: list)-> list or None:
    if isinstance(token2, list) and isinstance(stop_words, list):
        if token2:
            for token in enumerate(token2):
                if token[1] in stop_words:
                    token2[token[0]] = ' '
            while ' ' in token2:
                token2.remove(' ')
            return token2
        return None
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
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        tokens = tokenize(text)
        tokens = remove_stop_words(tokens, stop_words)
        frq_dict = calculate_frequencies(tokens)
        language_profile = {'name':language, 'freq': frq_dict, 'n_words': len(frq_dict)}
        return language_profile
    return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict)\
            and isinstance(top_n, int):
        top_n_words_unk = get_top_n_words(unknown_profile['freq'], top_n)
        top_n_words_comp = get_top_n_words(profile_to_compare['freq'],top_n)
        common_elements = 0
        for element in top_n_words_unk:
            if element in top_n_words_comp:
                common_elements+= 1
                freq_common = common_elements/len(top_n_words_unk)
                return round(freq_common, 2)
    return None

def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) \
            and isinstance(profile_2, dict) and isinstance(top_n, int):
            freq_common1 = compare_profiles(unknown_profile, profile_1, top_n)
            freq_common2 = compare_profiles(unknown_profile, profile_2, top_n)
            if freq_common1 > freq_common2:
                return profile_1['name']
            if freq_common2 > freq_common1:
                return profile_2['name']
            if freq_common1 == freq_common2:
                languages_names = [profile_1['name'], profile_2['name']]
                languages_names.sort()
            return languages_names[0]
    return None



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
