import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import aiohttp

class inspire(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="inspire", description="Inspirational!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def inspire(self, ctx):
    async with ctx.typing():
      url = "https://inspirobot.me/api?generate=true"
      if datetime.datetime.now(tz=datetime.timezone.utc).month == 12:
        url += "&season=xmas"
        # christmas code!! so jolly
      async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
          if resp.status != 200:
            return await ctx.reply('Error!') # Returning prevents the rest of the command from running
          await ctx.reply(await resp.text(), mention_author=False)
          # API returns a URL leading to the generated image, so we just send the URL instead of downloading it ourselves.

async def setup(bot):
  await bot.add_cog(inspire(bot=bot))