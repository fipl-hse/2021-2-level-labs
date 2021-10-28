"""
Language detection starter
"""

import os
from lab_1.main import tokenize, remove_stop_words
from lab_2.main import get_freq_dict, get_language_profiles, get_language_features, get_text_vector, calculate_distance, predict_language_score

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
PATH_TO_DATASET_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'dataset')

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'eng.txt'),
              'r', encoding='utf-8') as file_to_read:
        EN_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.txt'),
              'r', encoding='utf-8') as file_to_read:
        DE_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'lat.txt'),
              'r', encoding='utf-8') as file_to_read:
        LAT_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_de.txt'),
              'r', encoding='utf-8') as file_to_read:
        DE_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_eng.txt'),
              'r', encoding='utf-8') as file_to_read:
        EN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_lat.txt'),
              'r', encoding='utf-8') as file_to_read:
        LAT_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'unknown_samples.txt'),
              'r', encoding='utf-8') as file_to_read:
        UNKNOWN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]


    EXPECTED = ['de', 'eng', 'lat']
    RESULT = ''

    stop_words = []
    texts_corpus = []
    language_labels = []
    eng_tokens = remove_stop_words(tokenize(EN_TEXT), stop_words)
    de_tokens = remove_stop_words(tokenize(DE_TEXT), stop_words)
    lat_tokens = remove_stop_words(tokenize(LAT_TEXT), stop_words)
    unknown_tokens = []
    for text in UNKNOWN_SAMPLES:
        unknown_tokens.append(remove_stop_words(tokenize(text), stop_words))

    # get_freq_dict
    print(get_freq_dict(eng_tokens))
    print(get_freq_dict(de_tokens))
    print(get_freq_dict(lat_tokens))

    # preparing for get_language_profiles
    texts_corpus = [eng_tokens, de_tokens, lat_tokens]
    language_labels = ['eng', 'de', 'lat']

    # get_language_profiles
    language_profiles = get_language_profiles(texts_corpus, language_labels)

    # get_language_features
    unique_tokens = get_language_features(language_profiles)

    # get_text_vector
    known_text_vectors = []
    unknown_text_vectors = []
    labels_of_languages = []
    for text in EN_SAMPLES:
        eng_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors.append(get_text_vector(eng_tokens_samples, language_profiles))
        labels_of_languages.append('en')
    for text in DE_SAMPLES:
        de_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors.append(get_text_vector(de_tokens_samples, language_profiles))
        labels_of_languages.append('de')
    for text in LAT_SAMPLES:
        lat_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors.append(get_text_vector(lat_tokens_samples, language_profiles))
        labels_of_languages.append('lat')
    for element in unknown_tokens:
        unknown_text_vectors.append(get_text_vector(element, language_profiles))

    # calculate_distance
    distance = calculate_distance(unknown_text_vectors[0], known_text_vectors[0])

    # predict_language_score
    minimum = len(min(known_text_vectors, key=len))
    known_vectors = []
    unknown_vectors = []
    RESULT = []
    for vector in known_text_vectors:
        vec = vector[:minimum]
        known_vectors.append(vec)
    for vector in unknown_text_vectors:
        vec = vector[:minimum]
        unknown_vectors.append(vec)
    for vector in unknown_vectors:
        language_score_predict = predict_language_score(vector, known_vectors, labels_of_languages)
        RESULT.append(language_score_predict[0])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, EXPECTED

