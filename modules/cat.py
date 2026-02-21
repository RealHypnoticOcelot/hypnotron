import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import aiohttp

class cat(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="cat", description="Get a random cat picture!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def cat(self, ctx):
    async with ctx.typing():
      async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
          if resp.status != 200:
            return await ctx.reply(f'Error: Response code {resp.status}')
          resp = await resp.json()
          embed = discord.Embed(
            color=discord.Color.random(),
            title="Here's your cat image!"
          ).set_footer(text="From https://thecatapi.com").set_image(url=resp[0]['url'])
          await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(cat(bot=bot))