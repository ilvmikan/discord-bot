import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('PREFIX')

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('--------')

    cogs_to_add = ['greetings', 'games', 'admin', 'config', 'profile']

    for cog in cogs_to_add:
        try:
            cog_module = __import__(f'cogs.{cog}', fromlist=[cog])
            cog_class = getattr(cog_module, cog.capitalize())
            await bot.add_cog(cog_class(bot))
        except Exception as e:
            print(f"erro ao adicionar o cog {cog}: {e}")

    print('>>> cogs adicionados <<<')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para executar este comando")
    else:
        print(f"Erro não tratado: {error}")

bot.run(token)