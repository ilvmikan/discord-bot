import discord
from discord.ext import commands
import random
from outro import utils

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        img_embed = utils.greetings_imgs()
        description_quotes = utils.quotes()
        server_channel = 1222588877194268824

        embed = discord.Embed(
            title=f'Bem-vindo, {member.name}!',
            description=(description_quotes),
            color=discord.Colour.purple(),
        ) 
        embed.set_image(url=img_embed)
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=member.joined_at.strftime("%A %d. %B %Y"))

        channel_set = member.guild.get_channel(server_channel)
        await channel_set.send(embed=embed)

def setup(bot):
    bot.add_cog(Greetings(bot))
