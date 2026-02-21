import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp
import random

async def tosdr_autocomplete(interaction: discord.Interaction, current: str,) -> list[app_commands.Choice[str]]:
  async with aiohttp.ClientSession() as session:
    services_list = []
    async with session.get(f"https://api.tosdr.org/search/v4/?query={current}") as resp:
      try:
        resp = await resp.json()
        for i in resp['parameters']['services']:
          services_list.append(i["name"])
          if len(services_list) == 25:
            continue
      except:
        pass

    services_list = [
      app_commands.Choice(name=i, value=i)
      for i in services_list
    ]
    return services_list[0 : 25]

# Probably could be done better, but oh well!
class tosdr(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="tosdr", description="Search Terms of Service; Didn't Read")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.autocomplete(search=tosdr_autocomplete)
  async def time(self, ctx, *, search: str):
    async with aiohttp.ClientSession() as session:
      async with session.get(f"https://api.tosdr.org/search/v4/?query={search}") as resp:
        if resp.status != 200:
          return await ctx.reply(f"Error: Response code {resp.status}", mention_author=False, ephemeral=True)
        data = await resp.json()
        try:
          data = data['parameters']['services'][0]
        except IndexError:
          await ctx.reply(f"No service found!", ephemeral=True, mention_author=False)
        randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        tosdr_rating_image = data['links']['crisp']['badge']['png']
        tosdr_service_name = data['name']
        tosdr_service_url = data['links']['crisp']['service']
        tosdr_points_url = data['links']['crisp']['api']

        async with session.get(tosdr_points_url) as resp:
          if resp.status != 200:
            return await ctx.reply('Error!', mention_author=False, ephemeral=True)
          points_data_unfiltered = await resp.json()
          points_data = []
          for i in points_data_unfiltered['parameters']['points']:
            if i['status'] == "approved":
              points_data.append(i)

          points_list = []
          if len(points_data) >= 5:
            point_count = 5
          else:
            points_temp = []
            for i in points_data:
              points_temp.append(i)
            point_count = len(points_temp)
          i = 0
          while len(points_list) < point_count:
            points_list.append(f"- {points_data[i]['title']}")
            i += 1

          if point_count == 5:
            points_list.append(f"And {len(points_data) - point_count} more...")
          points = "\n".join(points_list)
          
          embed = discord.Embed(
            color=randomrgb, 
            title=f"{tosdr_service_name}",
            url=tosdr_service_url,
            description=points
          ).set_image(url=tosdr_rating_image)
          await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(tosdr(bot=bot))