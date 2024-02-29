from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

load_dotenv()

unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY')
url = 'https://api.unsplash.com/'
headers = {'Authorization': f'Client-ID {unsplash_access_key}'}

class Apis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='uimg', invoke_without_command=True)
    async def _uimg(self, ctx):
        await ctx.reply('!uimg <comando>')

    @_uimg.command(name='random')
    async def _random(self, ctx):
        api_info = requests.get(f'{url}photos/random', headers=headers)

        if api_info.status_code == 200:
            photo_url = api_info.json()['urls']['regular']
            await ctx.send(photo_url)
        else:
            print(f'Erro na solicitação: {api_info.status_code}')





            

def setup(bot):
    bot.add_cog(Apis(bot))