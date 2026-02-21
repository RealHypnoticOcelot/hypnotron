import discord
from discord import app_commands
from discord.ext import commands, tasks

class delete(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="delete", description="Delete my messages!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    count = "The number of messages to delete"
  )
  @commands.check_any(commands.has_permissions(manage_messages=True), commands.dm_only())
  async def delete(self, ctx, count: int):
    await ctx.reply(f"Deleting {count} messages!", mention_author=False, ephemeral=True)
    if not ctx.interaction:
      count += 1
    async for msg in ctx.channel.history():
      if msg.author == bot.user:
        messages.append(i)
    for i in range(count):
      if messages != []:
        await messages[0].delete()
        await asyncio.sleep(1)
        messages.pop(0)

async def setup(bot):
  await bot.add_cog(delete(bot=bot))