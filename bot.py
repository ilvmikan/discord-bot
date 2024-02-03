import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from cogs.greetings import Greetings
from cogs.games import Games
from cogs.admin import Admin
from cogs.server_config import Config
from cogs.user_profile.profile import Profile
from cogs.apis import Unsplash_random_image

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
    await bot.add_cog(Greetings(bot))
    await bot.add_cog(Games(bot))
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Config(bot))
    await bot.add_cog(Profile(bot))
    await bot.add_cog(Unsplash_random_image(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para executar este comando")
    else:
        print(f"Erro não tratado: {error}")

bot.run(token)