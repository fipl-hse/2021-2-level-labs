"""
Lab 1
Language detection
"""

import re

def tokenize(text: str) -> list or None:
    if isinstance(text, str):
        text = text.lower()
        string_with_tokens = ""
        for i in text:
            if i.isalpha() or i.isspace():
                string_with_tokens += i
        tokens = string_with_tokens.split()
        return tokens
    else:
        return None


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    try:
        for i in tokens:
            if isinstance(i, str):
                tokens = [i for i in tokens if i not in stop_words]
                return tokens
            else:
                return None
    except:
        return None


def calculate_frequencies(tokens: list) -> dict or None:
    print(tokens)
    if type(tokens) is list:
        for i in tokens:
            if isinstance(i, str):
                freq_dict = {i: tokens.count(i) for i in tokens}
                return freq_dict
            else:
                return None


def get_top_n_words(freq_dict: dict, top_n: int) -> list or None:
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        if freq_dict != {} and top_n > 0:
            new_dict = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
            count = 1
            top_list = []
            first, snd = zip(*new_dict)
            for i in first:
                if count <= top_n:
                    top_list.append(i)
                    count += 1
                if count > top_n:
                    break
            return top_list
        else:
            return []
    else:
        return None


def create_language_profile(language: str, text: str, stop_words: list) -> dict or None:
    first_step = tokenize(text)
    second_step = remove_stop_words(first_step, stop_words)
    freq_dict = calculate_frequencies(second_step)
    if isinstance(language, str) and isinstance(text, str) and isinstance(stop_words, list):
        language_profile = {"name": language,
                            "freq": freq_dict,
                            "n_words": len(freq_dict)}
        return language_profile
    else:
        return None


def compare_profiles(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> float or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        top_n_common_words = []
        top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
        top_n_words_known_profile = get_top_n_words(profile_to_compare['freq'],top_n)
        for i in top_n_words_unknown_profile:
            if i in top_n_words_known_profile:
                top_n_common_words.append(i)
        intersecting_words = len(top_n_common_words)/len(top_n_words_unknown_profile)
        return round(float(intersecting_words), 2)
    else:
        return None


def detect_language(unknown_profile: dict, profile_1: dict, profile_2: dict, top_n: int) -> str or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_1, dict) and isinstance(profile_2, dict) and isinstance(top_n, int):
        first_intersecting_words = compare_profiles(unknown_profile, profile_1, top_n)
        second_intersecting_words = compare_profiles(unknown_profile,profile_2,top_n)
        if first_intersecting_words > second_intersecting_words:
            return profile_1['name']
        if second_intersecting_words > first_intersecting_words:
            return profile_2['name']
        else:
            sorted_profiles =[profile_1['name'], profile_2['name']].sort()
            return sorted_profiles[0]
    else:
        return None


def compare_profiles_advanced(unknown_profile: dict, profile_to_compare: dict, top_n: int) -> list or None:
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        common = []
        top_n_words_unknown_profile = get_top_n_words(unknown_profile['freq'], top_n)
        top_n_words_known_profile = get_top_n_words(profile_to_compare['freq'], top_n)
        for i in top_n_words_known_profile:
            if i  in top_n_words_unknown_profile:
                common.append(i)
        sorted_common = sorted(common)
        score = (len(common) / len(top_n_words_known_profile))
        profile_to_compare_keys = list(profile_to_compare['freq'].keys())
        sorted_keys = sorted(profile_to_compare_keys,key=len)
        max_length_word = sorted_keys [-1]
        min_length_word = sorted_keys[0]
        average_token_length = len(''.join(profile_to_compare_keys))/len(profile_to_compare_keys)
        full_profile = {'name': profile_to_compare['name'],
                'common': common,
                'score': score,
                'max_length_word': max_length_word,
                'min_length_word': min_length_word,
                'average_token_length': average_token_length,
                'sorted_common': sorted_common}
        return full_profile
    else:
        return None


def detect_language_advanced(unknown_profile: dict, profiles: list, languages: list, top_n: int) -> str or None:
    if isinstance(unknown_profile, dict) and isinstance(profiles, list) and isinstance(languages, list) and isinstance(top_n, int):
        def score_function():
            score = {}
            for i in profiles:
                if i['name'] in languages:
                    for x in i:
                        full_profile = compare_profiles_advanced(unknown_profile, i, top_n)
                        score.update({i['name']: full_profile['score']})
            if not score:
                return None
            score_sorted = sorted(score.items(), key=lambda x: x[1], reverse=True)
            max_score = [a[0] for a in score_sorted][0]
            return max_score
        if languages != []:
            max_score = score_function()
            return max_score
        if languages == []:
            for i in profiles:
                languages.append(i['name'])
            max_score = score_function()
            return max_score
    else:
        None
