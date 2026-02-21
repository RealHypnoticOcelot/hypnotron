import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiohttp

class discordstatus(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="discordstatus", description="Get Discord's status!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  async def REPLACEME(self, ctx):
    async with aiohttp.ClientSession() as session:
      async with session.get(f"https://discordstatus.com/api/v2/summary.json") as resp:
        if resp.status != 200:
          return await ctx.reply(f"Error: Response code {resp.status}", mention_author=False, ephemeral=True)
        data = await resp.json()

        status_status = data['status']['description']
        if data['incidents'] == []:
          status_description = "No Unresolved Incidents"
        else:
          status_description = []
          for i in data['incidents']:
            status_description.append(f"**{i['name']}**\n{i['incident_updates'][0]['body']}")
          status_description = "\n\n".join(status_description)
        
        embed = discord.Embed(
          color=discord.Color.random(), 
          title=f"Discord Status: {status_status}",
          description=status_description, 
          url="https://discordstatus.com/")
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
  await bot.add_cog(discordstatus(bot=bot))