from translator import englishToFrench, frenchToEnglish

def test_english_to_french():
    # assert englishToFrench('') == '', 'Should be blank'
    assert englishToFrench('Hello') == 'Bonjour', 'Should be bonjour'

def test_french_to_english():
    # assert frenchToEnglish('') == '', 'Should be blank'
    assert frenchToEnglish('Bonjour') == 'Hello', 'Should be hello'

if __name__ == '__main__':
    test_english_to_french()
    test_french_to_english()
    print("all tests passed")