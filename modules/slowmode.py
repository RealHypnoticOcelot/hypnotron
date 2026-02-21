import discord
from discord import app_commands
from discord.ext import commands, tasks

class slowmode(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="slowmode", description="Set the slowmode of the current channel!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    seconds = "The amount of seconds between messages. Set to 0 to disable."
  )
  @commands.has_permissions(manage_channels=True)
  async def slowmode(self, ctx, seconds: int):
    try:
      await ctx.channel.edit(slowmode_delay=seconds)
      await ctx.reply(content=f"Successfully set {ctx.channel.mention}'s slowmode to {seconds} seconds!", mention_author=False, ephemeral=True)
    except discord.errors.HTTPException:
      await ctx.reply("Failed to set slowmode! Did you set the amount of seconds greater than 21600?", mention_author=False, ephemeral=True)

  @slowmode.error
  async def slowmode_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.reply('Missing permissions!', mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(slowmode(bot=bot))