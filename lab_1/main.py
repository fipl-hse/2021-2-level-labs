"""
Lab 1
Language detection
"""
import json
from os.path import exists


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


def remove_stop_words(tokens, stop_words):
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if isinstance(tokens, list) and tokens != []:
        if all(isinstance(s, str) for s in tokens):
            if isinstance(stop_words, list):
                cleaned_tokens = []
                for token in tokens:
                    if token not in stop_words:
                        cleaned_tokens.append(token)
                return cleaned_tokens
            else:
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


def get_top_n_words(freq_dict, top_n):
    if not isinstance(freq_dict, dict):
        return None
    if not all(isinstance(v, int) for v in freq_dict.values()):
        return None
    if not isinstance(top_n, int):
        return None
    srtd_list = [wrd[0] for wrd in sorted(freq_dict.items(), key=lambda val: val[1], reverse=True)]
    if top_n < len(srtd_list):
        return srtd_list[:top_n]
    elif top_n >= len(srtd_list):
        return srtd_list


def create_language_profile(language, text, stop_words):
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        tokens = tokenize(text)
        cleaned_tokens = remove_stop_words(tokens, stop_words)
        freq_dict = calculate_frequencies(cleaned_tokens)
        language_profile = {'name': language, 'freq': freq_dict, 'n_words': len(freq_dict)}
        return language_profile


def compare_profiles(unknown_profile, profile_to_compare, top_n):
    if ( 
        isinstance(unknown_profile, dict) 
        and isinstance(profile_to_compare, dict) 
        and isinstance(top_n, int)
    ):
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


def detect_language(unknown_profile, profile_1, profile_2, top_n):
    if ( 
        isinstance(unknown_profile, dict) 
        and isinstance(profile_1, dict) 
        and isinstance(profile_2, dict) 
        and isinstance(top_n, int)
    ):
        compare_1 = compare_profiles(unknown_profile, profile_1, top_n)
        compare_2 = compare_profiles(unknown_profile, profile_2, top_n)
        if compare_1 > compare_2:
            return profile_1['name']
        elif compare_2 > compare_1:
            return profile_2['name']
        else:
            return max(profile_1['name'], profile_2['name'])


def compare_profiles_advanced(unknown_profile, profile_to_compare, top_n):
    if (
        isinstance(unknown_profile, dict) 
        and isinstance(profile_to_compare, dict) 
        and isinstance(top_n, int)
    ):
        report = {}
        top_words_unk = get_top_n_words(unknown_profile['freq'], top_n)
        top_words_comp = get_top_n_words(profile_to_compare['freq'], top_n)
        common_words = []
        for word in top_words_comp:
            if word in top_words_unk:
                common_words.append(word)
        score = compare_profiles(unknown_profile, profile_to_compare, top_n)
        tokens = profile_to_compare['freq'].keys()
        max_length_word = max(tokens, key=len)
        min_length_word = min(tokens, key=len)
        all_tokens_len = len(''.join(tokens))
        average_token_length = all_tokens_len / len(tokens)
        sorted_common = sorted(common_words)
        report['name'] = profile_to_compare['name']
        report['common'] = common_words
        report['score'] = score
        report['max_length_word'] = max_length_word
        report['min_length_word'] = min_length_word
        report['average_token_length'] = average_token_length
        report['sorted_common'] = sorted_common
        return report


def detect_language_advanced(unknown_profile, profiles, languages, top_n):
    if (
        isinstance(unknown_profile, dict) 
        and isinstance(profiles, list) 
        and isinstance(languages, list) 
        and isinstance(top_n, int)
    ):
        dict_lang_score = {}
        for profile_to_compare in profiles:
            if languages == []:
                compare = compare_profiles_advanced(unknown_profile, profile_to_compare, top_n)
                dict_lang_score[compare['name']] = compare['score']
            else:
                if profile_to_compare['name'] in languages:
                    compare = compare_profiles_advanced(unknown_profile, profile_to_compare, top_n)
                    dict_lang_score[compare['name']] = compare['score']
        if dict_lang_score != {}:
            sorted_lang = []
            for lang, score in dict_lang_score.items():
                if score == max(dict_lang_score.values()):
                    sorted_lang.append(lang)
            sorted_lang = sorted(sorted_lang)
        else:
            return None
        return sorted_lang[0]


def load_profile(path_to_file):
    """
    Loads a language profile
    :param path_to_file: a path
    :return: a dictionary with three keys – name, freq, n_words
    """
    if isinstance(path_to_file, str):
        if exists(path_to_file):
            with open(path_to_file, mode='r', encoding='UTF-8') as file:
                profile = json.load(file)
                return profile
        return None
    return None


def save_profile(profile):
    """
    Saves a language profile
    :param profile: a dictionary
    :return: 0 if everything is ok, 1 if not
    """
    if not isinstance(profile, dict):
        return 1
    if not (
        isinstance(profile['name'], str) 
        or isinstance(profile['freq'], dict) 
        or isinstance(profile['n_words'], int)
    ):
        return 1
    profile_dict = '{}.json'.format(profile['name'])
    with open(profile_dict, mode='w', encoding='UTF-8') as file:
        json.dump(profile, file)
        return 0
