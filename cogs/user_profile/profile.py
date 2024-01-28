from discord.ext import commands
import discord

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='profile', invoke_without_command=True)
    @commands.guild_only()
    async def _info(self, ctx):
        await ctx.send('!info command')

    @_info.command(name='me')
    async def _profile_me(self, ctx):
        await self._profile(ctx, user=ctx.author)

    @_info.command(name='user')
    async def _profile_user(self, ctx, user: discord.User):
        await self._profile(ctx, user=user)

    async def _profile(self, ctx, *, user: discord.User):
        embed = discord.Embed(
            color=discord.Colour.purple(),
            description='!info desc add <content> para adicionar uma breve descrição.',
        )
        embed.set_author(name=user.name, icon_url=user.avatar)

        member = ctx.guild.get_member(user.id)

        if member:
            if any(role.permissions.administrator for role in member.roles):
                highest_role = f'<@&{member.top_role.id}> | __Com poderes de moderação no servidor__'
            else:
                highest_role = f'<@&{member.top_role.id}>' if member.top_role.name != "@everyone" else "Nenhum cargo"

        embed.add_field(name='Cargo mais alto', value=highest_role, inline=True)

        permissions = {
            'banir': member.guild_permissions.ban_members,
            'expulsar': member.guild_permissions.kick_members,
            'silenciar': member.guild_permissions.mute_members,
            'gerenciar cargos': member.guild_permissions.manage_roles,
            'gerenciar canais': member.guild_permissions.manage_channels,
            'mover membros em canal de voz': member.guild_permissions.move_members
        }

        allowed_permissions = [permission for permission, has_permission in permissions.items() if has_permission]

        if allowed_permissions:
            permission_text = ', '.join(allowed_permissions)
            embed.add_field(name='Permissões no servidor', value=permission_text, inline=False)
        else:
            embed.add_field(name='Permissões no servidor', value='Nenhuma permissão', inline=False)

        await ctx.channel.send(embed=embed)
