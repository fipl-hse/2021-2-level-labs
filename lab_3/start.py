"""
Language detection starter
"""

import os

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    ENG_SAMPLE = "Helium is the byproduct of millennia of radioactive decay from the elements thorium and uranium."
    GERMAN_SAMPLE = "Zwei Begriffe, die nicht unbedingt zueinander passen, am Arbeitsplatz schon mal gar nicht."
    UNKNOWN_SAMPLE = "Helium is material."


    # score 6, params: k = 5, trie_level = 2
    EXPECTED_DISTANCE_TO_EN_DE_PROFILES = 17, 25


    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'

