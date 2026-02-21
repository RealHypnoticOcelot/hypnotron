import discord
from discord import app_commands
from discord.ext import commands, tasks
import io
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageOps
import math
from utils import get_mentions

class quote(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="quote", description="Quote a user's message!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
  @app_commands.describe(
    msgid="The message ID of the message you'd like to quote!"
  )
  async def quote(self, ctx, msgid: str):
    try:
      msg = await ctx.channel.fetch_message(int(msgid))
      if msg.content != "":
        avatar = await msg.author.display_avatar.read()
        with Image.new("RGBA", size=(1280, 720), color='black') as quote_image:
          
          # Paste avatar onto canvas
          avatar = Image.open(io.BytesIO(avatar)).resize((quote_image.size[1], quote_image.size[1]), resample=Image.Resampling.BICUBIC)
          avatar = ImageOps.grayscale(avatar)
          quote_image.paste(
            avatar,
            (
              int(-(quote_image.size[0] * 0.1)),
              0
            )
          )
          
          # Add a little gradient between the avatar and the canvas
          # Not my best work, but it'll do!
          rectangle = Image.new("RGBA", size=(quote_image.size[1], quote_image.size[1]))
          gradient = Image.linear_gradient('L').rotate(90).resize((rectangle.size[0],rectangle.size[1]))
          gamma = 0.7 # More means more transparency
          gradient = gradient.point(lambda f: int((f/255.0)**(1/gamma)*255))
          rectangle.putalpha(gradient)
          quote_image.paste(
            rectangle,
            (
              int(-(quote_image.size[0] * 0.1)),
              0
            ), 
            mask=rectangle
          )

          # Add the actual quote to the image
          def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
            lines = ['']
            for word in text.split():
              line = f'{lines[-1]} {word}'.strip()
              if font.getlength(line) <= line_length:
                lines[-1] = line
              else:
                lines.append(word)
            return '\n'.join(lines)
          # Some nightmare math that does generally manage to return an accurate font size for most text
          fontsize = (
            100/(1+math.sqrt(len(msg.content))/15)
          )
          font = ImageFont.truetype(
            font=(Path.cwd() / "quotes" / "Junicode-Cond.ttf"),
            size=fontsize
          )
          finaltext = (
            get_wrapped_text(f"\"{get_mentions(msg)}\"", font, 550) + 
            "\n\n-" +
            get_wrapped_text(msg.author.display_name, font, 550) + f", {msg.created_at.year}"
          )
          draw = ImageDraw.Draw(quote_image).multiline_text(
            xy=(quote_image.size[0]/2 + (avatar.size[1] / 2.5), quote_image.size[1]/2,),
            text=finaltext,
            font=font,
            fill='#FFFFFF',
            anchor="mm"
          )

          output_buffer = io.BytesIO()
          quote_image.save(output_buffer, "png", optimize=True, quality=10)
          output_buffer.seek(0) # Get the first frame, if this somehow manages to be a gif
          await ctx.reply(file=discord.File(output_buffer, filename="quote.png"), mention_author=False)
      else:
        await ctx.reply("Message has no content!", mention_author=False, ephemeral=True)
    except discord.NotFound:
      await ctx.reply("Couldn't find message! Was it sent in this channel?", mention_author=False, ephemeral=True)
    except ValueError:
      await ctx.reply("Invalid message ID!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(quote(bot=bot))