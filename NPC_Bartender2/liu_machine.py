# coffee_shop_machine.py

from Discord_NPC_RPG_BOT import Machine, Sender

from NPC_Bartender2.outin_machine import OutInMachine
from NPC_Bartender2.coffee_machine import CoffeeMachine
#from NPC_Bartender2.desert_machine import DessertMachine
#from NPC_Bartender2.coffeetalk_machine import CoffeeTalkMachine
#from NPC_Bartender2.smalltalk_machine import SmallTalkMachine


class LiuMachine(
        OutInMachine,
        CoffeeMachine,
        #DessertMachine,
        #CoffeeTalkMachine,
        #SmallTalkMachine,
        Machine
    ):

    def __init__(self):
        super().__init__()
        self.relations = {}


liu_machine = LiuMachine()


"""
# =================
# TESTE DE USO
# =================
class Player(Sender):
    def __init__(self):
        super().__init__()
        self.on_coffee_shop = False


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
        conjunto_retornos = liu_machine.receive(simbolos[resp-1](), player)["retornos"]
        for retornos in conjunto_retornos:
            for retorno in retornos:
                print(retorno)
"""
