import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

class moderation_actions(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.Cog.listener()
  async def on_audit_log_entry_create(self, entry): # There are events for bans/unbans, but they don't include who banned them
    moderation_actions_channel = await entry.guild.fetch_channel(
      dotenv_values()['MODERATION_ACTIONS_CHANNEL']
    )
    if entry.action == discord.AuditLogAction.kick: # Kicks
      target_user = await self.bot.fetch_user(entry.target.id)
      embed = discord.Embed(
        color=discord.Color.from_str("#FF0000"), 
        title=f"{target_user.display_name} was kicked", 
        description=f"{target_user.name} was kicked by {entry.user.mention}{f'\n**Reason:** {entry.reason}' if entry.reason else ''}"
      ).set_author(
        name=target_user.name,
        icon_url=target_user.display_avatar.url
      ).set_footer(text=f"User ID: {target_user.id}")
      await moderation_actions_channel.send(embed=embed)
    elif entry.action == discord.AuditLogAction.member_update:
      if hasattr(entry.after, 'timed_out_until'): # Timeouts
        if entry.after.timed_out_until == None: # if timeout was removed, won't log natural untimeouts because it doesn't get set to None that way
          change = "Un-Timed Out"
          embed_hex = "#00FF00"
          until = ""
        else:
          change = "Timed Out"
          embed_hex = "#FF0000"
          unixtimestamp = int(entry.after.timed_out_until.timestamp())
          until = f"until <t:{unixtimestamp}:f>(<t:{unixtimestamp}:R>)" # convert to discord unix timestamp in relative time
        embed = discord.Embed(
          color=discord.Color.from_str(embed_hex), 
          title=f"{entry.target.display_name} {change}", 
          description=f"{entry.target.mention} was {change.lower()} by {entry.user.mention} {until}{f'\n**Reason:** {entry.reason}' if entry.reason else ''}"
        ).set_author(name=entry.target.name, icon_url=entry.target.display_avatar.url)
        await moderation_actions_channel.send(embed=embed)
    elif entry.action == discord.AuditLogAction.ban: # Bans
      target_user = await self.bot.fetch_user(entry.target.id)
      embed = discord.Embed(
        color=discord.Color.from_str("#FF0000"), 
        title=f"{target_user.display_name} Banned", 
        description=f"{target_user.name} was banned by {entry.user.mention}{f'\n**Reason:** {entry.reason}' if entry.reason else ''}"
      ).set_author(
        name=target_user.name,
        icon_url=target_user.display_avatar.url
      ).set_footer(text=f"User ID: {target_user.id}")
      await moderation_actions_channel.send(embed=embed)
    elif entry.action == discord.AuditLogAction.unban: # Unbans
      target_user = await self.bot.fetch_user(entry.target.id)
      embed = discord.Embed(
        color=discord.Color.from_str("#00FF00"), 
        title=f"{target_user.display_name} Unbanned", 
        description=f"{target_user.name} was unbanned by {entry.user.mention}{f'\n**Reason:** {entry.reason}' if entry.reason else ''}"
      ).set_author(
        name=target_user.name,
        icon_url=target_user.display_avatar.url
      ).set_footer(text=f"User ID: {target_user.id}")
      await moderation_actions_channel.send(embed=embed)
async def setup(bot):
  await bot.add_cog(moderation_actions(bot=bot))