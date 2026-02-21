import discord
from discord import app_commands
from discord.ext import commands
import io
from pathlib import Path
import pickle
import random
import typing
from PIL import Image
import math
import asyncio

country_dir = Path.cwd() / "countries"
country_info = pickle.load(open(country_dir / "country_info.pkl", "rb"))

async def getsilhouette(hard):
  silhouette = random.choice(country_info)
  with open(silhouette['path'], 'rb') as fp:
    fp = Image.open(fp)
    if hard == True:
      fp = fp.rotate(random.randint(1,360), resample=Image.Resampling.BICUBIC, expand=True)
    bg = Image.new(mode="RGBA", size=(500, 500))
    
    old_width, old_height = fp.size
    x1 = int(math.floor((bg.size[0] - old_width) / 2))
    y1 = int(math.floor((bg.size[1] - old_height) / 2))
    bg.paste(fp, (x1, y1, x1 + old_width, y1 + old_height))

    output_buffer = io.BytesIO()
    bg.save(output_buffer, "png")  # or whatever format
    output_buffer.seek(0)
    silhouette['image'] = output_buffer
  return (silhouette)

class guessplace(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.hybrid_command(name="guessplace", description="Guess the name of a country!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  @app_commands.describe(
    guesstype="Choose your guess!",
    hardmode="Whether to rotate regions in Silhouette mode"
  )
  async def guessplace(
    self,
    ctx,
    guesstype: typing.Literal["flag", "silhouette"],
    hardmode: typing.Optional[bool] = False
  ):
    if guesstype == "flag":
      country = random.choice(country_info)
      async with ctx.typing():
        await ctx.reply(
          f"What region is this? {country['flag']}",
          mention_author=False
        )
        def check(answer):
          return answer.content.lower() in [name.lower() for name in country['names']] and answer.channel == ctx.channel
        try:
          msg = await self.bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
          await ctx.channel.send(f"Nobody got it... the answer was {country['names'][0]}!\n-# Valid answers: {', '.join(country['names'])}")
        else:
          await msg.reply(f"{msg.author.mention} got it!")
    elif guesstype == "silhouette":
      country = await getsilhouette(hardmode)
      async with ctx.typing():
        await ctx.reply(
          f"Guess the country based off of the silhouette!{' `[HARD MODE]`' if hardmode else ''}\n-# Disclaimer: Country silhouettes are based upon de facto status, not de jure.",
          file=discord.File(country['image'], filename="country.png"),
          mention_author=False
        )
        def check(answer):
          return answer.content.lower() in [name.lower() for name in country['names']] and answer.channel == ctx.channel
        try:
          msg = await self.bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
          await ctx.channel.send(f"Nobody got it... the answer was {country['names'][0]}!\n-# Valid answers: {', '.join(country['names'])}")
        else:
          await msg.reply(f"{msg.author.mention} got it!")

async def setup(bot):
  await bot.add_cog(guessplace(bot))