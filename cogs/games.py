from discord.ext import commands
import random
from discord import Embed as DiscordEmbed

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    """
        TENTANDO CRIAR UM PEDRA, PAPEL e TESOURA
        (forma horrivel)
        REGRA: FAZER FUNCIONAR E DEPOIS REFATORAR
    """
    @commands.Cog.listener()
    async def on_message(self, msg):
        conteudo = msg.content.lower()
        options = ['pedra', 'papel', 'tesoura']

        if conteudo not in options:
            return

        result = random.choice(options)

        outcomes = {
            ('pedra', 'pedra'): "Droga, deu empate!",
            ('papel', 'papel'): "Droga, deu empate!",
            ('tesoura', 'tesoura'): "Droga, deu empate!",
            ('pedra', 'papel'): "Você perdeu!",
            ('papel', 'tesoura'): "Você perdeu!",
            ('tesoura', 'pedra'): "Você perdeu!",
        }

        if (conteudo, result) in outcomes:
            await msg.channel.send(f"{outcomes[(conteudo, result)]}\nVocê: {conteudo}\nMinha escolha: {result}")
        else:
            await msg.channel.send(f"Você ganhou!\nVocê escolheu {conteudo}\nMinha escolha foi: {result}")


    @commands.group(name='game', invoke_without_command=True)
    async def game(self, ctx):
        await ctx.channel.send('!game <command>')

    @game.command(name='coinflip')
    async def _coinflip(self, ctx):
        result = random.choice(['cara', 'coroa'])
        msg_author = ctx.author.mention
        await ctx.send(f"{msg_author}, deu __**{result}**__!")

def setup(bot):
    bot.add_cog(Games(bot))
