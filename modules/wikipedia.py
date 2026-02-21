import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing
import aiohttp

class wikipedia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="wikipedia", description="Search Wikipedia!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def wikipedia(self, ctx, *, search: typing.Optional[str]):
    if search != None:
      search = search.replace(" ", "_")
      search = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search}"
    else:
      search = "https://en.wikipedia.org/api/rest_v1/page/random/summary/"
    application = ctx.bot.application
    headers = {"User-Agent": "None"} # Replace this with your email!
    async with aiohttp.ClientSession() as session:
      async with session.get(search, headers=headers) as resp:
        if resp.status == 404:
          return await ctx.reply('Invalid Search!(Hint: The search string is case sensitive)', mention_author=False, ephemeral=True)
        elif resp.status == 403:
          return await ctx.reply(f'This bot has an invalid user-agent! Contact `{application.owner.name}` and have them fix it.', mention_author=False, ephemeral=True)
        elif resp.status != 200:
          return await ctx.reply(f"Error: Response code {resp.status}", mention_author=False, ephemeral=True)
        url = await resp.json()
        article_title = url['title']
        article_description = url['extract']
        embed = discord.Embed(
          color=discord.Color.random(), 
          title=article_title, 
          description=article_description, 
          url=url['content_urls']['desktop']['page'])
        try:
          embed = embed.set_thumbnail(url=url['thumbnail']['source'])
        except:
          pass
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(wikipedia(bot=bot))