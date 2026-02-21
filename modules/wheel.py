import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
from utils import mentionstrip

class wheel(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="wheel", description="Spin a wheel between multiple options!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    choices = "Options; Comma separate each choice."
  )
  async def wheel(self, ctx, *, choices: str):
    choices = [choice.replace(",", "").strip() for choice in choices.split(",") if choice.replace(",", "").strip()]
    # Convert to list and remove any blank spaces
    if len(choices) > 1:
      await ctx.reply(await mentionstrip(ctx.guild, random.choice(choices)), mention_author=False)
    else:
      await ctx.reply("Not enough arguments detected! Did you comma separate them?", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(wheel(bot=bot))