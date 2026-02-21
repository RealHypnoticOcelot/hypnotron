import discord
from discord import app_commands
from discord.ext import commands, tasks

class pin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="pin", description="Pin a message from its ID!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    msgid="The message ID of the voice message!"
  )
  @commands.check_any(commands.has_permissions(manage_messages=True), commands.dm_only())
  async def pin(self, ctx, msgid: str):
    try:
      msg = await ctx.channel.fetch_message(int(msgid))
      await msg.pin()
      await ctx.reply(content=f"Successfully pinned message!", mention_author=False, ephemeral=True)
    except ValueError:
      await ctx.reply("Not a valid message ID!", mention_author=False, ephemeral=True)
    except discord.errors.HTTPException:
      await ctx.reply("Could not pin this message!", mention_author=False, ephemeral=True)

  @pin.error
  async def pin_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.reply('Missing permissions!', mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(pin(bot=bot))