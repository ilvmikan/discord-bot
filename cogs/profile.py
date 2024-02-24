from discord.ext import commands
import discord
import requests
import imghdr
from database.db import *

def is_valid_image(url):
    try:
        response = requests.get(url, stream=True)
        if 'image' not in response.headers['Content-Type']:
            return False
        image_type = imghdr.what(None, response.content)
        return image_type in ['jpeg', 'png']
    except Exception as e:
        print(f"Erro ao verificar a imagem: {e}")
        return False


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database('database/discord_bot.db')
        self.user_profile = UserProfile(db_name='database/discord_bot.db')

    @commands.group(name='profile', invoke_without_command=True)
    @commands.guild_only()
    async def _profile(self, ctx):
        await ctx.send('!profile command')




    @_profile.command(name='create')
    async def _profile_create(self, ctx, description=None, image_url=None):
        self.user_profile.create_table()

        self.user_profile.create_user_profile(
            id_discord=ctx.author.id,
            description=description or 'Crie a sua descrição utilizando o comando !profile create desc <conteudo>',
            image_url=image_url or 'https://i.pinimg.com/564x/b1/90/a2/b190a2ac5f6912ff2d976f3c753c0331.jpg'
        )
        
        await ctx.channel.send('Perfil criado com sucesso! Utilize **!profile me**')



    @_profile.command(name='me')
    async def _profile_me(self, ctx):
        user_id = ctx.author.id
        description, bg_img = self.user_profile.show_user_profile(user_id)
        embed_profile = discord.Embed(
            color=discord.Colour.blue(),
            description=description
        )
        embed_profile.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed_profile.set_image(url=bg_img)
        await ctx.send(embed=embed_profile)



    @_profile.command(name='desc')
    async def _profile_edit_description(self, ctx, *, new_desc):
        user_id = ctx.author.id
        self.user_profile.edit_description(user_id, new_desc)
        await ctx.channel.send('Descrição atualizada com sucesso!')



    @_profile.command(name='img')
    async def _profile_edit_image(self, ctx, new_img):
        """_summary_

        Args:
            ctx (_type_): _description_
            new_img (_type_): _description_
        """        
        user_id = ctx.author.id

        if not is_valid_image(new_img):
            await ctx.channel.send('Por favor, forneça um link válido para uma imagem JPEG ou PNG.')
            return

        self.user_profile.edit_image(user_id, new_img)
        await ctx.channel.send('Imagem atualizada com sucesso!')




