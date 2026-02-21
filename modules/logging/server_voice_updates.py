import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

class server_voice_updates(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.Cog.listener()
  async def on_audit_log_entry_create(self, entry):
    server_voice_updates_channel = await entry.guild.fetch_channel(
      dotenv_values()['SERVER_VOICE_UPDATES_CHANNEL']
    )
    if entry.action == discord.AuditLogAction.member_update:
      if hasattr(entry.after, 'mute'): # Server Mute
        if entry.after.mute == True:
          change = "Muted"
          embed_hex = "#FF0000"
        else:
          change = "Unmuted"
          embed_hex = "#00FF00"
        embed = discord.Embed(
          color=discord.Color.from_str(embed_hex), 
          title=f"{entry.target.display_name} Server {change}", 
          description=f"{entry.target.mention} was server {change.lower()} by {entry.user.mention}"
        ).set_author(name=entry.target.name, icon_url=entry.target.display_avatar.url)
        await server_voice_updates_channel.send(embed=embed)
      elif hasattr(entry.after, 'deaf'): # Server Deafen
        if entry.after.deaf == True:
          change = "Deafened"
          embed_hex = "#FF0000"
        else:
          change = "Undeafened"
          embed_hex = "#00FF00"
        embed = discord.Embed(
          color=discord.Color.from_str(embed_hex), 
          title=f"{entry.target.display_name} Server {change}", 
          description=f"{entry.target.mention} was server {change.lower()} by {entry.user.mention}"
        ).set_author(name=entry.target.name, icon_url=entry.target.display_avatar.url)
        await server_voice_updates_channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(server_voice_updates(bot=bot))