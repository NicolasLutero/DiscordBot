from Discord_NPC_RPG_Bot import Machine, BaseState, BaseSymbol, Sender


# ============================================
# PLAYER
# ============================================

class Player(Sender):

    def __init__(self):
        super().__init__()

        self.medkits = 1
        self.water = 1
        self.bandages = 1
        self.reputation = 0


# ============================================
# SYMBOL BASE COM TEXTO
# ============================================

class TextSymbol(BaseSymbol):

    description = "Ação"

    def get_text(self):
        return self.description


# ============================================
# SYMBOLS
# ============================================

class TalkSymbol(TextSymbol):
    description = "Conversar com o batedor"


class AskBattleSymbol(TextSymbol):
    description = "Perguntar sobre a batalha"


class GiveMedkitSymbol(TextSymbol):
    description = "Usar kit médico no batedor"


class GiveWaterSymbol(TextSymbol):
    description = "Oferecer água"


class EncourageSymbol(TextSymbol):
    description = "Tentar encorajar o batedor"


class AskSecretSymbol(TextSymbol):
    description = "Perguntar sobre rotas secretas do inimigo"


class WaitSymbol(TextSymbol):
    description = "Aguardar um momento"


# ============================================
# NPC MACHINE
# ============================================

class ScoutNPC(Machine):

    def __init__(self):

        super().__init__()

        self.health = 40
        self.max_health = 100

        self.morale = 20
        self.trust_required = 5

        self.secret_revealed = False
        self.dead = False


# ============================================
# STATES
# ============================================

class AliveState(BaseState):

    def is_active(self, machine, sender):
        return not machine.dead


class WoundedState(BaseState):

    def is_active(self, machine, sender):
        return machine.health < 60 and not machine.dead


class LowMoraleState(BaseState):

    def is_active(self, machine, sender):
        return machine.morale < 40 and not machine.dead


class TrustState(BaseState):

    def is_active(self, machine, sender):

        relation = machine.relations.get(sender.get_id(), {})

        trust = relation.get("trust", 0)

        return trust >= machine.trust_required


# ============================================
# HANDLERS
# ============================================

def talk_handler(machine, sender, symbol):

    print("Batedor: ... pensei que ninguém viria.")

    relation = machine.relations.setdefault(sender.get_id(), {})
    relation["trust"] = relation.get("trust", 0) + 1


def battle_handler(machine, sender, symbol):

    print("Batedor: Estamos segurando o inimigo...")
    print("Batedor: mas eles têm mais tropas.")

    machine.morale -= 2


def pain_handler(machine, sender, symbol):

    print("Batedor: Argh... meu ferimento...")


def medkit_handler(machine, sender, symbol):

    if sender.medkits <= 0:
        print("Você não possui kit médico.")
        return

    sender.medkits -= 1

    machine.health += 40

    if machine.health > machine.max_health:
        machine.health = machine.max_health

    print("Você trata os ferimentos do batedor.")

    relation = machine.relations.setdefault(sender.get_id(), {})
    relation["trust"] = relation.get("trust", 0) + 3


def water_handler(machine, sender, symbol):

    if sender.water <= 0:
        print("Você não possui água.")
        return

    sender.water -= 1

    machine.morale += 10

    print("O batedor bebe água e parece mais disposto.")


def encourage_handler(machine, sender, symbol):

    print("Você tenta encorajar o batedor.")

    machine.morale += 5

    relation = machine.relations.setdefault(sender.get_id(), {})
    relation["trust"] = relation.get("trust", 0) + 1


def secret_handler(machine, sender, symbol):

    relation = machine.relations.setdefault(sender.get_id(), {})

    trust = relation.get("trust", 0)

    if trust < machine.trust_required:
        print("Batedor: Não posso confiar essa informação ainda...")
        return

    if machine.morale < 40:
        print("Batedor: Eu... não consigo pensar direito agora...")
        return

    print("Batedor: Há uma passagem atrás das colinas ao norte.")
    print("Batedor: Os inimigos usam para trazer reforços.")

    machine.secret_revealed = True


def wait_handler(machine, sender, symbol):

    machine.health -= 5
    machine.morale -= 2

    print("O tempo passa...")

    if machine.health <= 0:
        machine.dead = True
        print("O batedor não resistiu aos ferimentos.")


# ============================================
# SETUP
# ============================================

npc = ScoutNPC()
player = Player()


alive_state = AliveState()
wounded_state = WoundedState()
morale_state = LowMoraleState()
trust_state = TrustState()


alive_state.register_symbol(TalkSymbol, talk_handler)
alive_state.register_symbol(AskBattleSymbol, battle_handler)
alive_state.register_symbol(WaitSymbol, wait_handler)

wounded_state.register_symbol(TalkSymbol, pain_handler, priority=10)
wounded_state.register_symbol(GiveMedkitSymbol, medkit_handler)
wounded_state.register_symbol(GiveWaterSymbol, water_handler)

morale_state.register_symbol(EncourageSymbol, encourage_handler)

trust_state.register_symbol(AskSecretSymbol, secret_handler)


npc.add_state(alive_state)
npc.add_state(wounded_state)
npc.add_state(morale_state)
npc.add_state(trust_state)


# ============================================
# LOOP
# ============================================

while True:

    if npc.dead:
        break

    print("\n====== ACAMPAMENTO AVANÇADO ======")

    print("Saúde do batedor:", npc.health)
    print("Moral do batedor:", npc.morale)

    relation = npc.relations.get(player.get_id(), {})
    print("Confiança:", relation.get("trust", 0))

    print("\n0 - Encerrar")

    accepted = list(npc.accepted_symbols(player))

    for i, symbol_cls in enumerate(accepted, start=1):

        text = symbol_cls().get_text()

        print(f"{i} - {text}")

    choice = input("Escolha: ")

    if not choice.isdigit():
        continue

    choice = int(choice)

    if choice == 0:
        break

    if choice > len(accepted):
        continue

    symbol = accepted[choice - 1]()

    npc.receive(symbol, player)


# ============================================
# FINAL
# ============================================

print("\n====== RESULTADO ======")

if npc.secret_revealed:
    print("Você descobriu a passagem secreta do inimigo.")
    print("Isso pode mudar o rumo da guerra.")

elif npc.dead:
    print("O batedor morreu antes de revelar qualquer informação.")

else:
    print("Você deixou o acampamento sem descobrir nada importante.")
