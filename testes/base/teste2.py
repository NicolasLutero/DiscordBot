# teste2.py
from Discord_NPC_RPG_Bot import Machine, BaseSymbol, BaseState, Sender


# =========================================================
# EXEMPLO DE USO
# =========================================================
class Maquina(Machine):
    def __init__(self):
        super().__init__()
        self.estado_atual = "S"


# Símbolos ================================================
class PingA(BaseSymbol):
    pass

class PingB(BaseSymbol):
    pass


# Estados =================================================
class StateS(BaseState):
    def is_active(self, machine: Maquina, sender: Sender) -> bool:
        return machine.estado_atual == "S"

class StateQ1(BaseState):
    def is_active(self, machine: Maquina, sender: Sender) -> bool:
        return machine.estado_atual == "Q1"

class StateQ2(BaseState):
    def is_active(self, machine: Maquina, sender: Sender) -> bool:
        return machine.estado_atual == "Q2"

class StateR1(BaseState):
    def is_active(self, machine: Maquina, sender: Sender) -> bool:
        return machine.estado_atual == "R1"

class StateR2(BaseState):
    def is_active(self, machine: Maquina, sender: Sender) -> bool:
        return machine.estado_atual == "R2"


# Teste Prático ===========================================
m = Maquina()
s = Sender()


state_s = StateS()

def handler_s_a(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "Q1"

def handler_s_b(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "R1"

state_s.register_symbol(PingA, handler_s_a, priority=0)
state_s.register_symbol(PingB, handler_s_b, priority=0)


state_q1 = StateQ1()

def handler_q1_a(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "Q1"

def handler_q1_b(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "Q2"

state_q1.register_symbol(PingA, handler_q1_a, priority=0)
state_q1.register_symbol(PingB, handler_q1_b, priority=0)


state_q2 = StateQ2()

def handler_q2_a(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "Q1"

def handler_q2_b(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "Q2"

state_q2.register_symbol(PingA, handler_q2_a, priority=0)
state_q2.register_symbol(PingB, handler_q2_b, priority=0)


state_r1 = StateR1()

def handler_r1_a(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "R2"

def handler_r1_b(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "R1"

state_r1.register_symbol(PingA, handler_r1_a, priority=0)
state_r1.register_symbol(PingB, handler_r1_b, priority=0)


state_r2 = StateR2()

def handler_r2_a(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "R2"

def handler_r2_b(machine: Maquina, sender: Sender, symbol):
    machine.estado_atual = "R1"

state_r2.register_symbol(PingA, handler_r2_a, priority=0)
state_r2.register_symbol(PingB, handler_r2_b, priority=0)


m.add_state(state_s)
m.add_state(state_q1)
m.add_state(state_q2)
m.add_state(state_r1)
m.add_state(state_r2)

for _ in range(10):
    entrada = input("Digite sua entrada: ")
    m.estado_atual = "S"

    for c in list(entrada):
        if c == "a":
            m.receive(PingA(), s)
        if c == "b":
            m.receive(PingB(), s)

    if m.estado_atual in ["Q1", "R1"]:
        print("Entrada Aceita")
    else:
        print("Entrada Recusada")
