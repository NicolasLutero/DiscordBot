# desert_machine.py
from Discord_NPC_RPG_BOT import BaseState

from NPC_Bartender2.assistant_state_symbol import TalkingSymbol


# =================
# SYMBOL
# =================
class GetInSymbol(TalkingSymbol):
    description = "<Entrar na Cafeteria Aurora>"

    def __init__(self):
        super().__init__(f"O sino acima da porta faz “plin”, indicando que alguém chegou!")


# =================
# STATES
# =================
class OutState(BaseState):
    def is_active(self, machine, sender):
        return not sender.on_coffee_shop


# =================
# CONFIGURAÇÃO
# =================
def getin_out(machine, sender, symbol):
    sender.on_coffee_shop = True

    msm = "Olá! Bem-vindo ao Café Aurora! Como posso te ajudar?"
    if hasattr(machine, "relations"):
        if sender in machine.relations.keys():
            relation = machine.relations[sender]
            if "apelido" in relation.keys():
                msm = f"Olá {relation["apelido"]}! Tudo bem? Como posso te ajudar?"
            elif "nome" in relation.keys():
                msm = f"Oi {relation["nome"]}! Bem-vindo de volta ao Café Aurora! Como posso te ajudar?"
    return [
        TalkingSymbol(symbol.msm),
        TalkingSymbol(f"Liu: {msm}")
    ]


out_state = OutState()
out_state.register_symbol(GetInSymbol, getin_out)


# =================
# MACHINE
# =================
states = [
    out_state
]


class OutInMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)
