# coffee_machine.py
from Discord_NPC_RPG_BOT import BaseState

from NPC_Bartender2.assistant_state_symbol import TalkingSymbol


# =================
# SYMBOL
# =================
class AskCoffeeSymbol(TalkingSymbol):
    description = "<Pedir um Café>"

    def __init__(self):
        super().__init__("Você pede um café.")


# =================
# STATES
# =================
class NotInterestedCoffeeState(BaseState):
    def is_active(self, machine, sender):
        if not sender.on_coffee_shop:
            return False
        try:
            return not machine.relations[sender]["CoffeeInterested"]
        except Exception:
            return True


# =================
# CONFIGURAÇÃO
# =================
def askcoffe_out(machine, sender, symbol):
    msm = "Temos vários cafés. Qual você gostaria?"
    machine.relations[sender]["CoffeeInterested"] = True
    return [
        TalkingSymbol("Você: Quero um café."),
        TalkingSymbol(f"Liu: {msm}")
    ]


notinterestedcoffee_state = NotInterestedCoffeeState()
notinterestedcoffee_state.register_symbol(AskCoffeeSymbol, askcoffe_out)


# =================
# MACHINE
# =================
states = [
    notinterestedcoffee_state
]


class CoffeeMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)
