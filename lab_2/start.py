"""
Language detection starter
"""

import os
from lab_2.main import (tokenize, remove_stop_words,
                        get_language_profiles, get_sparse_vector,
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
    for text in EN_SAMPLES:
        eng_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors.append(get_text_vector(eng_tokens_samples, language_profiles))
    for text in DE_SAMPLES:
        de_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors.append(get_text_vector(de_tokens_samples, language_profiles))
    for text in LAT_SAMPLES:
        lat_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors.append(get_text_vector(lat_tokens_samples, language_profiles))
    for element in unknown_tokens:
        unknown_text_vectors.append(get_text_vector(element, language_profiles))

    # calculate_distance
    distance = calculate_distance(unknown_text_vectors[0], known_text_vectors[0])

    # predict_language_score
    predict_language_score = predict_language_score(unknown_text_vectors, known_text_vectors,
                                                    language_labels)

    # calculate_distance_manhattan
    distance_m = calculate_distance_manhattan(unknown_text_vectors[0], known_text_vectors[0])

    # predict_language_knn
    predict_language_knn(unknown_text_vectors[0],
                         known_text_vectors, language_labels, 1, 'manhattan')

    # get_sparse_vector
    known_text_vectors_sparse = []
    unknown_text_vectors_sparse = []
    language_labels_sparse = []
    for text in EN_SAMPLES:
        eng_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors_sparse.append(get_sparse_vector(eng_tokens_samples, language_profiles))
        language_labels_sparse.append('en')
    for text in DE_SAMPLES:
        de_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors_sparse.append(get_sparse_vector(de_tokens_samples, language_profiles))
        language_labels_sparse.append('de')
    for text in LAT_SAMPLES:
        lat_tokens_samples = remove_stop_words(tokenize(text), stop_words)
        known_text_vectors_sparse.append(get_sparse_vector(lat_tokens_samples, language_profiles))
        language_labels_sparse.append('lat')
    for element in unknown_tokens:
        unknown_text_vectors_sparse.append(get_sparse_vector(element, language_profiles))

    # calculate_distance_sparse
    distance_sparse = calculate_distance_sparse(unknown_text_vectors_sparse[0],
                                                known_text_vectors_sparse[0])

    # predict_language_knn_sparse
    k = 3
    RESULT = []
    for vector in unknown_text_vectors_sparse:
        predict_language = predict_language_knn_sparse(
            vector, known_text_vectors_sparse, language_labels_sparse, k)
        RESULT.append(predict_language[0])
    print(RESULT)
    EXPECTED = ['de', 'eng', 'lat']
    stop_words = []
    corpus = []
    language_labels = []
    for text in DE_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('de')
    for text in EN_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('eng')
    for text in LAT_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('lat')
    language_profiles = get_language_profiles(corpus, language_labels)
    known_text_vectors = []
    for text in corpus:
        known_text_vectors.append(get_sparse_vector(text, language_profiles))
    k = 3
    RESULT = []
    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), stop_words)
        unknown_text_vector = get_sparse_vector(unknown_text, language_profiles)
        predicted_lang = predict_language_knn_sparse(unknown_text_vector, known_text_vectors,
                                                     language_labels, k)
        RESULT.append(predicted_lang[0])
    print(f"{RESULT} are possible languages")
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Detection not working'
