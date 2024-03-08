from discord.ext import commands
import discord
import re
from time import time

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='mod', invoke_without_command=True)
    async def _mod(self, ctx):
        await ctx.channel.send('!mod <command>')

    @commands.has_guild_permissions(kick_members=True)
    @_mod.command(name='kick')
    async def _kick(self, ctx, user: discord.Member, *, reason=None):
        await self.perform_action(ctx, 'kick', user, reason)

    @commands.has_guild_permissions(ban_members=True)
    @_mod.command(name='ban')
    async def _ban(self, ctx, user: discord.Member, *, reason=None):
        await self.perform_action(ctx, 'ban', user, reason)

    @commands.has_guild_permissions(ban_members=True)
    @_mod.command(name='unban')
    async def _unban(self, ctx, user_id: int, reason=None):
        user = discord.Object(id=user_id)
        await self.perform_action(ctx, 'unban', user, reason)

    async def handle_mute(self, ctx, member, duration, reason):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if not muted_role:
            muted_role = await ctx.guild.create_role(name='Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f'{member.mention} foi mutado.')

    @commands.has_guild_permissions(mute_members=True)
    @_mod.command(name='mute')
    async def mute(self, ctx, member: discord.Member, duration=None, *, reason=None):    
        await self.handle_mute(ctx, member, duration, reason)

    @commands.has_guild_permissions(mute_members=True)
    @_mod.command(name='unmute')
    async def _unmute(self, ctx, user: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if muted_role in user.roles:
            for channel in ctx.guild.channels:
                await channel.set_permissions(user, speak=True, send_messages=True)

            await user.remove_roles(muted_role)
            await ctx.send(f'{user.mention} foi desmutado.')

    @commands.has_guild_permissions(manage_messages=True)
    @_mod.command(name='clear')
    async def _clear(self, ctx, quantity: int):
        messages = await ctx.channel.purge(limit=quantity + 1)
        await ctx.send(f'{len(messages) - 1} mensagens foram excluídas')
        print(f'As mensagens do canal "{ctx.channel.name}" (ID: {ctx.channel.id}) do servidor "{ctx.guild.name}" (ID: {ctx.guild.id}) foram excluídas')


    async def perform_action(self, ctx, action, user, reason='Tenho permissão, então eu posso.'):
        try:
            method = getattr(ctx.guild, action)
            action_name = {'kick': 'expulso', 
                      'ban': 'banido', 
                      'unban': 'desbanido'}
            
            action_name_2 = {'kick': 'expulsar', 
                      'ban': 'banir', 
                      'unban': 'desbanir'}
            
            await method(user, reason=reason)
            await ctx.send(f'{user} foi {action_name[action]}, razão: {reason}')
        except discord.Forbidden:
            await ctx.send(f'Sem permissão para {action_name_2[action]} {user}')


def setup(bot):
    bot.add_cog(Admin(bot))