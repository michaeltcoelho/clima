import unicodedata


def sanitize_string(string):
    return ''.join(
        ch for ch in unicodedata.normalize('NFKD', string)
        if not unicodedata.combining(ch))
