"""
Language detection starter
"""

import os
from lab_2.main import (
    tokenize,
    remove_stop_words,
    get_language_profiles,
    get_language_features,
    get_sparse_vector,
    predict_language_knn_sparse
)

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

    corpus = []
    labels = []
    STOP_WORDS = []
    KNN = 3
    for text in DE_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), STOP_WORDS))
        labels.append('de')
    for text in EN_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), STOP_WORDS))
        labels.append('eng')
    for text in LAT_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), STOP_WORDS))
        labels.append('lat')
    dummy_labels = [str(i) for i in range(len(corpus))]
    dummy_labeled_profiles = get_language_profiles(corpus, dummy_labels)
    features = get_language_features(dummy_labeled_profiles)
    vectors = [get_sparse_vector(text, dummy_labeled_profiles) for text in corpus]

    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), STOP_WORDS)
        unknown_vector = get_sparse_vector(unknown_text, dummy_labeled_profiles)
        prediction = predict_language_knn_sparse(unknown_vector,
                                                 vectors,
                                                 labels,
                                                 KNN)
        RESULT.append(prediction[0])
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert EXPECTED == RESULT, 'Detection not working'
