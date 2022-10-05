import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from dotenv import load_dotenv

load_dotenv()

apikey = os.environ['apikey']
url = os.environ['url']

authenticator = IAMAuthenticator(apikey)
language_translator = LanguageTranslatorV3(version='2018-05-01',authenticator=authenticator)
language_translator.set_service_url(url)

def englishToFrench(englishText: str) -> str:
    response = language_translator.translate(text=englishText.split(), model_id='en-fr').get_result()
    return response['translations'][0]['translation']


def frenchToEnglish(frenchText: str):
    response = language_translator.translate(text=frenchText.split(), model_id='fr-en').get_result()
    return response['translations'][0]['translation']

if  __name__ == "__main__":
    print(frenchToEnglish('Monsieur'))