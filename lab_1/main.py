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
    if not isinstance(text, str):
        return None
    text=text.lower()
    punctuation_marks= """1234567890-=!@#$%^&*()_+{};:[]'"№,./<>?\|~`"""
    for i in text:
        if i in punctuation_marks:
            text=text.replace(i, '')
    tokens=text.split()
    return tokens 


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
   
    right_tokens=[]
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    for i in tokens:
        if i not in stop_words:
            right_tokens.append(i)
    return right_tokens

def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    d={}
    if not isinstance(tokens, list):
        return None
    for i in tokens:
        if not isinstance(i, str):
            return None
        if i not in d:
            d[i]=1
        else:
            d[i]+=1
    return d


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words
    :return: a list of the most common words
    """
    if not isinstance(freq_dict, dict):
        return None
    s_freq_list = sorted(freq_dict.values())
    s_dict_nd={}
    s_freq_list = s_freq_list[::-1]
    for i in s_freq_list:
        for k in freq_dict.keys():
            if freq_dict[k] == i:
                s_dict_nd[k] = freq_dict[k]
    top_n_list = s_dict_nd.keys()
    top_n_list = list(top_n_list)
    top_n_list = top_n_list[:top_n]
    return top_n_list



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
    tokens = remove_stop_words(tokens, stop_words)
    freq_dict = calculate_frequencies(tokens)
    l_p = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
    return l_p


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
    unknown_profile_top_n = get_top_n_words(unknown_profile['freq'], top_n)
    profile_to_compare_top_n = get_top_n_words(profile_to_compare['freq'], top_n)
    common_top_n = 0
    
    for i in unknown_profile_top_n:
        if i in profile_to_compare_top_n:
            common_top_n +=1 
    l_ptc= len(profile_to_compare_top_n)
    pr = common_top_n/l_ptc
    pr = round(pr, 2)
    return pr
                         
def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """

    if not isinstance(unknown_profile, dict) or not isinstance(profile_1, dict):
        return None
    if not isinstance(profile_2, dict) or not isinstance(top_n, int):
        return None
    ptc_1_tokens = compare_profiles(unknown_profile, profile_1, top_n)
    ptc_2_tokens = compare_profiles(unknown_profile, profile_2, top_n)
    name_1 = profile_1['name']
    name_2 = profile_2['name']
    if ptc_1_tokens > ptc_2_tokens:
        return name_1
    if ptc_2_tokens > ptc_1_tokens:
        return name_2


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if (not isinstance(unknown_profile, dict)
            or not isinstance(profile_to_compare, dict)
            or not isinstance(top_n, int)):
        return None
   
    top_n_words_unknown = get_top_n_words(unknown_profile["freq"], top_n)
    top_n_words_compare = get_top_n_words(profile_to_compare["freq"], top_n)
    common = []
    for word in top_n_words_compare:
        if word in top_n_words_unknown:
            common.append(word)
    sorted_common = sorted(common)
 
    score = round(len(common) / len(top_n_words_unknown), 2)

    max_length_word = max(profile_to_compare["freq"].keys(), key=len)
    min_length_word = min(profile_to_compare["freq"].keys(), key=len)

    length_of_tokens = []
    for token in profile_to_compare["freq"].keys():
        length_of_tokens.append(len(token))
    average_token_length = sum(length_of_tokens)/len(profile_to_compare["freq"].keys())
 
    report = {'name': profile_to_compare["name"],
              'common': common,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    return report



def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
     if (not isinstance(unknown_profile, dict) or not isinstance(profiles, list) or not isinstance(languages, list) or not isinstance(top_n, int)):
            return None
    reports = []
    for profile in profiles:
        if profile["name"] in languages or not languages:
            report = compare_profiles_advanced(unknown_profile, profile, top_n)
            reports.append(report)
    reports = sorted(reports, key=lambda x: x["score"], reverse=True)
    
    if not reports:
        return None
 
    list_with_only_scores = []
    for element_dict in reports:
        list_with_only_scores.append(element_dict["score"])
    max_scores = max(list_with_only_scores)
    number_of_max_scores = list_with_only_scores.count(max_scores)
    reports = sorted(reports[:number_of_max_scores], key=lambda x: x["name"])
    return reports[0]["name"]



def load_profile(path_to_file: str) -> dict or None:
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not isinstance(path_to_file, str) or not exists(path_to_file):
        return None
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        profile = json.load(json_file)
    return profile


def save_profile(profile: dict) -> int:
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict) or ("name" or "freq" or "n_words") not in profile.keys():
        return 1
    if (not isinstance(profile["name"], str)
            or not isinstance(profile["freq"], dict)
            or not isinstance(profile["n_words"], int)):
        return 1
    path_to_file = "{}.json".format(profile["name"])
    with open(path_to_file, "w", encoding="utf-8") as file:
        json.dump(profile, file)
    return 0
