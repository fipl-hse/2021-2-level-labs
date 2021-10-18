"""
Language detection starter
"""

from main import *
import os

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

    RESULT = []
    EXPECTED = ['de', 'eng', 'lat']

    corpus = []
    labels = []
    stop_words = []
    k = 3
    # creating corpus of German, English and Latin
    # usual tokenization of the text to get the corpus
    # appending the language name in labels
    for text in DE_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), stop_words))
        labels.append('de')
    for text in EN_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), stop_words))
        labels.append('eng')
    for text in LAT_SAMPLES:
        corpus.append(remove_stop_words(tokenize(text), stop_words))
        labels.append('lat')

    # creating the labels but using numeration instead of names
    # used for calculating the unique variable and vectors from all known texts
    index_labels = [str(i) for i in range(len(corpus))]
    # getting profiles with their indexes {0: "first_text_freqs", 1: "second_text_freqs" etc.}
    # and unique words thorough all of them
    index_label_profiles = get_language_profiles(corpus, index_labels)
    unique = get_language_features(index_label_profiles)
    # using these profiles to create a bunch of known vectors
    vectors = [get_sparse_vector(text, index_label_profiles) for text in corpus]

    # tokenizing the unknown text
    # guessing the language of each sample
    for text in UNKNOWN_SAMPLES:
        unknown_text = remove_stop_words(tokenize(text), stop_words)
        unknown_vector = get_sparse_vector(unknown_text, index_label_profiles)
        guess = predict_language_knn_sparse(unknown_vector, vectors, labels, k)
        RESULT.append(guess[0])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == EXPECTED, 'Detection not working'
