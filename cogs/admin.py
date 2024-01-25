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

    async def check_permissions(self, ctx, action):
        required_permissions = discord.Permissions()
        required_permissions.update(**{action: True})

        if not ctx.guild.me.guild_permissions >= required_permissions or not ctx.author.guild_permissions >= required_permissions:
            await ctx.send(f'Você não tem permissão para usar esse comando')
            return False
        return True

    async def perform_action(self, ctx, action, user, reason=None):
        try:
            method = getattr(ctx.guild, action)
            await method(user, reason=reason)
            await ctx.send(f'{user} foi {action}, razão: {reason}')
        except discord.Forbidden:
            await ctx.send(f'Sem permissão para {action} {user}')

    @commands.group(name='mod', invoke_without_command=True)
    async def _mod(self, ctx):
        await ctx.channel.send('!mod <command>')

    @_mod.command(name='kick')
    async def _kick(self, ctx, user: discord.Member, *, reason=None):
        if await self.check_permissions(ctx, 'kick_members'):
            await self.perform_action(ctx, 'kick', user, reason)

    @_mod.command(name='ban')
    async def _ban(self, ctx, user: discord.Member, *, reason=None):
        if await self.check_permissions(ctx, 'ban_members'):
            await self.perform_action(ctx, 'ban', user, reason)

    @_mod.command(name='unban')
    async def _unban(self, ctx, user_id: int, reason=None):
        if await self.check_permissions(ctx, 'ban_members'):
            user = discord.Object(id=user_id)
            await self.perform_action(ctx, 'unban', user, reason)

    @_mod.command(name='mute')
    async def mute(self, ctx, member: discord.Member, duration=None, *, reason=None):
        if await self.check_permissions(ctx, 'mute_members'):
            await self.handle_mute(ctx, member, duration, reason)

    async def handle_mute(self, ctx, member, duration, reason):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if not muted_role:
            muted_role = await ctx.guild.create_role(name='Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role, reason=reason)

        if duration:
            await discord.utils.sleep(parse_duration(duration))
            await member.remove_roles(muted_role, reason="Tempo de mute expirado")

        await ctx.send(f'{member.mention} foi mutado.')

    @_mod.command(name='unmute', hidden=True)
    async def _unmute(self, ctx, user: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if muted_role in user.roles:
            for channel in ctx.guild.channels:
                await channel.set_permissions(user, speak=True, send_messages=True)

            await user.remove_roles(muted_role)
            await ctx.send(f'{user.mention} foi desmutado.')
        else:
            await ctx.send(f'{user.mention} não possui o cargo "Muted".')

    @commands.has_guild_permissions(manage_messages=True)
    @_mod.command(name='clear', hidden=True)
    async def _clear(self, ctx, quantity: int):
        messages = await ctx.channel.purge(limit=quantity + 1)
        await ctx.send(f'{len(messages) - 1} mensagens foram excluídas')
        print(f'As mensagens do canal "{ctx.channel.name}" (ID: {ctx.channel.id}) do servidor "{ctx.guild.name}" (ID: {ctx.guild.id}) foram excluídas')
