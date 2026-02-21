import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime

class itemshop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="itemshop", description="Get today's Fortnite item shop!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def itemshop(self, ctx):
    today = datetime.datetime.now(tz=datetime.timezone.utc)
    image_url = f"https://bot.fnbr.co/shop-image/fnbr-shop-{today.day}-{today.month}-{today.year}.png"
    embed = discord.Embed(
      color=discord.Color.random(),
      title=f"Item Shop for {today.strftime('%A, %B %d')}"
    ).set_footer(text="From https://fnbr.co/").set_image(url=image_url)
    await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(itemshop(bot=bot))