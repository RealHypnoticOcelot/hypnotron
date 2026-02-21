import discord
from discord import app_commands
from discord.ext import commands, tasks
import io
from PIL import Image
import re

class hex(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="hex", description="Get the color of a specific hex code!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  @app_commands.describe(
    hex_code="The hex code you'd like to display"
  )
  @app_commands.rename(hex_code="hex")
  async def hex(self, ctx, hex_code: str):
    if len(hex_code) % 2 != 0:
      hex_code = "#" + hex_code
    # Check if valid hex code
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_code):
      async with ctx.typing():
        output_buffer = io.BytesIO()
        Image.new(mode="RGB", size=(128, 128), color=hex_code).save(output_buffer, "png")
        output_buffer.seek(0)
        await ctx.reply(mention_author=False, file=discord.File(output_buffer, filename=f"{hex}.png"))
    else:
      await ctx.reply(content="Not a valid hex code!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(hex(bot=bot))