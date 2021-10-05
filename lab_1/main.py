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

    else:
        text = text.lower()
        cleaned_text = ''
        for x in text:
            if x.isalpha() or x.isspace():
                cleaned_text += x
        tokens = cleaned_text.split()
        return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not len(tokens):
        return None

    elif not isinstance(stop_words, list):
        return tokens

    else:
        cleaned_tokens = [word for word in tokens if word not in stop_words]
        return cleaned_tokens


def calculate_frequencies(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not (isinstance(tokens, list)
            and all(isinstance(t, str) for t in tokens)):
        return None

    else:
        freq_dict = {}
        for token in tokens:
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
    if not (isinstance(freq_dict, dict)
            and isinstance(top_n, int)
            and all(isinstance(v, int) for v in freq_dict.values())):
        return None

    else:
        freq_list = sorted(freq_dict.items(),
                           key=lambda pair: pair[1], reverse=True)
        sorted_words = []
        for pair in freq_list:
            sorted_words.append(pair[0])
        if top_n <= len(freq_list):
            return sorted_words[:top_n]
        return sorted_words


def create_language_profile(language: str,
                            text: str,
                            stop_words: list) -> dict or None:
    """
    Creates a language profile
    :param language: a language
    :param text: a text
    :param stop_words: a list of stop words
    :return: a dictionary with three keys – name, freq, n_words
    """
    if not (isinstance(language, str)
            and isinstance(text, str)
            and isinstance(stop_words, list)):
        return None

    elif not (all(isinstance(s, str) for s in stop_words) or stop_words == []):
        return None

    else:
        tokens = tokenize(text)
        cleaned_tokens = remove_stop_words(tokens, stop_words)
        freq_dict = calculate_frequencies(cleaned_tokens)
        lang_profile = {'name': language,
                        'freq': freq_dict, 'n_words': len(freq_dict)}
        return lang_profile


def compare_profiles(unknown_profile: dict,
                     profile_to_compare: dict,
                     top_n: int) -> float or None:
    """
    Compares profiles and calculates the distance using top n words
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: the distance
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None

    else:
        top_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
        top_profile_to_compare = get_top_n_words(profile_to_compare['freq'], top_n)
        tokens_in_common = []
        for i in top_unknown_profile:
            if i in top_profile_to_compare:
                tokens_in_common.append(i)
        distance = round(len(tokens_in_common) / len(top_unknown_profile), 2)
        return distance


def detect_language(unknown_profile: dict,
                    profile_1: dict,
                    profile_2: dict,
                    top_n: int) -> str or None:
    """
    Detects the language of an unknown profile
    :param unknown_profile: a dictionary
    :param profile_1: a dictionary
    :param profile_2: a dictionary
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_1, dict)
            and isinstance(profile_2, dict)
            and isinstance(top_n, int)):
        return None

    comparison_1 = compare_profiles(unknown_profile, profile_1, top_n)
    comparison_2 = compare_profiles(unknown_profile, profile_2, top_n)

    if comparison_1 > comparison_2:
        language = profile_1['name']
        return language

    elif comparison_2 > comparison_1:
        language = profile_2['name']
        return language

    elif comparison_1 == comparison_2:
        language = sorted(profile_1['name'], profile_2['name'])
        return language


def compare_profiles_advanced(unknown_profile: dict,
                              profile_to_compare: dict,
                              top_n: int) -> list or None:
    """
    Compares profiles and calculates some advanced parameters
    :param unknown_profile: a dictionary
    :param profile_to_compare: a dictionary
    :param top_n: a number of the most common words
    :return: a dictionary with 7 keys – name, score, common, sorted_common, max_length_word,
    min_length_word, average_token_length
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profile_to_compare, dict)
            and isinstance(top_n, int)):
        return None

    unknown_top_n = get_top_n_words(unknown_profile['freq'], top_n)
    compare_top_n = get_top_n_words(profile_to_compare['freq'], top_n)
    common = []
    for word in compare_top_n:
        if word in unknown_top_n:
            common.append(word)
    score = compare_profiles(unknown_profile, profile_to_compare, top_n)
    words = profile_to_compare['freq'].keys()
    max_length_word = max(words, key=len)
    min_length_word = min(words, key=len)
    average_token_length = sum(len(word) for word in words) / len(words)
    sorted_common = sorted(common)
    report = {'name': profile_to_compare['name'],
              'common': common,
              'score': score,
              'max_length_word': max_length_word,
              'min_length_word': min_length_word,
              'average_token_length': average_token_length,
              'sorted_common': sorted_common}
    return report


def detect_language_advanced(unknown_profile: dict,
                             profiles: list,
                             languages: list,
                             top_n: int) -> str or None:
    """
    Detects the language of an unknown profile within the list of possible languages
    :param unknown_profile: a dictionary
    :param profiles: a list of dictionaries
    :param languages: a list of possible languages
    :param top_n: a number of the most common words
    :return: a language
    """
    if not (isinstance(unknown_profile, dict)
            and isinstance(profiles, list)
            and isinstance(languages, list)
            and isinstance(top_n, int)):
        return None

    lang_score = {}
    for profile_to_compare in profiles:

        if (profile_to_compare['name'] in languages) or not languages:
            comparison = compare_profiles_advanced(unknown_profile,
                                                   profile_to_compare, top_n)
            lang_score[comparison['name']] = comparison['score']

    if lang_score == {}:
        return None

    else:
        sorted_languages = []
        for name, score in lang_score.items():
            if score == max(lang_score.values()):
                sorted_languages.append(name)
        sorted_languages = sorted(sorted_languages)
        return sorted_languages[0]
