import discord
from discord import app_commands

from NPC_Bartender import *
from Discord_NPC_RPG_BOT.sender import Sender

senders = {}

# ======================
# CLASSE DO BOT
# ======================

class DiscordBOT(discord.Client):

    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
        self.machine = bartender_machine

    # ======================
    # SENDER
    # ======================

    @staticmethod
    def get_sender(interaction):
        user_id = interaction.user.id
        if user_id not in senders.keys():
            senders[user_id] = Sender()
        return senders[user_id]

    # ======================
    # HOOKS DO DISCORD
    # ======================

    async def setup_hook(self):
        # Limpa e sincroniza usando apenas o ID
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
@bot.tree.command(name="introduceyourself")
async def introduceyourself(interaction: discord.Interaction, nome: str):
    sender = bot.get_sender(interaction)
    if IntroduceYourselfSymbol not in bot.machine.accepted_symbols(sender):
        await interaction.response.send_message("Essa ação não está disponível agora.")
        return
    symbol = IntroduceYourselfSymbol(nome)
    result = bot.machine.receive(symbol, sender)
    retorno = ""
    for conjunto_retorno in result["retornos"]:
        for parte_retorno in conjunto_retorno:
            retorno += f"{parte_retorno}\n"
        retorno += "\n"
    await interaction.response.send_message(retorno)


@bot.tree.command(name="talkalittle")
async def talkalittle(interaction: discord.Interaction):
    sender = bot.get_sender(interaction)
    if TalkALittleSymbol not in bot.machine.accepted_symbols(sender):
        await interaction.response.send_message("Essa ação não está disponível agora.")
        return
    symbol = TalkALittleSymbol()
    result = bot.machine.receive(symbol, sender)
    await interaction.response.send_message(result)


@bot.tree.command(name="talk")
async def talk(interaction: discord.Interaction):
    sender = bot.get_sender(interaction)
    if TalkSymbol not in bot.machine.accepted_symbols(sender):
        await interaction.response.send_message("Essa ação não está disponível agora.")
        return
    symbol = TalkSymbol()
    result = bot.machine.receive(symbol, sender)
    await interaction.response.send_message(result)


@bot.tree.command(name="talkalot")
async def talkalot(interaction: discord.Interaction):
    sender = bot.get_sender(interaction)
    if TalkALotSymbol not in bot.machine.accepted_symbols(sender):
        await interaction.response.send_message("Essa ação não está disponível agora.")
        return
    symbol = TalkALotSymbol()
    result = bot.machine.receive(symbol, sender)
    await interaction.response.send_message(result)


bot.run("MTQ3OTIxMjg5NTU1MTM2MTA1NA.GmbVz4.7z01ltu1uIFleAWmHsaI-_OYcsiHEKcS7PRBZo")
