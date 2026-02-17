from deep_translator import GoogleTranslator
import os

class TranslationService:
    def __init__(self):
        # We don't need a persistent translator object for deep-translator in the same way
        pass

    def translate_text(self, text: str, target_lang: str):
        try:
            # deep-translator handles the request per call
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return text # Fallback to original text

translation_service = TranslationService()
