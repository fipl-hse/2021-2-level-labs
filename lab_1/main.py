def tokenize(text_str):
    if isinstance(text_str, str) is False:
        return None
    else:
        symbols = ["'", '-', '%', '>', '<', '$', '@', '#', '&', '*', '.', ',', '!', ';', ':']
        for i in text_str:
            if i in symbols:
                text_str = text_str.replace(i, "")
        text_update = ''.join([i for i in text_str if not i.isdigit()])
        return text_update.lower().split()

def remove_stop_words(text_update, STOP_WORDS):
    if isinstance(STOP_WORDS, list) and isinstance(text_update, list):
        if text_update:
            for m in enumerate(text_update):
                if m[1] in STOP_WORDS:
                    text_update[m[0]] = ''
            while '' in text_update:
                text_update.remove('')
            return text_update
        else:
            return None
    else:
        return None

def calculate_frequencies(text_update):
    if isinstance(text_update, list):
        for j in text_update:
            if isinstance(j, str):
                frequency_dict = {}
                for token in text_update:
                    if token not in frequency_dict:
                        frequency_dict[token] = 1
                    else:
                        frequency_dict[token] += 1
                return frequency_dict
            return None
    return None

def get_top_n_words(frequency_dict, top_n):
    if isinstance(frequency_dict, dict) and isinstance(top_n, int):
        freq_sort_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)[:top_n])
        freq_sort_list = list((freq_sort_dict).keys())
        return freq_sort_list
    else:
        return None

def create_language_profile(language, text_str, STOP_WORDS):
    if isinstance(language, str) and isinstance(text_str, str) and isinstance(STOP_WORDS, list):
        l_profile = {'name': '', 'freq': {}, 'n_words': 0}
        tokens = tokenize(text_str)
        tokens = remove_stop_words(tokens, STOP_WORDS)
        l_profile['name'] = language
        l_profile['freq'] = calculate_frequencies(tokens)
        l_profile['n_words'] = len(l_profile['freq'].keys())
        return l_profile
    return None

def compare_profiles(unknown_profile, profile_to_compare, top_n):
    if isinstance(unknown_profile, dict) and isinstance(profile_to_compare, dict) and isinstance(top_n, int):
        common_tokens = 0
        tn1_unknown = get_top_n_words(unknown_profile['freq'], top_n)
        tn2_pr_to_comp = get_top_n_words(profile_to_compare['freq'], top_n)
        for word_1 in tn1_unknown:
            for word_2 in tn2_pr_to_comp:
                if word_1 == word_2:
                    common_tokens += 1
        crosses = round(common_tokens/top_n, 2)
        return crosses
    return None





