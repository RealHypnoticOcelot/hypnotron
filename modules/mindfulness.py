import discord
from discord import app_commands, FFmpegPCMAudio
from discord.ext import commands, tasks
import aiohttp
from dotenv import dotenv_values

async def getmindfulness():
  async with aiohttp.ClientSession() as session:
    async with session.get("https://inspirobot.me/api?generateFlow=1") as resp:
      if resp.status != 200:
        return None
      json = await resp.json()
      return json

class mindfulness(commands.Cog):
  def __init__(self, bot):
    self.bot = bot # adding a bot attribute for easier access
    self.mindfulness.start()

  async def cog_unload(self):
    self.mindfulness.cancel()

  @tasks.loop(seconds=None)
  async def mindfulness(self):
    while True:
      while not self.voiceclient.is_connected():
        try:
          self.voiceclient = await self.mindfuness_channel.connect()
        except:
          pass
      mp3 = await getmindfulness()
      source = FFmpegPCMAudio(mp3['mp3'], executable="ffmpeg")
      self.voiceclient.play(source)
      # typing lined up with mp3 file
      previoustime = 0
      typingtime = random.randint(5,20) / 10
      for entry in mp3['data']:
        if entry['type'] != "stop":
          await asyncio.sleep((entry['time'] - previoustime) - typingtime - 0.5)
          async with mindfulness_channel.typing():
            await asyncio.sleep(typingtime)
            if entry['type'] == "quote":
              await self.channel.send(f"```\n{entry['text']}\n```")
              previoustime = entry['time']
        # wait to finish if not done
        while self.voiceclient.is_playing():
          await asyncio.sleep(1)

  @mindfulness.before_loop
  async def before_mindfulness(self):
    await self.bot.wait_until_ready()
    guild = await self.bot.fetch_guild(
      dotenv_values()['MINDFULNESS_GUILD']
    )
    self.mindfulness_channel = await guild.fetch_channel(
      dotenv_values()['MINDFULNESS_CHANNEL']
    )
    self.voiceclient = await self.mindfulness_channel.connect()

  @mindfulness.after_loop
  async def after_mindfulness(self):
    await self.voiceclient.disconnect()

async def setup(bot):
  await bot.add_cog(mindfulness(bot=bot))