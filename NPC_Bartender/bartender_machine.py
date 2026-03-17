# bartender_machine.py
from Discord_NPC_RPG_BOT import Machine, Sender

from NPC_Bartender.lore_machine import LoreConversationMachine


# ======================
# COMBINAÇÃO DE MAQUINAS
# ======================

class BartenderMachine(
        LoreConversationMachine,
        Machine
        ):
    def __init__(self):
        super().__init__()


bartender_machine = BartenderMachine()

if __name__ == "__main__":
    player = Sender()

    while True:
        print("0 - Sair")
        simbolos = list(bartender_machine.accepted_symbols(player))
        for n, simbolo in enumerate(simbolos):
            print(f"{n+1} - {simbolo}")
        resp = int(input("R: "))
        if resp == 0:
            break
        if 0 < resp <= len(simbolos):
            simbolo = simbolos[resp-1]()
            print(f"{simbolo.msm}")
            retornos_por_handlers = bartender_machine.receive(simbolo, player)["retornos"]
            for retornos_do_handler in retornos_por_handlers:
                for retorno in retornos_do_handler:
                    print(retorno)
        if resp < 0:
            print("Opição Inválida")
