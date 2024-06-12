import importlib


def translate(key, locale=None):
    """Returns the requested key in the given locale or key"""
    if locale is None or locale == 'en_EN':
        return key

    module = importlib.import_module('translation.' + locale)
    lang = module.t

    if key not in lang:
        return key

    return lang[key]
