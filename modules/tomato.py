import discord
from discord import app_commands
from discord.ext import commands, tasks
import random

class tomato(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="tomato", description="BOOOOO!!! 🍅")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def tomato(self, ctx):
    text = ""
    for i in range(0, random.randint(1, 5)):
      text += f" BOO" + ("O" * random.randint(0, 5)) + ("!" * random.randint(2, 6)) + " " + ("🍅" * random.randint (1, 6))
    await ctx.reply(text, mention_author=False)

async def setup(bot):
  await bot.add_cog(tomato(bot=bot))