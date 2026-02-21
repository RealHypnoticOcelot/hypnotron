import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

class voice_updates(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access 

  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    voice_channel = await member.guild.fetch_channel(
      dotenv_values()['VOICE_UPDATES_CHANNEL']
    )
    if before.channel == None and after.channel != None: # Joins
      changetype = "Joined"
      changename = after.channel.mention
      embed_hex = "#00FF00"    
    elif before.channel != None and after.channel == None: # Leaves
      changetype = "Left"
      changename = before.channel.mention
      embed_hex = "#FF0000"
    elif (before.channel != None and after.channel != None) and before.channel != after.channel: # sometimes it just shows the same channel i guess
      changetype = "Switched"
      changename = f"from {before.channel.mention} to {after.channel.mention}"
      embed_hex = "#0a919e"
    else:
      changetype = None
    if changetype != None:
      embed = discord.Embed(
        color=discord.Color.from_str(embed_hex), 
        title=f"{member.display_name} {changetype} Voice Channel", 
        description=f"{member.mention} {changetype.lower()} {changename}"
      ).set_author(name=member.name, icon_url=member.display_avatar.url)
      await voice_channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(voice_updates(bot=bot))