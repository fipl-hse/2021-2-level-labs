"""
Language detection starter
"""

import os
from lab_2.main import get_sparse_vector
from lab_2.main import get_language_profiles
from lab_2.main import predict_language_knn_sparse
from main import tokenize
from main import remove_stop_words

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
    # создаем языковые профили
    labels = ['eng', 'de', 'lat']
    lat_tokens = remove_stop_words(tokenize(LAT_TEXT), [])
    de_tokens = remove_stop_words(tokenize(DE_TEXT), [])
    eng_tokens = remove_stop_words(tokenize(EN_TEXT), [])
    corpus = [eng_tokens, de_tokens, lat_tokens]
    language_profiles = get_language_profiles(corpus, labels)
    # создаем список разреженных векторов известных текстов
    known_tet_vectors = []
    language_labels = []
    for text in DE_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        known_tet_vectors.append(get_sparse_vector(tokens, language_profiles))
        language_labels.append('de')
    for text in EN_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        known_tet_vectors.append(get_sparse_vector(tokens, language_profiles))
        language_labels.append('eng')
    for text in LAT_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        known_tet_vectors.append(get_sparse_vector(tokens, language_profiles))
        language_labels.append('lat')
    # создаем разреженные векторы для неизвестных текстов
    unknown_text_vectors = []
    for text in UNKNOWN_SAMPLES:
        tokens = remove_stop_words(tokenize(text), [])
        unknown_text_vectors.append(get_sparse_vector(tokens, language_profiles))
    # узнаем язык текстов
    result = []
    for vector in unknown_text_vectors:
        result.append(predict_language_knn_sparse(vector, known_tet_vectors, language_labels, 3)[0])
    print(result)
    print(EXPECTED)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert result, EXPECTED
