"""
Lab 1
Language detection
"""


def tokenize(text: str):
    if isinstance(text, str):
        text = text.lower()
        text = text.replace("'", ' ')
        n_text = ''
        for i in range(len(text)):
            if text[i].isalpha() or text[i] == ' ' or text[i] == '\n':
                n_text += text[i]
            else:
                text.replace(text[i], ' ')
        t_tokens = n_text.split()
        return t_tokens
    return None
    pass

def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    if isinstance(tokens, list) and isinstance(stop_words, list):
        no_stop_words = []
        for token in tokens:
            if token not in stop_words:
                no_stop_words.append(token)
        return no_stop_words
    return None
    pass


def calculate_frequencies(tokens: list) -> dict or None:
    if isinstance(tokens, list):
        f_dict = {}
        for token in tokens:
            if type(token) != str:
                return None
            if token not in f_dict:
                f_dict[token] = 1
            else:
                f_dict[token] += 1
        return f_dict
    return None
    pass


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        n_dict = {k: freq_dict[k] for k in sorted(freq_dict, key=freq_dict.get, reverse=True)}
        top_lst = list(n_dict.keys())
        top = top_lst[:top_n]
        return top
    return None
    pass


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        tokens = tokenize(text)
        no_stop_words = remove_stop_words(tokens, stop_words)
        f_dict = {}
        f_dict = calculate_frequencies(no_stop_words)
        l_profile = {'name': language, 'freq': f_dict, 'n_words': len(f_dict)}
        return l_profile
    return None
    pass


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        for k in unknown_profile.keys():
            if k == 'freq':
                d_1 = unknown_profile['freq']
        for k in profile_to_compare.keys():
            if k == 'freq':
                d_2 = profile_to_compare['freq']
        top_unk = get_top_n_words(d_1, top_n)
        top_comp = get_top_n_words(d_2, top_n)
        equal = 0
        for k_u in top_unk:
            for k_c in top_comp:
                if k_u == k_c:
                    equal += 1
        eq_per = round((equal / len(top_unk)), 2)
        return eq_per
    return None
    pass


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) and isinstance(profile_2, dict) and isinstance(
            top_n, int):
        eq_per_1 = compare_profiles(unknown_profile, profile_1, top_n)
        eq_per_2 = compare_profiles(unknown_profile, profile_2, top_n)
        if eq_per_1 > eq_per_2:
            detected_language = profile_1.get('name')
        elif eq_per_2 > eq_per_1:
            detected_language = profile_2.get('name')
        return detected_language
    return None
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
