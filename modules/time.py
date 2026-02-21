import discord
from discord import app_commands
from discord.ext import commands, tasks
import datetime
import pytz
import typing

async def timezone_autocomplete(interaction: discord.Interaction, current: str,) -> list[app_commands.Choice[str]]:
	timezone_list = [
		app_commands.Choice(name=i, value=i)
		for i in pytz.all_timezones if current.lower() in i.lower()
	]
	return timezone_list[0 : 25]

class time(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="time", description="Get the time in a timezone!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.autocomplete(timezone=timezone_autocomplete)
  async def time(self, ctx, timezone: str, ephemeral: typing.Optional[bool] = False):
    try:
      tz = datetime.datetime.now(tz=pytz.timezone(timezone))
      await ctx.reply(f"It's currently **{tz.strftime('%-I:%M %p')}** for {timezone}(`{tz.strftime('%Z')}`).", ephemeral=ephemeral)
    except pytz.exceptions.UnknownTimeZoneError:
      await ctx.reply("Invalid Timezone(s)!", mention_author=False, ephemeral=True)

  @commands.hybrid_command(name="tzdifference", description="Get the time in a timezone!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.autocomplete(timezone1=timezone_autocomplete, timezone2=timezone_autocomplete)
  async def tzdifference(self, ctx, timezone1: str, timezone2: typing.Optional[str] = str(pytz.timezone("UTC"))):
    try:
      tz1 = datetime.datetime.now(tz=pytz.timezone(timezone1))
      tz2 = datetime.datetime.now(tz=pytz.timezone(timezone2))
      difference = tz1.utcoffset() - tz2.utcoffset()
      offset = "behind" if abs(difference.days) != difference.days else "ahead of"
      total_hours = difference.seconds // 3600
      total_minutes = (difference.seconds % 3600) // 60
      if offset == "behind":
        total_hours = 24 - total_hours
        if total_minutes != 0:
          total_minutes = 60 - total_minutes 
      total_minutes = f"and {total_minutes} minutes " if total_minutes != 0 else ""
      total_hours = f"{total_hours} hours " if total_hours > 1 else f"{total_hours} hour "
      timezone1 = f"{timezone1}(`{tz1.strftime('%Z')}`)" if tz1.strftime('%Z') != str(timezone1) else f"`{timezone1}`"
      timezone2 = f"{timezone2}(`{tz2.strftime('%Z')}`)" if tz2.strftime('%Z') != str(timezone2) else f"`{timezone2}`"
      await ctx.reply(f"""{timezone1} is **{total_hours}{total_minutes}{offset}** {timezone2}.
It's currently **{tz1.strftime('%-I:%M %p')}** for {timezone1}.
It's currently **{tz2.strftime('%-I:%M %p')}** for {timezone2}.""", mention_author=False)
    except pytz.exceptions.UnknownTimeZoneError:
      await ctx.reply("Invalid Timezone(s)!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(time(bot=bot))