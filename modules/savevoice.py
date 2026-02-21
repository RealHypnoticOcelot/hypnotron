import discord
from discord import app_commands
from discord.ext import commands, tasks

class savevoice(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access

  @commands.hybrid_command(name="savevoice", description="Download a voice message!")
  @app_commands.allowed_installs(guilds=True, users=True)
  @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # Guilds, DMs, DMs/Group DMs
  @app_commands.describe(
    msgid="The message ID of the voice message!"
  )
  async def savevoice(self, ctx, msgid: str):
    try:
      msg = await ctx.channel.fetch_message(int(msgid))
      if msg.flags.voice == True:
        ogg = await msg.attachments[0].to_file(filename=f"{msg.author.name}_{msg.created_at.strftime('%Y-%m-%d')}.ogg")
        await ctx.reply(file=ogg)
      else:
        await ctx.reply("Not a voice message!", mention_author=False, ephemeral=True)
    except ValueError:
      await ctx.reply("Not a valid message ID!", mention_author=False, ephemeral=True)

async def setup(bot):
  await bot.add_cog(savevoice(bot=bot))