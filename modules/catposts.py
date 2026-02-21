import discord
from discord.ext import commands, tasks
import datetime
import aiohttp
import io
from dotenv import dotenv_values

async def get_cat():
  async with aiohttp.ClientSession() as session:
    async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
      if resp.status != 200:
        return None
      url = await resp.json()
      url = url[0]['url']
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp: # Have to fetch the image, in order to upload it to Discord
      if resp.status != 200:
        return None
      else:
        filedata = io.BytesIO(await resp.read())
        filename = "catpost." + resp.content_type[resp.content_type.index("/") + 1:]
        return filedata, filename

class catposts(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access
    self.catpost.start()

  def cog_unload(self):
    self.catpost.cancel()

  @tasks.loop(time=datetime.time(hour=17, minute=00, tzinfo=datetime.timezone.utc)) # utc
  async def catpost(self):
    print("Catpost Activated")
    catposts_channel = self.bot.get_guild(
      dotenv_values()['CATPOSTS_GUILD']
    ).get_channel(
      dotenv_values()['CATPOSTS_CHANNEL']
    )
    catpost = await get_cat()
    catpost_message = await catposts_channel.send("<@&1047920691992870962>", file=discord.File(catpost[0], filename=catpost[1]))
    await catpost_message.add_reaction("🐱")

async def setup(bot):
  await bot.add_cog(catposts(bot=bot))