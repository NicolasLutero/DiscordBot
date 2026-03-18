# dessert_machine.py
from NPC_RPG_BOT import BaseState

from NPC_Bartender.assistant_state_symbol import TalkingSymbol


# =================
# SYMBOL
# =================
class AskDessertSymbol(TalkingSymbol):
    description = "<Pedir um Doce>"

    def __init__(self):
        super().__init__("Você pede um Doce.")


class GiveUpDessertSymbol(TalkingSymbol):
    description = "<Pedir outra coisa>"

    def __init__(self):
        super().__init__("Você decidi pedir outra coisa.")


class AskChocolateCakeDessertSymbol(TalkingSymbol):
    description = "<Pedir um Bolo de Chocolate>"

    def __init__(self):
        super().__init__("Você pede um Bolo de Chocolate.")


class AskCroissantDessertSymbol(TalkingSymbol):
    description = "<Pedir um Croissant>"

    def __init__(self):
        super().__init__("Você pede um Croissant.")


class AskStrawberryPieDessertSymbol(TalkingSymbol):
    description = "<Pedir um Torta de Morango>"

    def __init__(self):
        super().__init__("Você pede um Torta de Morango.")


class AskSuggestionDessertSymbol(TalkingSymbol):
    description = "<Pedir uma Sugestão>"

    def __init__(self):
        super().__init__("Você pede uma sugestão.")


# =================
# STATES
# =================
class NotInterestedDessertState(BaseState):
    def is_active(self, machine, sender):
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Nothing"
        except Exception:
            return True


class InterestedDessertState(BaseState):
    def is_active(self, machine, sender) -> bool:
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Dessert"
        except Exception:
            return False


# =================
# CONFIGURAÇÃO
# =================
def askdessert_notinteresteddessert(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Dessert"
    return [
        TalkingSymbol("Você: Quero um doce."),
        TalkingSymbol("Liu: Hmm, temos algumas coisas deliciosas hoje."),
        TalkingSymbol("Liu: Tem bolo de chocolate, croissant e torta de morango. Estão fresquinhos!")
    ]

def giveupdessert_interesteddessert(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Pensando bem, vou escolher outra coisa."),
        TalkingSymbol("Liu: Fique a vontade.")
    ]

def askchocolatecakedessert_interesteddessert(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Eu gostaria de um Bolo de Chocolate."),
        TalkingSymbol("Liu corta um pedaço do Bolo de Chocolate e te serve."),
        TalkingSymbol("Liu: Bolo de Chocolate!")
    ]

def askcroissantdessert_interesteddessert(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Eu acho que vou de Croissant."),
        TalkingSymbol("Liu pega um Croissant da vitrine e te entrega."),
        TalkingSymbol("Liu: Croissant! Como pedido.")
    ]

def askstrawberrypiedessert_interesteddessert(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Eu gostaria uma Torta de Morango."),
        TalkingSymbol("Liu corta um pedaço da Torta de Morango e te serve."),
        TalkingSymbol("Liu: Torta de Morango! A mais pedida!")
    ]

def asksuggestiondessert_interesteddessert(machine, sender, symbol):
    return [
        TalkingSymbol("Você: O que é mais pedido?"),
        TalkingSymbol("Liu: A Torta de Morango acaba bem rápido aqui haha.")
    ]


notinteresteddessert_state = NotInterestedDessertState()
notinteresteddessert_state.register_symbol(AskDessertSymbol, askdessert_notinteresteddessert)

interesteddessert_state = InterestedDessertState()
interesteddessert_state.register_symbol(GiveUpDessertSymbol, giveupdessert_interesteddessert)
interesteddessert_state.register_symbol(AskChocolateCakeDessertSymbol, askchocolatecakedessert_interesteddessert)
interesteddessert_state.register_symbol(AskCroissantDessertSymbol, askcroissantdessert_interesteddessert)
interesteddessert_state.register_symbol(AskStrawberryPieDessertSymbol, askstrawberrypiedessert_interesteddessert)
interesteddessert_state.register_symbol(AskSuggestionDessertSymbol, asksuggestiondessert_interesteddessert)


# =================
# MACHINE
# =================
states = [
    notinteresteddessert_state,
    interesteddessert_state
]


class DessertMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)
