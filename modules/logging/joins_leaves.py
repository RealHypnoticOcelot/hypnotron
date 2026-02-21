import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

class joins_leaves(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.Cog.listener()
  async def on_member_join(self, member):
    joins_channel = await before.guild.fetch_channel(
      dotenv_values()['JOINS_LEAVES_CHANNEL']
    )
    embed = discord.Embed(
      color=discord.Color.from_str("#00FF00"), 
      title=f"{member.display_name} Joined", 
      description=f"{member.name} joined the server!").set_author(name=member.name, icon_url=member.display_avatar.url
    )
    await joins_channel.send(embed=embed)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    leaves_channel = await before.guild.fetch_channel(
      dotenv_values()['JOINS_LEAVES_CHANNEL']
    )
    embed = discord.Embed(
      color=discord.Color.from_str("#FF0000"), 
      title=f"{member.display_name} left", 
      description=f"{member.name} left the server").set_author(name=member.name, icon_url=member.display_avatar.url)
    await leaves_channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(joins_leaves(bot=bot))