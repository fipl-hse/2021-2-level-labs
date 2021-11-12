import os
from main import tokenize, remove_stop_words
from lab_2.main import get_language_profiles

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'unknown_samples.txt'),
              'r', encoding='utf-8') as file_to_read:
        UNKNOWN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]
    stop_words = []
    texts_corpus = []
    language_labels = []
    for text in EN_SAMPLES:
        texts_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('eng')
    for text in DE_SAMPLES:
        texts_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('de')
    for text in LAT_SAMPLES:
        texts_corpus.append(remove_stop_words(tokenize(text), stop_words))
        language_labels.append('lat')

    language_profiles = get_language_profiles(texts_corpus, language_labels)

    known_text_vectors = []
    for text in texts_corpus:
        known_text_vectors.append(get_sparse_vector(text, language_profiles))
    k = 3
    RESULT = []
    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), stop_words)
        unknown_text_vector = get_vector(unknown_text, language_profiles)
        predict_language = predict_language_knn(unknown_text_vector, known_text_vectors,
                                                       language_labels, k)

        RESULT.append(predict_language[0])

    print(RESULT)
    EXPECTED = ['de', 'eng', 'lat']
    RESULT = ''

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'