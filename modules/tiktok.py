import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp
import re

class tiktok(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="tiktok", description="Embed a TikTok!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def tiktok(self, ctx, url: str):
    async with ctx.typing():
      async with aiohttp.ClientSession() as session:
        try:
          async with session.get(url) as resp:
            url = str(resp.url.with_query(None))
            await ctx.reply(re.sub(r'(w{3}).?tiktok', "d.tiktokez", url), mention_author=False)
        except aiohttp.InvalidURL:
          await ctx.reply("Invalid URL!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(tiktok(bot=bot))