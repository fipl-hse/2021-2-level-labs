"""
Language detection starter
"""

import os
from lab_1.main import tokenize, remove_stop_words
from lab_2.main import get_freq_dict, get_language_profiles, get_text_vector, get_sparse_vector, \
    predict_language_knn_sparse

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

    en_tokens = tokenize(EN_TEXT)
    de_tokens = tokenize(DE_TEXT)
    lat_tokens = tokenize(LAT_TEXT)

    corpus = [en_tokens, de_tokens, lat_tokens]

    language_profiles = get_language_profiles(corpus, ['en', 'de', 'lat'])
    unknown_text_vector_1 = get_sparse_vector(tokenize(UNKNOWN_SAMPLES[0]),
                                              language_profiles)
    unknown_text_vector_2 = get_sparse_vector(tokenize(UNKNOWN_SAMPLES[1]),
                                              language_profiles)
    unknown_text_vector_3 = get_sparse_vector(tokenize(UNKNOWN_SAMPLES[2]),
                                              language_profiles)

    known_samples = []
    known_text_vectors = []
    for element in EN_SAMPLES:
        known_samples.append(element)
    for element in DE_SAMPLES:
        known_samples.append(element)
    for element in LAT_SAMPLES:
        known_samples.append(element)
    for element in known_samples:
        known_text_vectors.append(get_sparse_vector(tokenize(element), language_profiles))

    language_labels = ['en', 'en', 'en', 'en', 'en', 'de',
                       'de', 'de', 'de', 'de', 'lat', 'lat', 'lat', 'lat', 'lat']
    first_language = predict_language_knn_sparse(unknown_text_vector_1,
                                                 known_text_vectors, language_labels, k=1)
    second_language = predict_language_knn_sparse(unknown_text_vector_2,
                                                  known_text_vectors, language_labels, k=1)
    third_language = predict_language_knn_sparse(unknown_text_vector_3,
                                                 known_text_vectors, language_labels, k=1)

    EXPECTED = ['de', 'eng', 'lat']
    RESULT = [first_language[0], second_language[0], third_language[0]]

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'