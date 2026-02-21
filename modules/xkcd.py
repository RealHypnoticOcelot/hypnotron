import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing
import aiohttp

class xkcd(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="xkcd", description="Get the current or a custom XKCD comic!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def REPLACEME(self, ctx, issue: typing.Optional[int] = False):
    async with ctx.typing():
      issue = f"{issue}/" if issue else ""
      async with aiohttp.ClientSession() as session:
        async with session.get(f"https://xkcd.com/{issue}info.0.json") as resp:
          if resp.status == 404:
            return await ctx.reply("Error: Issue not found!", mention_author=False, ephemeral=True)
          elif resp.status != 200:
            return await ctx.reply(f"Error: Response code {resp.status}", mention_author=False, ephemeral=True)
          url = await resp.json()
          embed = discord.Embed(
            color=discord.Color.random(), 
            title=f"XKCD #{url['num']}: {url['safe_title']}",
            description=url['alt']).set_image(url=url['img'])
          await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(xkcd(bot=bot))