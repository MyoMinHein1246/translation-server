from deep_translator import GoogleTranslator, MyMemoryTranslator, PonsTranslator, LingueeTranslator

from api.languages import LANGUAGES

def translate_with_google(text, source, target, proxies=None):
    try:
        """Translate using Google Translator with optional proxy fallback."""
        translator = GoogleTranslator(source=source, target=target)
        return translator.translate(text)
    except Exception as e:
        if proxies:
            translator = GoogleTranslator(source=source, target=target, proxies=proxies)
            return translator.translate(text)
    

def translate_with_mymemory(text, source, target, proxies=None):
    try:
        """Translate using MyMemory Translator with optional proxy fallback."""
        translator = MyMemoryTranslator(source=source, target=target)
        return translator.translate(text)
    except Exception as e:
        if proxies:
            translator = MyMemoryTranslator(source=source, target=target, proxies=proxies)
            return translator.translate(text)

def translate_with_pons(text, source, target, proxies=None):
    """Translate using Pons Translator with optional proxy fallback."""
    source_name = next((lang["name"] for lang in LANGUAGES if lang["code"] == source), source)
    target_name = next((lang["name"] for lang in LANGUAGES if lang["code"] == target), target)
    
    try:
        translator = PonsTranslator(source=source_name, target=target_name)
        return translator.translate(text)
    except Exception as e:
        if proxies:
            translator = PonsTranslator(source=source_name, target=target_name, proxies=proxies)
            return translator.translate(text)

def translate_with_linguee(text, source, target, proxies=None):
    """Translate using Linguee Translator with optional proxy fallback."""
    source_name = next((lang["name"] for lang in LANGUAGES if lang["code"] == source), source)
    target_name = next((lang["name"] for lang in LANGUAGES if lang["code"] == target), target)
    
    try:
        translator = LingueeTranslator(source=source_name, target=target_name)
        return translator.translate(text)
    except Exception as e:
        if proxies:
            translator = LingueeTranslator(source=source_name, target=target_name, proxies=proxies)
            return translator.translate(text)


# Centralized engine methods
ENGINE_METHODS = {
    "google": translate_with_google,
    "mymemory": translate_with_mymemory,
    "pons": translate_with_pons,
    "linguee": translate_with_linguee,
}