import discord
import json
from discord import app_commands

from NPC_Bartender import *
from NPC_RPG_BOT import Sender

senders = {}


# ======================
# CLASSE DO BOT
# ======================

class DiscordBOT(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.machine = liu_machine

    # ======================
    # SENDER
    # ======================
    @staticmethod
    def get_sender(interaction):
        user_id = interaction.user.id
        if user_id not in senders.keys():
            senders[user_id] = Player()
        return senders[user_id]

    async def check_sender(self, symbol: type, sender: Sender, interaction: discord.Interaction):
        if symbol not in self.machine.accepted_symbols(sender):
            await interaction.response.send_message("Essa ação não está disponível agora.")
            return False
        return True

    # =======================
    # HOOKS DO DISCORD
    # =======================

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"O bot {self.user} foi ligado com sucesso.")


# ======================
# CRIAÇÃO DO BOT
# ======================
bot = DiscordBOT()

# ----------------------
# Comando /simbolos
# ----------------------
@bot.tree.command(name="simbolos")
async def simbolos(interaction: discord.Interaction):
    sender = bot.get_sender(interaction)
    available = bot.machine.accepted_symbols(sender)
    if not available:
        await interaction.response.send_message("Nenhuma ação disponível.")
        return
    msg = "\n".join(
        f"/{symbol.__name__.replace('Symbol','').lower()} - {symbol.description}"
        for symbol in available
    )
    await interaction.response.send_message(msg)


# ----------------------
# Comandos de Symbols
# ----------------------
async def action(interaction, symbol):
    sender = bot.get_sender(interaction)
    if not await bot.check_sender(type(symbol), sender, interaction):
        return
    result = bot.machine.receive(symbol, sender)
    retorno = ""
    for conjunto_retorno in result["retornos"]:
        for parte_retorno in conjunto_retorno:
            retorno += f"{parte_retorno}\n"
        retorno += "\n"
    if retorno == "":
        retorno = "..."
    await interaction.response.send_message(retorno)

# FORA DA CAFETERIA
@bot.tree.command(name="getin")
async def getin(interaction: discord.Interaction):
    await action(interaction, GetInSymbol())

#
@bot.tree.command(name="askcoffee")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskCoffeeSymbol())

#
@bot.tree.command(name="giveupcoffee")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, GiveUpCoffeeSymbol())

#
@bot.tree.command(name="askespressocoffee")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskEspressoCoffeeSymbol())

#
@bot.tree.command(name="askcappuccinocoffee")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskCappuccinoCoffeeSymbol())

#
@bot.tree.command(name="askcoffeewithmilk")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskCoffeeWithMilkSymbol())

#
@bot.tree.command(name="asksuggestioncoffee")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskSuggestionCoffeeSymbol())



#
@bot.tree.command(name="askdessert")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskDessertSymbol())

#
@bot.tree.command(name="giveupdessert")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, GiveUpDessertSymbol())

#
@bot.tree.command(name="askchocolatecakedessert")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskChocolateCakeDessertSymbol())

#
@bot.tree.command(name="askcroissantdessert")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskCroissantDessertSymbol())

#
@bot.tree.command(name="askstrawberrypiedessert")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskStrawberryPieDessertSymbol())

#
@bot.tree.command(name="asksuggestiondessert")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskSuggestionDessertSymbol())



#
@bot.tree.command(name="justlooking")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, JustLookingSymbol())

#
@bot.tree.command(name="makeorder")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, MakeOrderSymbol())

#
@bot.tree.command(name="thanks")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, ThanksSymbol())

#
@bot.tree.command(name="aboutaroma")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AboutAromaSymbol())

#
@bot.tree.command(name="seemenu")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, SeeMenuSymbol())



#
@bot.tree.command(name="casualtalk")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, CasualTalkSymbol())

#
@bot.tree.command(name="askwork")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskWorkSymbol())

#
@bot.tree.command(name="askfavoritedrink")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskFavoriteDrinkSymbol())

#
@bot.tree.command(name="askrecommendation")
async def askcoffee(interaction: discord.Interaction):
    await action(interaction, AskRecommendationSymbol())


# =================
# CHAVE DO BOT
# =================
def load_token():
    try:
        with open("token.json", "r") as f:
            dados = json.load(f)
            return dict(dados)["token"]
    except FileNotFoundError:
        return None


bot.run(load_token())
