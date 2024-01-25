from discord.ext import commands
import discord
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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