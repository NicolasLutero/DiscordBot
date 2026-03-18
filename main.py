import discord
from discord import app_commands

from NPC_Bartender import *
from NPC_RPG_BOT.sender import Sender

senders = {}


class Player(Sender):
    def __init__(self):
        super().__init__()
        self.on_coffee_shop = False


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

    async def check_sender(self, symbol: type, sender: Sender):
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
async def action(interaction, symbol, sender):
    if not await bot.check_sender(type(symbol), sender):
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
    sender = bot.get_sender(interaction)
    symbol = GetInSymbol
    await action(interaction, symbol(), sender)

# ACABOU DE ENTRAR
@bot.tree.command(name="askcoffee")
async def askcoffee(interaction: discord.Interaction):
    sender = bot.get_sender(interaction)
    symbol = AskCoffeeSymbol
    await action(interaction, symbol(), sender)

bot.run("MTQ3OTIxMjg5NTU1MTM2MTA1NA.GmbVz4.7z01ltu1uIFleAWmHsaI-_OYcsiHEKcS7PRBZo")
