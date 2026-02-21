import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing

class echo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="echo", description="Send a message to another channel through the bot!")
  @app_commands.allowed_installs(guilds=True, users=False)
  @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
  @app_commands.describe(
    msg = "Message to send"
  )
  @app_commands.rename(msg="message")
  async def echo(
    self, 
    ctx, 
    channel: typing.Optional[discord.TextChannel] = None,
    *, msg: str,
    attachment: typing.Optional[discord.Attachment] = None
  ):
    if channel == None:
      channel = ctx.channel
    # I was hoping to implement this as a check, but I don't know that you can
    # pass an argument to a check
    if channel.permissions_for(ctx.message.author).manage_messages:
      if attachment != None:
        attachment = await attachment.to_file()
      try:
        await channel.send(msg, file=attachment)
      except discord.Forbidden:
        await ctx.reply(f"I don't have permissions to send messages in {channel.mention}!", mention_author=False, ephemeral=True)
      await ctx.reply(content=f"Sent message to {channel.mention}!", mention_author=False, ephemeral=True)
    else:
      await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(echo(bot=bot))