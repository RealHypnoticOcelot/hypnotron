import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing

class lockdown(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="lockdown", description="Lockdown a channel! If a channel isn't specified, will lock every channel")
  @app_commands.allowed_installs(guilds=True, users=False)
  @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False) # Guilds, DMs, DMs/Group DMs
  @commands.has_guild_permissions(manage_channels=True)
  @commands.bot_has_guild_permissions(manage_channels=True)
  async def lockdown(self, ctx, channel: typing.Optional[discord.abc.GuildChannel]):
    lock_embed = discord.Embed(
      color = discord.Color.from_rgb(255, 0, 0),
      title = "🔒 Channel Locked!",
      description = "`All channels have been locked!`" if channel == None else "`This channel has been locked!`"
    ).set_thumbnail(url=ctx.bot.user.display_avatar.url)

    await ctx.reply(content="Lockdown initiated!", mention_author=False, ephemeral=True)
    if channel == None:
      for channel in ctx.guild.text_channels:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(embed=lock_embed)
      for channel in ctx.guild.voice_channels:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(embed=lock_embed)
    else:
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      if channel.type is discord.ChannelType.voice:
        overwrite.connect = False
      else:
        overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await channel.send(embed=lock_embed)

  @commands.hybrid_command(name="unlockdown", description="Unlockdown a channel! If a channel isn't specified, will lock every channel")
  @app_commands.allowed_installs(guilds=True, users=False)
  @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False) # Guilds, DMs, DMs/Group DMs
  @commands.has_guild_permissions(manage_messages=True)
  @commands.bot_has_guild_permissions(manage_messages=True)
  async def unlockdown(self, ctx, channel: typing.Optional[discord.abc.GuildChannel]):
    lock_embed = discord.Embed(
      color = discord.Color.from_rgb(0, 255, 0),
      title = "🔒 Channel Locked!",
      description = "`All channels have been unlocked!`" if channel == None else "`This channel has been unlocked!`"
    ).set_thumbnail(url=ctx.bot.user.display_avatar.url)

    await ctx.reply(content="Unlockdown initiated!", mention_author=False, ephemeral=True)
    if channel == None:
      for channel in ctx.guild.text_channels:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(embed=lock_embed)
      for channel in ctx.guild.voice_channels:
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await channel.send(embed=lock_embed)
    else:
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      if channel.type is discord.ChannelType.voice:
        overwrite.connect = None
      else:
        overwrite.send_messages = None
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
      await channel.send(embed=lock_embed)

  @lockdown.error
  async def slowmode_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.reply('Missing permissions!', mention_author=False, ephemeral=True)

  @unlockdown.error
  async def slowmode_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.reply('Missing permissions!', mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(lockdown(bot=bot))