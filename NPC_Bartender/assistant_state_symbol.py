# assistant_state_symbol.py
from NPC_RPG_BOT import BaseSymbol


# =================
# SYMBOL
# =================
class TalkingSymbol(BaseSymbol):
    description = "Símbolo abstrato de conversa."

    def __init__(self, msm):
        super().__init__()
        self.msm = msm

    def __str__(self):
        return self.msm
