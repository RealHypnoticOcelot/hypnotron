import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing
import random

class coinflip(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="coinflip", description="Roll a die!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    ephemeral = "Whether to make the message only visible to you"
  )
  async def coinflip(self, ctx, ephemeral: typing.Optional[bool] = False):
    await ctx.reply(f"The coin landed on {random.choice(['Heads', 'Tails'])}!", mention_author=False, ephemeral=ephemeral)

async def setup(bot):
  await bot.add_cog(coinflip(bot=bot))