import discord
from discord import app_commands
from discord.ext import commands, tasks
import io
from PIL import Image, UnidentifiedImageError

class NoStickerSlots(commands.CheckFailure):
  pass

class addsticker(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  async def slots_available(ctx):
    if ctx.guild.sticker_limit - len(await ctx.guild.fetch_stickers()) > 0:
      return True
    raise NoStickerSlots()

  @commands.hybrid_command(name="addsticker", description="REPLACEME")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    img = "Image to convert to a sticker. Will be resized."
  )
  @app_commands.rename(img="image")
  @commands.has_permissions(create_expressions=True)
  @commands.check(slots_available)
  async def addsticker(self, ctx, img: discord.Attachment, emoji: str, *, stickername: str):
    async with ctx.typing():
      try:
        sticker = Image.open(io.BytesIO(await img.read())).resize((320, 320))
        output_buffer = io.BytesIO()
        sticker.save(output_buffer, "png")
        output_buffer.seek(0)
        await ctx.guild.create_sticker(name=stickername, emoji=emoji, file=discord.File(output_buffer, filename="sticker.png"), description="")
        remainingSlots = str(ctx.guild.sticker_limit - len(await ctx.guild.fetch_stickers()))
        await ctx.reply(f"Created \"**{stickername}**\"! `{remainingSlots}` slot(s) remaining!", mention_author=False, ephemeral=True)
      except UnidentifiedImageError:
        await ctx.reply("Invalid attachment!", mention_author=False, ephemeral=True)
      except discord.errors.HTTPException:
        await ctx.reply("Invalid emoji!", mention_author=False, ephemeral=True)
  
  @addsticker.error
  async def addsticker_error(self, ctx, error):
    if isinstance(error, NoStickerSlots):
      await ctx.reply('No available sticker slots!', mention_author=False, ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
      await ctx.reply('Missing permissions!', mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(addsticker(bot=bot))