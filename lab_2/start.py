"""
Language detection starter
"""

import os
from lab_1.main import tokenize, remove_stop_words
from lab_2.main import get_freq_dict, get_language_profiles, \
    get_language_features, get_text_vector, \
    calculate_distance, predict_language_score, \
    calculate_distance_manhattan, predict_language_knn, \
    get_sparse_vector, calculate_distance_sparse, \
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
    stop_words = []
    texts_corpus = []
    language_labels = []
    eng_tokens = remove_stop_words(tokenize(EN_TEXT), stop_words)
    de_tokens = remove_stop_words(tokenize(DE_TEXT), stop_words)
    lat_tokens = remove_stop_words(tokenize(LAT_TEXT), stop_words)
    unknown_str = ''.join(UNKNOWN_SAMPLES)
    unknown_tokens = remove_stop_words(tokenize(unknown_str), stop_words)

    # get_freq_dict
    for text in EN_SAMPLES:
        print(get_freq_dict(eng_tokens))
    for text in DE_SAMPLES:
        print(get_freq_dict(de_tokens))
    for text in LAT_SAMPLES:
        print(get_freq_dict(lat_tokens))

    # preparing for get_language_profiles
    for text in EN_SAMPLES:
        texts_corpus.append(eng_tokens)
        language_labels.append('eng')
    for text in DE_SAMPLES:
        texts_corpus.append(de_tokens)
        language_labels.append('de')
    for text in LAT_SAMPLES:
        texts_corpus.append(lat_tokens)
        language_labels.append('lat')

    # get_language_profiles
    language_profiles = get_language_profiles(texts_corpus, language_labels)

    # get_language_features
    unique_tokens = get_language_features(language_profiles)

    # get_text_vector
    eng_vector = get_text_vector(eng_tokens, language_profiles)
    de_vector = get_text_vector(de_tokens, language_profiles)
    lat_vector = get_text_vector(lat_tokens, language_profiles)
    unknown_vector = get_text_vector(unknown_tokens, language_profiles)

    # calculate_distance
    eng_distance = calculate_distance(unknown_vector, eng_vector)
    de_distance = calculate_distance(unknown_vector, de_vector)
    lat_distance = calculate_distance(unknown_vector, lat_vector)

    # predict_language_score
    known_text_vectors = [eng_vector, de_vector, lat_vector]
    predict_language_score = predict_language_score(unknown_vector, known_text_vectors, language_labels)

    # calculate_distance_manhattan
    eng_distance_m = calculate_distance_manhattan(unknown_vector, eng_vector)
    de_distance_m = calculate_distance_manhattan(unknown_vector, de_vector)
    lat_distance_m = calculate_distance_manhattan(unknown_vector, lat_vector)

    # predict_language_knn
    predict_language_knn(unknown_vector, known_text_vectors, language_labels, 1, 'manhattan')

    # get_sparse_vector
    eng_sparse_vector = get_sparse_vector(eng_tokens, language_profiles)
    de_sparse_vector = get_sparse_vector(de_tokens, language_profiles)
    lat_sparse_vector = get_sparse_vector(lat_tokens, language_profiles)

    # calculate_distance_sparse
    en_distance_sparse = calculate_distance_sparse(unknown_vector, eng_sparse_vector)
    de_distance_sparse = calculate_distance_sparse(unknown_vector, de_sparse_vector)
    lat_distance_sparse = calculate_distance_sparse(unknown_vector, lat_sparse_vector)

    # predict_language_knn_sparse
    k = 3
    RESULT = []
    known_text_vectors_sparse = [eng_sparse_vector, de_sparse_vector, lat_sparse_vector]
    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), stop_words)
        unknown_text_vector = get_sparse_vector(unknown_text, language_profiles)
        predict_language = predict_language_knn_sparse(unknown_text_vector, known_text_vectors_sparse,
                                                       language_labels, k)
        RESULT.append(predict_language[0])
    print(RESULT)
    EXPECTED = ['de', 'eng', 'lat']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
