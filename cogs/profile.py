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
        await self._profile_page(ctx, user=ctx.author)

    @_info.command(name='user')
    async def _profile_user(self, ctx, user: discord.User):
        await self._profile_page(ctx, user=user)

    async def _profile_page(self, ctx, *, user: discord.User):
        embed_first_page = discord.Embed(
            color=discord.Colour.blue(),
            description='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem q',
        )
        embed_first_page.set_author(name=user.name, icon_url=user.avatar)
        embed_first_page.set_image(url='https://i.pinimg.com/564x/af/69/92/af69921bd04546c232d0a0aa3ba437c5.jpg')

        embed_second_page = discord.Embed(
            color=discord.Colour.red(),
            description='Segunda página de informações.',
        )
        embed_second_page.set_author(name=user.name, icon_url=user.avatar)

        # se tudo der errado, deixe somente esse embed e adicione "await ctx.channel.send(embed=embed) (altere o nome para embed)"
        embed_third_page = discord.Embed(
            color=discord.Colour.purple(),
        )
        embed_third_page.set_author(name=user.name, icon_url=user.avatar)

        member = ctx.guild.get_member(user.id)

        if member:
            if any(role.permissions.administrator for role in member.roles):
                highest_role = f'<@&{member.top_role.id}> | __Com poderes de moderação no servidor__'
            else:
                highest_role = f'<@&{member.top_role.id}>' if member.top_role.name != "@everyone" else "Nenhum cargo"

            embed_third_page.add_field(name='Cargo mais alto', value=highest_role, inline=True)

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
                embed_third_page.add_field(name='Permissões no servidor', value=permission_text, inline=False)
            else:
                embed_third_page.add_field(name='Permissões no servidor', value='Nenhuma permissão', inline=False)
                

        pages = [embed_first_page, embed_second_page, embed_third_page]
        current_page = 0
        message = await ctx.send(embed=pages[current_page])
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if str(reaction.emoji) == '➡️' and current_page < len(pages) - 1:
                    current_page += 1
                elif str(reaction.emoji) == '⬅️' and current_page > 0:
                    current_page -= 1

                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction, user)

            except Exception as e:
                print(e)
                break