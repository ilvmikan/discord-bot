from discord.ext import commands
import random
from discord import Embed as DiscordEmbed

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        msg_escolha = msg.content.lower()
        options = ['pedra', 'papel', 'tesoura']

        if msg_escolha not in options:
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
        
        title = "Você ganhou!"

        if (msg_escolha, result) in outcomes:
            title = outcomes[(msg_escolha, result)]

        embed = DiscordEmbed(  
                    title = title,
                    description = f"Você: {msg_escolha}\nMinha escolha: {result}"
                )

        await msg.channel.send(embed=embed)


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
