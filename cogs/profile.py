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
    async def _profile_create(self, ctx, *, description=None, image_url=None):
        self.user_profile.create_table()

        self.user_profile.create_user_profile(
            id_discord=ctx.author.id,
            description=description or 'Edite sua descrição utilizando o comando !profile desc **conteúdo**\nEdite a sua imagem utilizando !profile img **link**\nEdite a cor utilizando !profile color 255, 255, 255>',
            image_url=image_url or 'https://i.pinimg.com/564x/b1/90/a2/b190a2ac5f6912ff2d976f3c753c0331.jpg'
        )
        
        await ctx.channel.send('Perfil criado com sucesso! Utilize **!profile me**')


    @_profile.command(name='me')
    async def _profile_me(self, ctx):
        user_id = ctx.author.id
        description, bg_img, color = self.user_profile.show_user_profile(user_id)

        embed_profile = discord.Embed(
            color = discord.Colour.from_rgb(color[0] or 0, color[1] or 0, color[2] or 255),
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
        user_id = ctx.author.id

        if not is_valid_image(new_img):
            await ctx.channel.send('Por favor, forneça um link válido para uma imagem JPEG ou PNG.')
            return

        self.user_profile.edit_image(user_id, new_img)
        await ctx.channel.send('Imagem atualizada com sucesso!')


    @_profile.command(name='color')
    async def _profile_edit_color(self, ctx, r: int, g: int, b: int):
        user_id = ctx.author.id

        if not (0 <= r <= 255) or not (0 <= g <= 255) or not (0 <= b <= 255):
            await ctx.channel.send('Por favor, forneça valores RGB válidos (0-255) para as cores.')
            return

        self.user_profile.edit_color(user_id, r, g, b)
        await ctx.channel.send('Cor do perfil atualizada com sucesso!')


    @_profile.command(name='config')
    async def _profile_config(self, ctx):
        user_id = ctx.author.id
        id_discord, description, bg_img, color_r, color_g, color_b = self.user_profile.profile_config(user_id)

        embed = discord.Embed(
            title=f"Configurações do Perfil - {ctx.author.name}",
            color=discord.Colour.from_rgb(color_r, color_g, color_b)
        )
        embed.add_field(name="Descrição", value=f"_!profile desc <conteúdo>_\n{description}", inline=False)
        embed.add_field(name="Imagem de Fundo", value=f"_!profile img <img_link>_\n{bg_img}", inline=False)
        embed.add_field(name="Cor (RGB)", value=f"({color_r}, {color_g}, {color_b})", inline=False)

        await ctx.send(embed=embed)


    @_profile.command(name='deleteall')
    async def delete_all(self, ctx):
        if ctx.author.id == 1053121282767593492:
            delete = self.user_profile.delete_table_content()
            await ctx.channel.send(delete)




