from discord.ext import commands
import discord
import re
from time import time

def parse_duration(duration):
    pattern = re.compile(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?')

    match = pattern.match(duration)
    if not match:
        raise ValueError('Formato de duração inválido')

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='mod')
    async def _mod(self, ctx):
        await ctx.channel.send('!mod <command>')

    @_mod.command(name='kick')
    async def _kick(self, ctx, user: discord.Member, *, reason=None):
        if ctx.guild.me.guild_permissions.kick_members and ctx.author.guild_permissions.kick_members:
            try:
                await user.kick(reason=reason)
                await ctx.send(f'{user} foi expulso, razão: {reason}')
            except discord.Forbidden:
                await ctx.send(f'Sem permissão para expulsar {user}')
        else:
            await ctx.send(f'Sem permissão para expulsar membros')

    @_mod.command(name='ban')
    async def _ban(ctx, user: discord.Member, *, reason=None):
        if ctx.guild.me.guild_permissions.ban_members and ctx.author.guild_permissions.ban_members:
            try:
                await user.ban(reason=reason)
                await ctx.send(f'{user} foi banido, razão: {reason}')
            except discord.Forbidden:
                await ctx.send(f'Sem permissão para expulsar {user}')
        else:
            await ctx.send(f'Sem permissão para banir membros')

    @_mod.command(name='unban')
    async def _unban(ctx, user_id: int, reason=None):
        if ctx.author.guild_permissions.ban_members and ctx.guild.me.guild_permissions.ban_members:
            try:
                await ctx.guild.unban(discord.Object(id=user_id), reason=reason)
                await ctx.send(f'Usuário com ID {user_id} foi desbanido, razão: {reason}')
            except discord.Forbidden:
                await ctx.send(f'Sem permissão para desbanir usuário com ID {user_id}')
        else:
            await ctx.send('Sem permissão para desbanir.')

    @_mod.command(name='mute')
    async def mute(ctx, member: discord.Member, duration=None, *, reason=None):
        if ctx.author.guild_permissions.mute_members:
            muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

            if not muted_role:
                muted_role = await ctx.guild.create_role(name='Muted')

                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=False)

            await member.add_roles(muted_role, reason=reason)

            if duration:
                time.sleep(parse_duration(duration))
                await member.remove_roles(muted_role, reason="Tempo de mute expirado")

            await ctx.send(f'{member.mention} foi mutado.')

        else:
            await ctx.send('Você não tem permissão para mutar membros.')
    
    @_mod.command(name='unmute', hidden=True)
    async def _unmute(ctx, user: discord.Member):
        """
        Desmuta um usuário específico

        args:
            ctx: O contexto da mensagem que acionou o comando.
            user: um objeto do usuário que foi mencionado para ser silenciado
        """
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if muted_role in user.roles:
            for channel in ctx.guild.channels:
                await channel.set_permissions(user, speak=True, send_messages=True)

            await user.remove_roles(muted_role)
            await ctx.send(f'{user.mention} foi desmutado.')
        else:
            await ctx.send(f'{user.mention} não possui o cargo "Muted".')

    @_mod.command(name='clear', hidden=True)
    async def _clear(ctx, quantity: int):
        """
        Exclui as mensagens de um canal onde o comando "!mod clear <quantidade>" foi chamado
        
        args:
            ctx (discord.ext.commands.Context): O contexto da mensagem que acionou o comando.
            quantity: quantidade de mensagens para serem excluídas.
        """
        msg = []
        async for message in ctx.channel.history(limit=quantity + 1):
            msg.append(message)
    
        await ctx.channel.delete_messages(msg)
        await ctx.send(f'{quantity} mensagens foram excluídas')
        print(f'As mensagens do canal "{ctx.channel.name}" (ID: {ctx.channel.id}) do servidor "{ctx.guild.name}" (ID: {ctx.guild.id}) foram excluídas')
    