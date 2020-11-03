import unicodedata


class Util:
    @staticmethod
    def string_no_accents(s: str):
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
