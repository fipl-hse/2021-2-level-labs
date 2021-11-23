"""
Language detection starter
"""

import os
from lab_3.main import LanguageProfile, LetterStorage, ProbabilityLanguageDetector, LanguageDetector, \
    tokenize_by_sentence, encode_corpus, NGramTrie

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
profiles = os.listdir(PATH_TO_PROFILES_FOLDER)

if __name__ == '__main__':
    SECRET_SAMPLE = """ Некој е болен и тој не е слободен. Dлетува гол во дупка од мраз. 
    И пее, а плаче од болка. Дали е ова контраст, можеби – живот?"""

    # score 10, k = 1000, trie_levels = (2,)
    # predict SECRET_SAMPLE
    # print(detector.detect(unknown_profile, 1000, (2,)))
    # EXPECTED_LANGUAGE = ?
    # EXPECTED_MIN_DISTANCE = ?
    tokenized_unk = tokenize_by_sentence(SECRET_SAMPLE)

    unknown_storage = LetterStorage()
    unknown_storage.update(tokenized_unk)
    encoded_unk_corpus = encode_corpus(unknown_storage, tokenized_unk)

    unk_trie = NGramTrie(2, unknown_storage)
    unk_trie.extract_n_grams(encoded_unk_corpus)
    unk_trie.get_n_grams_frequencies()
    unk_trie.calculate_log_probabilities()

    unknown_profile = LanguageProfile(unknown_storage, 'unk')
    unknown_profile.create_from_tokens(encoded_unk_corpus, (2,))

    detector = ProbabilityLanguageDetector()

    for profile in profiles:
        known_letter_storage = LetterStorage()
        known_profile = LanguageProfile(known_letter_storage, profile)
        known_profile.open(os.path.join(PATH_TO_PROFILES_FOLDER, profile))
        detector.register_language(known_profile)

    new_freq_dict = {}
    for profile in detector.language_profiles.values():
        new_freq_dict = {}
        for trie in profile.tries:
            for n_gram_freq in trie.n_gram_frequencies:
                if isinstance(n_gram_freq, str):
                    for letter in n_gram_freq:
                        new_freq_dict[profile.storage.storage[letter]] = profile.storage.storage[letter]
        trie.extract_n_grams_frequencies(new_freq_dict)

    freq_dict = detector.detect(unknown_profile, 1000, (2,))
    language_value = freq_dict.max()
    for i in freq_dict.items():
        if i[1] == language_value:
            final_language = i[0]

    RESULT = final_language
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
