# coffee_machine.py
from NPC_RPG_BOT import BaseState

from NPC_Bartender.assistant_state_symbol import TalkingSymbol


# =================
# SYMBOL
# =================
class AskCoffeeSymbol(TalkingSymbol):
    description = "<Pedir um Café>"

    def __init__(self):
        super().__init__("Você pede um Café.")


class GiveUpCoffeeSymbol(TalkingSymbol):
    description = "<Pedir outra coisa>"

    def __init__(self):
        super().__init__("Você decide pedir outra coisa.")


class AskEspressoCoffeeSymbol(TalkingSymbol):
    description = "<Pedir um Café Expresso>"

    def __init__(self):
        super().__init__("Você pede um Café Expresso.")


class AskCappuccinoCoffeeSymbol(TalkingSymbol):
    description = "<Pedir um Cappuccino>"

    def __init__(self):
        super().__init__("Você pede um Cappuccino.")


class AskCoffeeWithMilkSymbol(TalkingSymbol):
    description = "<Pedir um Café com Leite>"

    def __init__(self):
        super().__init__("Você pede um Café com Leite.")


class AskSuggestionCoffeeSymbol(TalkingSymbol):
    description = "<Pedir uma Sugestão>"

    def __init__(self):
        super().__init__("Você pede uma sugestão.")


# =================
# STATES
# =================
class NotInterestedCoffeeState(BaseState):
    def is_active(self, machine, sender):
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Nothing"
        except Exception:
            return True


class InterestedCoffeeState(BaseState):
    def is_active(self, machine, sender) -> bool:
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Coffee"
        except Exception:
            return False


# =================
# CONFIGURAÇÃO
# =================
def askcoffe_notinterestedcoffee(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Coffee"
    return [
        TalkingSymbol("Você: Quero um café."),
        TalkingSymbol("Liu: Temos vários cafés. Qual você gostaria?")
    ]

def giveupcoffee_interestedcoffee(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Acho que vou pedir outra coisa."),
        TalkingSymbol("Liu: Como quiser.")
    ]

def askespressocoffee_interestedcoffee(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Eu gostaria de um Café Expresso."),
        TalkingSymbol("Liu prepara um Café Expresso e te entrega."),
        TalkingSymbol("Liu: Aqui esta o seu expresso!")
    ]

def askcappuccinocoffee_interestedcoffee(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Eu acho que vou de Cappuccino."),
        TalkingSymbol("Liu prepara um Cappucino e te entrega."),
        TalkingSymbol("Liu: Cappuccino! Como pedido.")
    ]

def askcoffeewithmilk_interestedcoffee(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Eu gostaria de Café com Leite."),
        TalkingSymbol("Liu prepara um Café com Leite e te entrega."),
        TalkingSymbol("Liu: Prontinho, Café com Leite!")
    ]

def asksuggestioncoffee_interestedcoffee(machine, sender, symbol):
    return [
        TalkingSymbol("Você: Qual você recomenda?"),
        TalkingSymbol("Liu: Hmm... Se você gosta de algo mais forte, o expresso é perfeito. Mas o cappuccino é o favorito da maioria.")
    ]


notinterestedcoffee_state = NotInterestedCoffeeState()
notinterestedcoffee_state.register_symbol(AskCoffeeSymbol, askcoffe_notinterestedcoffee)

interestedcoffee_state = InterestedCoffeeState()
interestedcoffee_state.register_symbol(GiveUpCoffeeSymbol, giveupcoffee_interestedcoffee)
interestedcoffee_state.register_symbol(AskEspressoCoffeeSymbol, askespressocoffee_interestedcoffee)
interestedcoffee_state.register_symbol(AskCappuccinoCoffeeSymbol, askcappuccinocoffee_interestedcoffee)
interestedcoffee_state.register_symbol(AskCoffeeWithMilkSymbol, askcoffeewithmilk_interestedcoffee)
interestedcoffee_state.register_symbol(AskSuggestionCoffeeSymbol, asksuggestioncoffee_interestedcoffee)


# =================
# MACHINE
# =================
states = [
    notinterestedcoffee_state,
    interestedcoffee_state
]


class CoffeeMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)
