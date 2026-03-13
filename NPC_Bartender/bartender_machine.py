# bartender_machine.py
from Discord_NPC_RPG_BOT import Machine

from NPC_Bartender.lore_machine import LoreConversationMachine


# ======================
# COMBINAÇÃO DE MAQUINAS
# ======================

class BartenderMachine(
        LoreConversationMachine,
        Machine
        ):
    def __init__(self):
        super().__init__()


bartender_machine = BartenderMachine()
