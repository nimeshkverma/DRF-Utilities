from difflib import SequenceMatcher


def get_class(class_string):
    parts = class_string.split('.')
    module = ".".join(parts[:-1])
    imported_class = __import__(module)
    for comp in parts[1:]:
        imported_class = getattr(imported_class, comp)
    return imported_class


def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()
