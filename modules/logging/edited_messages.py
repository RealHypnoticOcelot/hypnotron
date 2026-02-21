import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values
import difflib

class edited_messages(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access 

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    edits_channel = await before.guild.fetch_channel(
      dotenv_values()['EDITED_MESSAGES_CHANNEL']
    )
    embed_color = discord.Color.from_str("#0a919e")
    if before.author != self.bot.user and before.content != after.content: # Embedded gifs count as edits
      embeds = [
        discord.Embed(
          color=embed_color, 
          title=f"Message edited by {before.author.display_name} in {before.channel.mention}", 
          url=after.jump_url
        ).set_footer(
          text=f"User ID: {before.author.id} | Message ID: {after.id}"
        ).set_author(
          name=before.author.name,
          icon_url=before.author.display_avatar.url
        )
      ]
      if len(before.content) + len(after.content) > 4000:
        embeds.append(discord.Embed(
          color=embed_color,
          title="Before:",
          description=before.content
        ).set_footer(
          text=f"User ID: {before.author.id} | Message ID: {after.id}"
        ).set_author(
          name=before.author.name,
          icon_url=before.author.display_avatar.url
        ))
        embeds.append(discord.Embed(
          color=embed_color,
          title="After:",
          description=after.content
        ).set_footer(
          text=f"User ID: {before.author.id} | Message ID: {after.id}"
        ).set_author(
          name=before.author.name,
          icon_url=before.author.display_avatar.url
        ))
      else:
        embeds[0].description = f"**Before**:\n{before.content}\n**After:**\n{after.content}"
      for embed in embeds:
        await edits_channel.send(embed=embed)

async def setup(bot):
  await bot.add_cog(edited_messages(bot=bot))