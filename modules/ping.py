import discord
from discord import app_commands
from discord.ext import commands, tasks

class ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="ping", description="Get the bot's ping!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def ping(self, ctx):
    await ctx.reply(f"My ping is {round(bot.latency * 1000)}ms.", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(ping(bot=bot))