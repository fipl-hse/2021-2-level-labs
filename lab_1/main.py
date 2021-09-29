"""
Lab 1
Language detection
"""


def tokenize(text: str):
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    text = text.lower()
    text = text.replace("'", ' ')
    n_text = ''
    for i in text:
        if i.isalpha() or i == ' ' or i == '\n':
            n_text += i
        else:
            text.replace(i, ' ')
    t_tokens = n_text.split()
    return t_tokens



def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list):
        return None
    if not isinstance(stop_words, list):
        return None
    no_stop_words = []
    for token in tokens:
        if token not in stop_words:
            no_stop_words.append(token)
    return no_stop_words



def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    f_dict = {}
    for token in tokens:
        if not isinstance(token, str):
            return None
        if token not in f_dict:
            f_dict[token] = 1
        else:
            f_dict[token] += 1
    return f_dict




def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict):
        return None
    if not isinstance(top_n, int):
        return None
    n_dict = {k: freq_dict[k] for k in sorted(freq_dict, key=freq_dict.get, reverse=True)}
    top_lst = list(n_dict.keys())
    top = top_lst[:top_n]
    return top




def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(language, str):
        return None
    if not isinstance(text, str):
        return None
    if not isinstance(stop_words, list):
        return None
    tokens = tokenize(text)
    no_stop_words = remove_stop_words(tokens, stop_words)
    f_dict = {}
    f_dict = calculate_frequencies(no_stop_words)
    l_profile = {'name': language, 'freq': f_dict, 'n_words': len(f_dict)}
    return l_profile


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_to_compare, dict):
        return None
    if not isinstance(top_n, int):
        return None
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



def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not isinstance(unknown_profile, dict):
        return None
    if not isinstance(profile_1, dict):
        return None
    if not isinstance(profile_2, dict):
        return None
    if not isinstance(top_n, int):
        return None
    eq_per_1 = compare_profiles(unknown_profile, profile_1, top_n)
    eq_per_2 = compare_profiles(unknown_profile, profile_2, top_n)
    detected_language_1 = profile_1.get('name')
    detected_language_2 = profile_2.get('name')
    if eq_per_1 > eq_per_2:
        return detected_language_1
    if eq_per_2 > eq_per_1:
        return detected_language_2
    if eq_per_1 == eq_per_2:
        detected_languages = [detected_language_1, detected_language_2]
        detected_languages.sort()
        return detected_languages[0]



# def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict,
#                               top_n: int) -> dict or None:
#     if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) \
#             and isinstance(top_n, int):
#         for k in unknown_profile.keys():
#             if k == 'freq':
#                 d_1 = unknown_profile['freq']
#         for k in profile_to_compare.keys():
#             if k == 'freq':
#                 d_2 = profile_to_compare['freq']
#         top_unk = get_top_n_words(d_1, top_n)
#         top_comp = get_top_n_words(d_2, top_n)
#         equal = 0
#         equal_lst = []
#         for k_u in top_unk:
#             for k_c in top_comp:
#                 if k_u == k_c:
#                     equal += 1
#                     equal_lst.append(k_u)
#         top_e_lst = sorted(equal_lst[:top_n])
#         eq_per = equal / len(top_unk)
#         letters = ''.join(list(d_2.keys()))
#         count = len(letters) / len(list(d_2.keys()))
#         adv_profile = {'name' : profile_to_compare['name'], 'common' : top_e_lst,
#                        'score' : eq_per, 'max_length_word' : max(list(d_2.keys()), key=len),
#                        'min_length_word' : min(list(d_2.keys()), key=len), 'average_token_length' : count,
#                        'sorted_common': sorted(top_e_lst)}
#         return adv_profile
#     return None

# def detect_language_advanced(unknown_profile: dict, profiles: list,
#                         languages: list, top_n: int) -> str or None:
#     if isinstance(unknown_profile, dict) and isinstance(profiles, list) \
#         and isinstance(languages, list) and isinstance(top_n, int):
#         profiles_c = []
#         for i in profiles:
#             if i['name'] in languages:
#                 profiles_c.append(i)
#         score_lst = []
#         for e in profiles_c:
#             dict_score = compare_profiles_advanced(unknown_profile, e, top_n)
#             eq_per = dict_score['score']
#             score_lst.append(eq_per)
#         maximal_score = max(score_lst, key=lambda i: int(i))
#         for e in profiles_c:
#             if e['score'] == maximal_score:
#                 detected_language = e['name']
#         return detected_language
#     return None


#def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
  #  pass


#def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    #pass
