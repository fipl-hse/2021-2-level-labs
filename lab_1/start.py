"""
Language detection starter
"""


if __name__ == '__main__':

    english_text = """A man walks into a bar and orders a glass of water. 
                      The bartender points a gun at him and the man thanks him and leaves.
                      Why did the man thank the bartender?"""

    german_text = """Stell dir vor, du bist der Kapitän eines Frachtschiffes, das 30 Meter lang und 5 Meter breit ist.
                     Voll beladen hat es einen Tiefgang von 2 Metern, nicht beladen nur von einem Meter. 
                     Seine Höchstgeschwindigkeit betägt 18 Knoten. Wie alt ist der Kapitän?"""

    unknown_text = """A man is lying in his bed, trying to sleep. 
                      He picks up the phone and makes a call.
                      He waits for a while and hangs up before anyone could answer the phone.
                      Then he sleeps peacefully."""

    expected = 'en'
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
