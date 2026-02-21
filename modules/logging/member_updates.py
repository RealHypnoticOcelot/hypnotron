import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

class member_updates(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.Cog.listener()
  async def on_member_update(self, before, after):
    member_updates_channel = await after.guild.fetch_channel(
      dotenv_values()['MEMBER_UPDATES_CHANNEL']
    )
    if before.display_name != after.display_name: # Nickname updates
      embed = discord.Embed(
        color=discord.Color.from_str("#0a919e"),
        title=f"{after.name} Nickname Changed",
        description=f"**Before**:\n{before.display_name}\n**After:**\n{after.display_name}"
      ).set_author(name=before.display_name, icon_url=after.display_avatar.url)
      await member_updates_channel.send(embed=embed)
    if before.roles != after.roles: # Role updates
      rolechanged = list(set(before.roles).symmetric_difference(set(after.roles)))[0]
      if rolechanged in before.roles: # if it was removed
        changetype = "removed from"
        embed_hex = "#FF0000"
      else: # if it was added
        changetype = "given"
        embed_hex = "#00FF00"
      embed = discord.Embed(
        color=discord.Color.from_str(embed_hex), 
        title=f"{after.display_name} {changetype} role", 
        description=f"{after.mention} was {changetype} the {rolechanged.mention} role"
      ).set_author(name=before.name, icon_url=before.display_avatar.url)
      await member_updates_channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(member_updates(bot=bot))