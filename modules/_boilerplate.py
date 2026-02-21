import discord
from discord import app_commands
from discord.ext import commands, tasks

class REPLACEMECLASS(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="REPLACEMENAME", description="REPLACEME")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    REPLACEME = "REPLACE ME"
  )
  @app_commands.rename(REPLACEME="REPLACE_ME")
  async def REPLACEME(self, ctx, REPLACEME: str):
    pass

async def setup(bot):
  await bot.add_cog(REPLACEMECLASS(bot=bot))