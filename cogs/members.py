from discord.ext import commands
import discord

class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='info', invoke_without_command=True)
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
            highest_role = member.top_role.name if member.top_role.name != "@everyone" else "Nenhum cargo"
        else:
            highest_role = "Nenhum cargo no servidor"

        embed.add_field(name='Cargo mais alto', value=highest_role, inline=True)

        await ctx.channel.send(embed=embed)
