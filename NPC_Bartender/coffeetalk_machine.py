# coffeetalk_machine.py
from NPC_RPG_BOT import BaseState, BaseSymbol

from NPC_Bartender.assistant_state_symbol import TalkingSymbol

txt_menu = ("Menu"
            "\nCafés:"
            "\n - Expresso"
            "\n - Cappuccino"
            "\n - Café com Leite"
            "\nDoces:"
            "\n - Bolo de Chocolate"
            "\n - Torta de Morango"
            "\n - Croissant")


# =================
# SYMBOL
# =================
class JustLookingSymbol(TalkingSymbol):
    description = "<Apenas Olhando>"

    def __init__(self):
        super().__init__("Você diz que esta apenas olhando.")


class MakeOrderSymbol(TalkingSymbol):
    description = "<Pedir alguma coisa>"

    def __init__(self):
        super().__init__("Você decide pedir alguma coisa.")


class ThanksSymbol(TalkingSymbol):
    description = "<Agradecer a educação>"

    def __init__(self):
        super().__init__("Você agradece.")


class AboutAromaSymbol(TalkingSymbol):
    description = "<Comentar sobre o Aroma>"

    def __init__(self):
        super().__init__("Você comenta sobre o aroma.")


class SeeMenuSymbol(BaseSymbol):
    description = "<Olhar o menu de parede>"

    def __init__(self):
        super().__init__()


# =================
# STATES
# =================
class NotServedState(BaseState):
    def is_active(self, machine, sender):
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Nothing"
        except Exception:
            return True


class JustLookingState(BaseState):
    def is_active(self, machine, sender) -> bool:
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Looking"
        except Exception:
            return False


# =================
# CONFIGURAÇÃO
# =================
def justlooking_notserved(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Looking"
    return [
        TalkingSymbol("Você: Estou só olhando."),
        TalkingSymbol("Liu: Sem problema! Fique à vontade. Se precisar de alguma recomendação é só falar.")
    ]

def makeorder_justlooking(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Já decidi o que pedir."),
        TalkingSymbol("Liu: E o que seria?")
    ]

def thanks_justlooking(machine, sender, symbol):
    return [
        TalkingSymbol("Você: Obrigado."),
        TalkingSymbol("Liu sorri levemente e volta a arrumar outras coisas da cafeteria.")
    ]

def aboutaroma_justlooking(machine, sender, symbol):
    return [
        TalkingSymbol("Você: O aroma do café está ótimo."),
        TalkingSymbol("Liu: Está mesmo, sem dúvidas é o melhor café da região, grãos de primeira qualidade!"),
        TalkingSymbol("Liu: Já decidiu ou quer alguma sugestão?")
    ]

def seemenu_justlooking(machine, sender, symbol):
    return [
        TalkingSymbol("Você fica em silêncio olhando o cardápio na parede."),
        TalkingSymbol("Liu: É um belo cardápio não?"),
        TalkingSymbol(txt_menu)
    ]


notserved_state = NotServedState()
notserved_state.register_symbol(JustLookingSymbol, justlooking_notserved)

justlooking_state = JustLookingState()
justlooking_state.register_symbol(MakeOrderSymbol, makeorder_justlooking)
justlooking_state.register_symbol(ThanksSymbol, thanks_justlooking)
justlooking_state.register_symbol(AboutAromaSymbol, aboutaroma_justlooking)
justlooking_state.register_symbol(SeeMenuSymbol, seemenu_justlooking)


# =================
# MACHINE
# =================
states = [
    notserved_state,
    justlooking_state
]


class CoffeeTalkMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)
