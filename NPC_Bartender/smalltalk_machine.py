# smalltalk_machine.py
from NPC_RPG_BOT import BaseState

from NPC_Bartender.assistant_state_symbol import TalkingSymbol


# =================
# SYMBOL
# =================
class CasualTalkSymbol(TalkingSymbol):
    description = "<Conversar casualmente>"

    def __init__(self):
        super().__init__("Você decide puxar conversa.")


class AskWorkSymbol(TalkingSymbol):
    description = "<Perguntar sobre o trabalho>"

    def __init__(self):
        super().__init__("Você comenta sobre o trabalho dela.")


class AskFavoriteDrinkSymbol(TalkingSymbol):
    description = "<Perguntar bebida favorita>"

    def __init__(self):
        super().__init__("Você pergunta qual é a bebida favorita dela.")


class AskRecommendationSymbol(TalkingSymbol):
    description = "<Pedir recomendação casual>"

    def __init__(self):
        super().__init__("Você pede uma recomendação.")


# =================
# STATES
# =================
class NotTalkingState(BaseState):
    def is_active(self, machine, sender):
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Nothing"
        except Exception:
            return True


class TalkingState(BaseState):
    def is_active(self, machine, sender):
        if not sender.on_coffee_shop:
            return False
        try:
            return machine.relations[sender]["Interested"] == "Talking"
        except Exception:
            return False


# =================
# CONFIGURAÇÃO
# =================
def casualtalk_nottalking(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Talking"
    return [
        TalkingSymbol("Você: Como você está?"),
        TalkingSymbol("Liu: Estou bem! Um pouco ocupada hoje, mas café sempre deixa o dia melhor.")
    ]


def askwork_talking(machine, sender, symbol):
    return [
        TalkingSymbol("Você: Imagino que trabalhe bastante aqui."),
        TalkingSymbol("Liu: Sim hehe, normalmente fica mais cheio de manhã, já que as pessoas estão indo para o trabalho, mas eu gosto desse movimento todo")
    ]


def askfavoritedrink_talking(machine, sender, symbol):
    return [
        TalkingSymbol("Você: Qual é sua bebida favorita?"),
        TalkingSymbol("Liu: Eu adoro cappuccino com um pouco de canela.")
    ]


def askrecommendation_talking(machine, sender, symbol):
    if sender not in machine.relations.keys():
        machine.relations[sender] = {}
    machine.relations[sender]["Interested"] = "Nothing"
    return [
        TalkingSymbol("Você: Então me faça uma recomendação."),
        TalkingSymbol("Liu: Hmm, eu diria para experimentar um cappuccino. É o favorito da casa.")
    ]


nottalking_state = NotTalkingState()
nottalking_state.register_symbol(CasualTalkSymbol, casualtalk_nottalking)

talking_state = TalkingState()
talking_state.register_symbol(AskWorkSymbol, askwork_talking)
talking_state.register_symbol(AskFavoriteDrinkSymbol, askfavoritedrink_talking)
talking_state.register_symbol(AskRecommendationSymbol, askrecommendation_talking)


# =================
# MACHINE
# =================
states = [
    nottalking_state,
    talking_state
]


class SmallTalksMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)
