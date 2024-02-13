import discord
from discord.ext import commands

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
        embed = discord.Embed(
            title='Configurações do servidor',
            description='Deixe seu servidor automatizado com cargos, canal de logs e outros'
        )
        embed.add_field(name='Canal de boas vindas', value='!config welcome_channel <channel_id>')
        embed.add_field(name='Cargos para novos membros', value='!config autorole <role_id>')
        embed.add_field(name='Canal de logs', value='!config log_channel <channel_id>')
        await channel.send(embed=embed)

    @_config.command(name='welcome_channel')
    async def _welcome_channel(self, ctx, welcome_channel):
        # criar lógica com um banco de dados
        await ctx.channel.send(f'O canal de boas vindas foi alterado para {welcome_channel}')

    @_config.command(name='autorole')
    async def _autorole(self, ctx, role_id):
        # criar lógica com um banco de dados
        await ctx.channel.send(f'O cargo padrão foi alterado para {role_id}')

    @_config.command(name='log_channel')
    async def _log_channel(self, ctx, channel_id):
        # criar lógica com um banco de dados
        await ctx.channel.send(f'O canal de logs foi alterado para {channel_id}')

def setup(bot):
    bot.add_cog(Config(bot))