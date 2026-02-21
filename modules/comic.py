import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import comics
import pytz
import typing

async def comic_autocomplete(interaction: discord.Interaction, current: str,) -> list[app_commands.Choice[str]]:
	try:
		comics_list = comics.directory.search(current)
		comics_list = [
      app_commands.Choice(name=comic, value=comic)
      for comic in comics_list if current.lower() in comic.lower()
		]
		return comics_list[0 : 25]
	except InvalidEndpointError:
		return []

class customDate(commands.Converter):
  async def convert(self, ctx, argument):
    try:
      argument = datetime.datetime.strptime(argument, '%Y-%m-%d')
      return True, argument
    except:
      return False, argument

class comic(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="comic", description="Get a comic from GoComics!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    date="YYYY-MM-DD, or \"latest\" for the latest comic"
  )
  @app_commands.autocomplete(comic=comic_autocomplete)
  async def comic(self, ctx, comic: str, date: typing.Optional[customDate] = None):
    try:
      if date == None: # If no date was provided
        comic = comics.search(comic, date="random")
      elif date[0]: # If the date provided was valid
        try:
          comic = comics.search(comic, date=date[1])
        except comics.exceptions.InvalidDateError:
          await ctx.reply("No comic available on that date!", mention_author=False, ephemeral=True)
      else: # If the date provided was invalid
        if date[1].lower() == "latest":
          try:
            comic = comics.search(
              comic,
              date=(
                datetime.datetime.now(pytz.timezone('America/Chicago')).strftime('%Y-%m-%d')
              )
            )
            # Uses Chicago timezone, I'm pretty sure, since the company is based in Missouri
          except comics.exceptions.InvalidDateError:
            await ctx.reply("No comic available on that date!", mention_author=False, ephemeral=True)
        else:
          await ctx.reply("Invalid Date!", mention_author=False, ephemeral=True)
      embed = discord.Embed(
        color=discord.Color.random(),
        title=comic.title,
        url=comic.url,
        description=comic.date).set_image(url=comic.image_url)
      await ctx.reply(embed=embed, mention_author=False)
    except comics.exceptions.InvalidEndpointError:
      await ctx.reply("Invalid Comic!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(comic(bot=bot))