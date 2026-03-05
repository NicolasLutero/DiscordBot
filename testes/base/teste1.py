# teste1.py
from Discord_NPC_RPG_Bot import BaseState, Sender, BaseSymbol, Machine

# =========================================================
# EXEMPLO DE USO
# =========================================================

# Variaveis globais =======================================
counter = 0


# Símbolos ================================================
class PingA(BaseSymbol):
    def __init__(self, value: int):
        self.value = value

class PingB(BaseSymbol):
    def __init__(self, value: int):
        self.value = value


# Estados =================================================
class AlwaysActiveState(BaseState):
    def is_active(self, machine: Machine, sender: Sender) -> bool:
        return True


# Teste Prático ===========================================
m = Machine()
s = Sender()

state1 = AlwaysActiveState()
state2 = AlwaysActiveState()

def handler_a(machine: Machine, sender: Sender, symbol):
    global counter
    counter += symbol.value

def handler_b(machine: Machine, sender: Sender, symbol):
    global counter
    counter -= symbol.value

state1.register_symbol(PingA, handler_a, priority=1)
state2.register_symbol(PingB, handler_b, priority=0)

m.add_state(state1)
m.add_state(state2)

erros = [
    m.receive(PingA(5), sender=s),
    m.receive(PingA(7), sender=s),
    m.receive(PingA("a"), sender=s),
    m.receive(PingB(5), sender=s),
    m.receive(PingB(2), sender=s)
]

for n, cod in enumerate(erros):
    print(f"Erros do código: {n+1}")
    for e in cod:
        print(e)

print("Valor final global counter:", counter)
