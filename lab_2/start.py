"""
Language detection starter
"""

import os
from main import tokenize, get_language_profiles, get_text_vector, predict_language_knn

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

    INIT_LABELS = ['eng', 'de', 'lat']

    CORPUS = list()
    CORPUS.append(tokenize(EN_TEXT))
    CORPUS.append(tokenize(DE_TEXT))
    CORPUS.append(tokenize(LAT_TEXT))

    PROFILES = get_language_profiles(CORPUS, INIT_LABELS)

    UNK_VECTORS = list()
    for i in UNKNOWN_SAMPLES:
        UNK_VECTORS.append(get_text_vector(tokenize(i), PROFILES))

    KNOWN_VECTORS = list()
    ADD_LABELS = list()
    for j in EN_SAMPLES:
        KNOWN_VECTORS.append(get_text_vector(tokenize(j), PROFILES))
        ADD_LABELS.append('eng')
    for j in DE_SAMPLES:
        KNOWN_VECTORS.append(get_text_vector(tokenize(j), PROFILES))
        ADD_LABELS.append('de')
    for j in LAT_SAMPLES:
        KNOWN_VECTORS.append(get_text_vector(tokenize(j), PROFILES))
        ADD_LABELS.append('lat')

    PREDICTIONS = list()
    for k in UNK_VECTORS:
        PREDICTIONS.append(predict_language_knn(k, KNOWN_VECTORS, ADD_LABELS))

    EXPECTED = ['de', 'eng', 'lat']
    RESULT = list()
    for k in PREDICTIONS:
        RESULT.append(k[0])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
