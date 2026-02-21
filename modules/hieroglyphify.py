import discord
from discord import app_commands
from discord.ext import commands, tasks
import typing
import re

class hieroglyphify(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="hieroglyphify", description="For fun, not super accurate; for best results remove silent letters")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    undo = "Whether to de-hieroglyphify the input text"
  )
  async def hieroglyphify(self, ctx, undo: typing.Optional[bool] = False, *, text: str):
    char_map = [
      ("q", "𓎡"),
      ("w", "𓅃"),
      ("e", "𓅂"),
      ("r", "𓂋"),
      ("t", "𓏏"),
      ("y", "𓇌"),
      ("u", "𓅲"),
      ("i", "𓇋"),
      ("o", "𓅱"),
      ("p", "𓊪"),
      ("a", "𓄿"),
      ("s", "𓋴"),
      ("d", "𓂧"),
      ("f", "𓆑"),
      ("g", "𓎼"),
      ("h", "𓉔"),
      ("j", "𓆓"),
      ("k", "𓈎"),
      ("l", "𓃭"),
      ("z", "𓊃"),
      ("x", "𓇨"),
      ("c", "𓎢"),
      ("v", "𓆯"),
      ("b", "𓃀"),
      ("n", "𓈖"),
      ("m", "𓅓")
    ]

    # Replace multiple occurrences of a character with one instance, i.e. "teeest" becomes "test"
    # I'm just following what r74n did!
    # also makes it lowercase
    text = re.sub(r'(.)\1+', r'\1', text.lower())

    # Replace instances of a character with its hieroglyph equivalent
    if undo == False:
      for i in char_map:
        text = text.replace(i[0], i[1])
    else:
      for i in char_map:
        text = text.replace(i[1], i[0])
    
    await ctx.reply(f"{text}\n-# Adapted from [r74n](<https://c.r74n.com/converter/hieroglyphs>)", mention_author=False)

async def setup(bot):
  await bot.add_cog(hieroglyphify(bot=bot))