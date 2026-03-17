# lore_machine.py
from Discord_NPC_RPG_BOT import BaseState

from NPC_Bartender.assistant_state_symbol import TalkingSymbol


# =================
# SYMBOL
# =================
class IntroduceYourselfSymbol(TalkingSymbol):
    description = "<Se apresentar>"

    def __init__(self):
        self.name = input("Se apresentar como: ")
        super().__init__(f"{self.name}: Olá, meu nome é {self.name}")


class TalkALittleSymbol(TalkingSymbol):
    description = "<Conversar Pouco>"

    def __init__(self):
        super().__init__(f"* Vocês conversam um pouco. *")


class TalkSymbol(TalkingSymbol):
    description = "<Conversar>"

    def __init__(self):
        super().__init__(f"* Vocês conversam. *")


class TalkALotSymbol(TalkingSymbol):
    description = "<Conversar Muito>"

    def __init__(self):
        super().__init__(f"* Vocês conversam muito. *")


# =================
# STATES
# =================
class StrangerState(BaseState):
    def is_active(self, machine, sender):
        return sender not in machine.knows_people.keys()


class AcquaintanceState(BaseState):
    def is_active(self, machine, sender):
        acquaintance = sender in machine.knows_people.keys()
        if acquaintance:
            not_partner = machine.knows_people[sender]["conversations"] <= 7
            if not_partner:
                return True
        return False


class PartnerState(BaseState):
    def is_active(self, machine, sender):
        acquaintance = sender in machine.knows_people.keys()
        if acquaintance:
            partner = 20 > machine.knows_people[sender]["conversations"] > 7
            return partner
        return False


class CloseState(BaseState):
    def is_active(self, machine, sender):
        acquaintance = sender in machine.knows_people.keys()
        if acquaintance:
            close = machine.knows_people[sender]["conversations"] >= 20
            return close
        return False


# =================
# CONFIGURAÇÃO
# =================
def introduceyourself_stranger(machine, sender, symbol):
    if sender not in machine.knows_people.keys():
        machine.knows_people[sender] = {}
    machine.knows_people[sender]["name"] = symbol.name
    machine.knows_people[sender]["conversations"] = 1

    return [TalkingSymbol(f"{machine.bot_name}: Olá {symbol.name}! Sou {machine.bot_name}.")]

def talk_state(machine, sender, symbol):
    if isinstance(symbol, TalkALittleSymbol): conversations = 3
    elif isinstance(symbol, TalkSymbol): conversations = 5
    elif isinstance(symbol, TalkALotSymbol): conversations = 7
    else: conversations = 0
    machine.knows_people[sender]["conversations"] += conversations


stranger_state = StrangerState()
stranger_state.register_symbol(IntroduceYourselfSymbol, introduceyourself_stranger)

acquaintance_state = AcquaintanceState()
acquaintance_state.register_symbol(TalkALittleSymbol, talk_state)

partner_state = PartnerState()
partner_state.register_symbol(TalkALittleSymbol, talk_state)
partner_state.register_symbol(TalkSymbol, talk_state)

close_state = CloseState()
close_state.register_symbol(TalkALittleSymbol, talk_state)
close_state.register_symbol(TalkSymbol, talk_state)
close_state.register_symbol(TalkALotSymbol, talk_state)


# =================
# MACHINE
# =================
states = [
    stranger_state,
    acquaintance_state,
    partner_state,
    close_state
]


class LoreConversationMachine:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_states(states)

        self.bot_name = "Liu"
        self.knows_people = {}

