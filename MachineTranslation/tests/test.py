from translator import english_to_french, french_to_english


def test_english_to_french():
    assert english_to_french(
        'Miss') == 'Mlle', 'Should be Mademoiselle'
    assert english_to_french('Hello') == 'Bonjour', 'Should be bonjour'


def test_french_to_english():
    assert french_to_english(
        'Mlle') == 'Miss', 'Should be Miss'
    assert french_to_english('Bonjour') == 'Hello', 'Should be hello'


if __name__ == '__main__':
    test_english_to_french()
    test_french_to_english()
    print("all tests passed")
