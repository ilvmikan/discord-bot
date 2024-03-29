import discord
from discord import Embed as DiscordEmbed
from discord.ext import commands

class Embed:
    def __init__(self, title="Configurações do servidor", description=None, color=0x00ff00, image=None):
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
    

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.get_welcome_channel(guild)
        if channel is not None:
            await self._config(channel)

    @commands.Cog.listener()
    async def on_message(self, msg):
        """
            my_name = 'your bot name'
        """
        my_name = 'nyxn'
        if my_name in msg.content.lower():
            await msg.add_reaction('♥')


    def get_welcome_channel(self, guild):
        return (
            guild.system_channel
            or discord.utils.get(guild.channels, name='boas-vindas') 
            or discord.utils.get(guild.channels, type=discord.ChannelType.text) 
        )

    @commands.group(name='config', invoke_without_command=True)
    async def _config(self, channel):
        embed = Embed(
            description='Deixe seu servidor automatizado com cargos, canal de logs e outros'
        )
        embed.add_field(name='Canal de boas vindas', value='!config welcome_channel <channel_id>')
        embed.add_field(name='Cargos para novos membros', value='!config autorole <role_id>')
        embed.add_field(name='Canal de logs', value='!config log_channel <channel_id>')
        await channel.send(embed=embed.build())

    @_config.command(name='welcome_channel')
    async def _welcome_channel(self, ctx, welcome_channel):
        # criar lógica
        await ctx.channel.send(f'O canal de boas vindas foi alterado para {welcome_channel}')

    @_config.command(name='autorole')
    async def _autorole(self, ctx, role_id):
        # criar lógica 
        await ctx.channel.send(f'O cargo padrão foi alterado para {role_id}')

    @_config.command(name='log_channel')
    async def _log_channel(self, ctx, channel_id):
        # criar lógica 
        await ctx.channel.send(f'O canal de logs foi alterado para {channel_id}')

def setup(bot):
    bot.add_cog(Config(bot))
