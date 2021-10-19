"""
Language detection starter
"""

import os
from lab_2.main import (tokenize,
                        remove_stop_words,
                        get_language_profiles,
                        get_sparse_vector,
                        predict_language_knn_sparse)

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

    text_corpus = []
    lang_labels = []
    STOP_WORDS = []
    KNN = 3

    for text in DE_SAMPLES:
        text_corpus.append(remove_stop_words(tokenize(text), STOP_WORDS))
        lang_labels.append('de')
    for text in EN_SAMPLES:
        text_corpus.append(remove_stop_words(tokenize(text), STOP_WORDS))
        lang_labels.append('eng')
    for text in LAT_SAMPLES:
        text_corpus.append(remove_stop_words(tokenize(text), STOP_WORDS))
        lang_labels.append('lat')

    lang_profiles = get_language_profiles(text_corpus, lang_labels)
    known_vectors = [get_sparse_vector(text, lang_profiles) for text in text_corpus]

    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), STOP_WORDS)
        unknown_vector = get_sparse_vector(unknown_text, lang_profiles)
        prediction = predict_language_knn_sparse(unknown_vector, known_vectors, lang_labels, KNN)
        RESULT.append(prediction[0])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Detection not working'
