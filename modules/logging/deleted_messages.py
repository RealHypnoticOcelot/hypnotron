import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import dotenv_values

class deleted_messages(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access 

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    deletes_channel = await message.guild.fetch_channel(
      dotenv_values()['DELETED_MESSAGES_CHANNEL']
    )
    files = []
    if message.attachments != []:
      for i in message.attachments:
        files.append(i)
    if message.stickers != []:
      for i in message.stickers:
        if isinstance(await i.fetch(), discord.GuildSticker): # can't reupload discord's lottie format stickers
          files.append(i)
    logattachments = [await i.to_file() for i in files]
    embed = discord.Embed(
      color=discord.Color.from_str("#FF0000"), 
      title=f"Message deleted by {message.author.display_name} in {message.channel.mention}", 
      description=message.content).set_footer(
        text=f"User ID: {message.author.id} | Message ID: {message.id}{' | Attached Files Above' if files != [] else ''}"
      ).set_author(
        name=message.author.name,
        icon_url=message.author.display_avatar.url
      )
    await deletes_channel.send(embed=embed, files=logattachments)

async def setup(bot):
  await bot.add_cog(deleted_messages(bot=bot))