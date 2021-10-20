"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words


# 4

def get_freq_dict(tokens: list) -> dict or None:
    if not isinstance(tokens, list):
        return None
    result = {}
    for token in tokens:
        if isinstance(token, str):
            if token in result:
                result[token] += 1
            else:
                result[token] = 1
        else:
            return None
    for word in result:  # нахождение частоты встречаемости каждого слова в токенах и округление до 5 знаков после запятой 
        result[word] = round(result[word] / len(tokens), 5)
    return result


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    """
    Computes language profiles for a collection of texts
        and adds appropriate language label for each text
    :param texts_corpus: a list of given texts
    :param language_labels: a list of given language labels
    :return: a dictionary of dictionaries - language profiles
    """

    if not isinstance(texts_corpus, list) or not isinstance(language_labels, list):
        return None
    result = {}
    for i in range(len(texts_corpus)):
        if not isinstance(texts_corpus[i], list) or not isinstance(language_labels[i], str):
            return None
        else:  # возвращает словарь где ключ метка языка, а значение словарь частот
            result[language_labels[i]] = get_freq_dict(texts_corpus[i])
    return result


def get_language_features(language_profiles: dict) -> list or None:
    """
    Gets all unique words from language profiles
        and sorts them in alphabetical order
    :param language_profiles: a dictionary of dictionaries - language profiles
    """

    if not isinstance(language_profiles, dict):
        return None
    words = set()  # создание пустого множества
    for item in language_profiles.items():  # разбиение словаря на список и итерация по нему
        for word in item[1]:  # это итерация по словам 
            words.add(word)
    if not words:
        return None
    return sorted(list(words))


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    if not isinstance(original_text, list):
        return None
    for elem in original_text:
        if not isinstance(elem, str):
            return None
    features = get_language_features(language_profiles)
    text_vector = []
    for feature in features:
        if feature not in original_text:
            text_vector.append(0)
        else:
            text_vector.append(original_text.count(feature) / len(original_text))

    return text_vector
