# BaseSymbol.py

# ==========================================================
# BaseSymbol
# ==========================================================

class SymbolMeta(type):
    description = "MetaClasse BaseSymbol"

    def __str__(cls):
        return cls.description


class BaseSymbol(metaclass=SymbolMeta):
    description = "Classe BaseSymbol"
