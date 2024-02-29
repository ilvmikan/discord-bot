from discord.ext import commands
import requests
from discord import Embed as DiscordEmbed
from dotenv import load_dotenv
import os

load_dotenv()

class Embed:
    def __init__(self, title=None, description=None, color=None, image=None):
        self.embed = DiscordEmbed(title=title, description=description, color=color)
        if image:
            self.embed.set_image(url=image)
    
    def set_title(self, title):
        self.embed.title = title
        return self

    def set_description(self, description):
        self.embed.description = description
        return self
    
    def set_color(self, color):
        self.embed.color = color
        return self
    
    def set_image(self, image):
        self.embed.set_image(url=image)
        return self
    
    def add_field(self, name, value, inline=False):
        self.embed.add_field(name=name, value=value, inline=inline)
        return self

    def build(self):
        return self.embed


class Apis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.unsplash_api = UnsplashAPI()
        self.advice_api = AdviceAPI()

    @commands.command(name='help_apis')
    async def _help_apis(self, ctx):
        embed = Embed(title='Comandos relacionado as Apis')
        embed.set_description('Aqui estão os comandos disponíveis para a classe Apis:')
        embed.add_field(name='!unsplash_random', value='Obtenha uma imagem aleatória do Unsplash.', inline=False)
        embed.add_field(name='!advice', value='Receba um conselho aleatório.', inline=False)
        await ctx.send(embed=embed.build())

    @commands.command(name='unsplash_random')
    async def _random_unsplash(self, ctx):
        photo_info = self.unsplash_api.get_random_photo_info()
        if photo_info:
            embed = Embed(description=photo_info['photo_description'], image=photo_info['photo_url'])
            await ctx.send(embed=embed.build())

    @commands.command(name='advice')
    async def _random_advice(self, ctx):
        advice_text = self.advice_api.get_random_advice()
        if advice_text:
            embed = Embed(title='Conselho do dia', description=advice_text, color=0xfc0303)
            await ctx.send(embed=embed.build())

    

class UnsplashAPI:
    def __init__(self):
        self.access_key = os.getenv('UNSPLASH_ACCESS_KEY')
        self.url = 'https://api.unsplash.com/'
        self.headers = {'Authorization': f'Client-ID {self.access_key}'}

    def get_random_photo_info(self):
        api_info = requests.get(f'{self.url}photos/random', headers=self.headers)

        if api_info.status_code == 200:
            photo_data = api_info.json()
            
            if 'urls' in photo_data and 'regular' in photo_data['urls']:
                photo_url = photo_data['urls']['regular']
            else:
                print('Chave "urls" ou "regular" não encontrada no JSON.')
                return None

            photo_description = photo_data.get('description', 'Descrição não disponível')
            
            return {'photo_url': photo_url, 'photo_description': photo_description}
        else:
            print(f'Erro na solicitação Unsplash: {api_info.status_code}')
            return None


class AdviceAPI:
    def __init__(self):
        self.url = 'https://api.adviceslip.com/advice'

    def get_random_advice(self):
        advice_response = requests.get(self.url)
        if advice_response.status_code == 200:
            advice_data = advice_response.json()
            return advice_data['slip']['advice']
        else:
            print(f'Erro na solicitação: {advice_response.status_code}')
            return None
        

def setup(bot):
    bot.add_cog(Apis(bot))
