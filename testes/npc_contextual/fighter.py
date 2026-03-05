from Discord_NPC_RPG_Bot import Machine, BaseState, BaseSymbol, Sender


# =========================
# PLAYER
# =========================

class Player(Sender):

    def __init__(self):
        super().__init__()
        self.has_medkit = True
        self.has_water = True


# =========================
# SYMBOLS
# =========================

class TalkSymbol(BaseSymbol):
    pass


class AskBattleSymbol(BaseSymbol):
    pass


class GiveMedkitSymbol(BaseSymbol):
    pass


class GiveWaterSymbol(BaseSymbol):
    pass


class AskMissionSymbol(BaseSymbol):
    pass


# =========================
# STATES
# =========================

class WoundedState(BaseState):

    def is_active(self, machine, sender):
        return machine.wounded


class HealthyState(BaseState):

    def is_active(self, machine, sender):
        return not machine.wounded


class IdleState(BaseState):

    def is_active(self, machine, sender):
        return True


# =========================
# HANDLERS
# =========================

def talk_handler(machine, sender, symbol):

    if machine.wounded:
        print("Guerreiro: *respira com dificuldade* ... a batalha está intensa...")
    else:
        print("Guerreiro: Graças a você estou melhor. Ainda consigo lutar.")


def ask_battle_handler(machine, sender, symbol):

    print("Guerreiro: A linha de frente está a algumas centenas de metros.")
    print("Guerreiro: Estamos tentando segurar os inimigos até chegarem reforços.")

    machine.battle_info_given = True


def pain_handler(machine, sender, symbol):

    print("Guerreiro: Argh... minha perna ainda dói...")


def give_medkit_handler(machine, sender, symbol):

    if not sender.has_medkit:
        print("Você não tem kit médico.")
        return

    if not machine.wounded:
        print("Guerreiro: Já estou bem.")
        return

    sender.has_medkit = False
    machine.wounded = False

    print("Você usa o kit médico para tratar o ferimento.")
    print("Guerreiro: Obrigado... você salvou minha vida.")


def give_water_handler(machine, sender, symbol):

    if not sender.has_water:
        print("Você não tem água.")
        return

    sender.has_water = False

    print("Você oferece água ao guerreiro.")
    print("Guerreiro: Obrigado... isso ajuda.")


def mission_handler(machine, sender, symbol):

    if machine.wounded:
        print("Guerreiro: Eu iria pedir ajuda... mas mal consigo ficar de pé.")
        return

    print("Guerreiro: Se você puder ajudar, leve esta mensagem ao comandante.")
    print("MISSÃO RECEBIDA: entregar mensagem ao comandante.")

    machine.mission_given = True


# =========================
# NPC MACHINE
# =========================

class WarriorNPC(Machine):

    def __init__(self):

        super().__init__()

        self.wounded = True
        self.battle_info_given = False
        self.mission_given = False


# =========================
# SETUP NPC
# =========================

npc = WarriorNPC()
player = Player()


# Estados

wounded_state = WoundedState()
healthy_state = HealthyState()
idle_state = IdleState()


# Registro de handlers

idle_state.register_symbol(TalkSymbol, talk_handler)
idle_state.register_symbol(AskBattleSymbol, ask_battle_handler)

wounded_state.register_symbol(TalkSymbol, pain_handler, priority=10)
wounded_state.register_symbol(GiveMedkitSymbol, give_medkit_handler)
wounded_state.register_symbol(GiveWaterSymbol, give_water_handler)

healthy_state.register_symbol(AskMissionSymbol, mission_handler)


npc.add_state(idle_state)
npc.add_state(wounded_state)
npc.add_state(healthy_state)


# =========================
# SYMBOL MENU
# =========================

symbol_menu = {
    TalkSymbol: "Conversar com o guerreiro",
    AskBattleSymbol: "Perguntar sobre a batalha",
    GiveMedkitSymbol: "Oferecer kit médico",
    GiveWaterSymbol: "Oferecer água",
    AskMissionSymbol: "Pedir uma missão"
}


# =========================
# LOOP DE INTERAÇÃO
# =========================

while True:

    print("\n--- ACAMPAMENTO DE GUERRA ---")
    print("Um guerreiro ferido está sentado próximo a uma fogueira.")
    print()

    accepted = npc.accepted_symbols(player)

    options = [None] + list(accepted)

    print("0 - Encerrar interação")

    for i, sym in enumerate(options[1:], start=1):
        print(f"{i} - {symbol_menu.get(sym, sym.__name__)}")

    choice = input("Escolha uma opção: ")

    if not choice.isdigit():
        continue

    choice = int(choice)

    if choice == 0:
        print("Encerrando.")
        break

    if choice >= len(options):
        continue

    symbol_class = options[choice]

    symbol_instance = symbol_class()

    npc.receive(symbol_instance, player)


# =========================
# FINAL
# =========================

print("\n--- RESULTADO ---")

if npc.mission_given:
    print("Você conseguiu ajudar o guerreiro e recebeu uma missão.")
elif npc.wounded:
    print("Você deixou o guerreiro ferido no acampamento.")
else:
    print("O guerreiro sobreviveu graças a você.")
