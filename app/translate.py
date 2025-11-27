from transformers import pipeline

try:
    yo2en_translator = pipeline("translation", model="Helsinki-NLP/opus-mt-yo-en", device=-1)
except Exception as e:
    print("Yoruba->English translator failed to load:", e)
    yo2en_translator = None

def translate_yoruba_to_english(text):
    """Translate Yoruba to English if translator exists; otherwise return input text."""
    if yo2en_translator is None:
        return text
    try:
        out = yo2en_translator(text, max_length=512)
        return out[0]["translation_text"]
    except Exception:
        return text