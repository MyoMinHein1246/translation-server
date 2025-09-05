from deep_translator import GoogleTranslator, MyMemoryTranslator, PonsTranslator, LingueeTranslator

def translate_with_google(text, source, target, proxies=None):
    """Translate using Google Translator with optional proxy fallback."""
    translator = GoogleTranslator(source=source, target=target, proxies=proxies)
    return translator.translate(text)

def translate_with_mymemory(text, source, target, proxies=None):
    """Translate using MyMemory Translator with optional proxy fallback."""
    translator = MyMemoryTranslator(source=source, target=target, proxies=proxies)
    return translator.translate(text)

def translate_with_pons(text, source, target, proxies=None):
    """Translate using Pons Translator with optional proxy fallback."""
    translator = PonsTranslator(source=source, target=target, proxies=proxies)
    return translator.translate(text)

def translate_with_linguee(text, source, target, proxies=None):
    """Translate using Linguee Translator with optional proxy fallback."""
    translator = LingueeTranslator(source=source, target=target, proxies=proxies)
    return translator.translate(text)

# Centralized engine methods
ENGINE_METHODS = {
    "google": translate_with_google,
    "mymemory": translate_with_mymemory,
    "pons": translate_with_pons,
    "linguee": translate_with_linguee,
}