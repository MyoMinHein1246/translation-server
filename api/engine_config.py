from deep_translator import GoogleTranslator, MyMemoryTranslator, QcriTranslator

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
    source_name = next((lang["name"] for lang in LANGUAGES if lang["code"] == source), "auto")
    target_name = next((lang["name"] for lang in LANGUAGES if lang["code"] == target), target).lower()

    try:
        """Translate using MyMemory Translator with optional proxy fallback."""
        translator = MyMemoryTranslator(source=source_name, target=target_name)
        return translator.translate(text)
    except Exception as e:
        if proxies:
            translator = MyMemoryTranslator(source=source_name, target=target_name, proxies=proxies)
            return translator.translate(text)

def translate_with_qcri(text, source, target, proxies=None):
    try:
        """Translate using QCRI Translator."""
        translator = QcriTranslator(source=source, target=target)
        return translator.translate(text=text, source=source, target=target, domain="general")
    except Exception as e:
        return f"QCRI Translation Error: {str(e)}"


# Centralized engine methods
ENGINE_METHODS = {
    "google": translate_with_google,
    "mymemory": translate_with_mymemory,
    "qcri": translate_with_qcri,
}