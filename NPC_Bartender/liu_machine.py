# liu_machine.py
from NPC_RPG_BOT import Machine, Sender

from NPC_Bartender.outin_machine import OutInMachine
from NPC_Bartender.coffee_machine import CoffeeMachine
from NPC_Bartender.dessert_machine import DessertMachine
from NPC_Bartender.coffeetalk_machine import CoffeeTalkMachine
from NPC_Bartender.smalltalk_machine import SmallTalksMachine


class LiuMachine(
        OutInMachine,
        CoffeeMachine,
        DessertMachine,
        CoffeeTalkMachine,
        SmallTalksMachine,
        Machine
    ):

    def __init__(self):
        super().__init__()
        self.relations = {}


liu_machine = LiuMachine()

class Player(Sender):
    def __init__(self):
        super().__init__()
        self.on_coffee_shop = False


if __name__ == "__main__":
    player = Player()
    while True:
        print("0 - Sair")
        simbolos = list(liu_machine.accepted_symbols(player))
        for n, simbolo in enumerate(simbolos):
            print(f"{n+1} - {simbolo}")
        resp = int(input("R: "))

        if resp < 1 or resp > len(simbolos):
            break
        else:
            reportado = liu_machine.receive(simbolos[resp-1](), player)
            for erro in reportado["errors"]:
                raise erro
            txt_retorno = ""
            for retornos in reportado["retornos"]:
                for retorno in retornos:
                    txt_retorno += str(retorno) + "\n"
                txt_retorno += "\n"
            if txt_retorno.replace("\n", "") == "":
                txt_retorno = "..."
            print(txt_retorno[:-1])
