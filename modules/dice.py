import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing
import random

class dice(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="dice", description="Roll a die!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    ephemeral = "Whether to make the message only visible to you"
  )
  async def dice(self, ctx, maxroll: typing.Optional[int] = 6, ephemeral: typing.Optional[bool] = False):
    await ctx.reply(f"The dice landed on {random.randint(1, maxroll)}!", mention_author=False, ephemeral=ephemeral)

async def setup(bot):
  await bot.add_cog(dice(bot=bot))