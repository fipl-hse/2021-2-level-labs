"""
Language detection starter
"""

import os
from lab_2.main import (tokenize, remove_stop_words,
                        get_language_profiles, get_sparse_vector, predict_language_knn_sparse)

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
    RESULT = []

    # Get tokens for known texts
    ENG_TOKENS = remove_stop_words(tokenize(EN_TEXT), [])
    DE_TOKENS = remove_stop_words(tokenize(DE_TEXT), [])
    LAT_TOKENS = remove_stop_words(tokenize(LAT_TEXT), [])
    # Get tokens for unknown texts
    UNKNOWN_TOKENS_FIRST_TEXT = remove_stop_words(tokenize(UNKNOWN_SAMPLES[0]), [])
    UNKNOWN_TOKENS_SECOND_TEXT = remove_stop_words(tokenize(UNKNOWN_SAMPLES[1]), [])
    UNKNOWN_TOKENS_THIRD_TEXT = remove_stop_words(tokenize(UNKNOWN_SAMPLES[2]), [])
    # Get tokens for given languages
    DE_SAMPLES_TOKENS = []
    ENG_SAMPLES_TOKENS = []
    LAT_SAMPLES_TOKENS = []
    for SAMPLE in DE_SAMPLES:
        DE_SAMPLES_TOKENS.extend(remove_stop_words(tokenize(SAMPLE), []))
    for SAMPLE in EN_SAMPLES:
        ENG_SAMPLES_TOKENS.extend(remove_stop_words(tokenize(SAMPLE), []))
    for SAMPLE in LAT_SAMPLES:
        LAT_SAMPLES_TOKENS.extend(remove_stop_words(tokenize(SAMPLE), []))
    # Get vectors for every unknown text
    LANGUAGE_PROFILES = get_language_profiles([DE_SAMPLES_TOKENS,
                                               ENG_SAMPLES_TOKENS,
                                               LAT_SAMPLES_TOKENS],
                                               ['de', 'eng', 'lat'])
    # Get texts vectors
    FIRST_UNKNOWN_TEXT_VECTORS = get_sparse_vector(UNKNOWN_TOKENS_FIRST_TEXT, LANGUAGE_PROFILES)
    SECOND_UNKNOWN_TEXT_VECTORS = get_sparse_vector(UNKNOWN_TOKENS_SECOND_TEXT, LANGUAGE_PROFILES)
    THIRD_UNKNOWN_TEXT_VECTORS = get_sparse_vector(UNKNOWN_TOKENS_THIRD_TEXT, LANGUAGE_PROFILES)
    DE_TEXT_VECTORS = get_sparse_vector(DE_TOKENS, LANGUAGE_PROFILES)
    ENG_TEXT_VECTORS = get_sparse_vector(ENG_TOKENS, LANGUAGE_PROFILES)
    LAT_TEXT_VECTORS = get_sparse_vector(LAT_TOKENS, LANGUAGE_PROFILES)
    # Calculate result
    RESULT.append(predict_language_knn_sparse(FIRST_UNKNOWN_TEXT_VECTORS,
                                              [DE_TEXT_VECTORS,
                                               ENG_TEXT_VECTORS,
                                               LAT_TEXT_VECTORS],
                                               ['de', 'eng', 'lat'])[0])
    RESULT.append(predict_language_knn_sparse(SECOND_UNKNOWN_TEXT_VECTORS,
                                              [DE_TEXT_VECTORS,
                                               ENG_TEXT_VECTORS,
                                               LAT_TEXT_VECTORS],
                                               ['de', 'eng', 'lat'])[0])
    RESULT.append(predict_language_knn_sparse(THIRD_UNKNOWN_TEXT_VECTORS,
                                              [DE_TEXT_VECTORS,
                                               ENG_TEXT_VECTORS,
                                               LAT_TEXT_VECTORS],
                                               ['de', 'eng', 'lat'])[0])
    # print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert EXPECTED == RESULT, 'Detection not working'
