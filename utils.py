import discord
import re

async def mentionstrip(guild: discord.Guild, msg: str):
    def clear_pings(result):
      if result.group(0) == "@everyone":
        return "`@everyone`"
      return "`@here`"
    mentions = []

    matchedmentions = re.findall(r'<@(\d+)>', msg)
    for i in matchedmentions:
      member = await guild.fetch_member(i)
      if member != None:
        mentions.append((f"<@{i}>", member.display_name))
    matchedroles = re.findall(r'<@&(\d+)>', msg)

    for i in matchedroles:
      for x in guild.roles:
        if x.id == int(i):
          rolename = x.name
          mentions.append((f"<@&{i}>", rolename))
  
    for i in mentions: # replace mentions with sanitized versions
      if str(i[0]) in msg:
        newname = "`@" + str(i[1]) + "`"
        msg = msg.replace(str(i[0]), newname)

    msg = re.sub(r'@everyone|@here', clear_pings, msg) # sanitize @everyone and @here
    return msg

def get_mentions(message: discord.Message):
  message_string = message.content

  for user in message.mentions:
    newname = "@" + user.display_name
    message_string = message_string.replace(user.mention, newname)

  for channel in message.channel_mentions:
    newname = "#" + channel.name
    message_string = message_string.replace(channel.mention, newname)
  
  for role in message.role_mentions:
    newname = "@" + role.name
    message_string = message_string.replace(role.mention, newname)
  
  return message_string