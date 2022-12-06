# -*- coding: utf8 -*-
from discord.ext import commands
import discord
import time as t
import asyncio
import datetime
import random
import re
from discord import app_commands, Interaction
from discord.app_commands import Choice
from typing import Literal
import typing
import mysql.connector
from PIL import Image, ImageFont, ImageDraw, ImageOps
from urllib.request import urlopen
import os
from io import BytesIO

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("h!"), case_insensitive=True, intents=intents, activity=discord.Streaming(name="Haviture", url="https://twitch.tv/haviture_ch"))

flagpairs = [("🇦🇨", "Ascension Island"), ("🇦🇩", "Andorra"), ("🇦🇪", "United Arab Emirates"), ("🇦🇫", "Afghanistan"), ("🇦🇬", "Antigua & Barbuda"), ("🇦🇮", "Anguilla"), ("🇦🇱", "Albania"), ("🇦🇲", "Armenia"), ("🇦🇴", "Angola"), ("🇦🇶", "Antarctica"), ("🇦🇷", "Argentina"), ("🇦🇸", "American Samoa"), ("🇦🇹", "Austria"), ("🇦🇺", "Australia"), ("🇦🇼", "Aruba"), ("🇦🇽", "Åland Islands"), ("🇦🇿", "Azerbaijan"), ("🇧🇦", "Bosnia & Herzegovina"), ("🇧🇧", "Barbados"), ("🇧🇩", "Bangladesh"), ("🇧🇪", "Belgium"), ("🇧🇫", "Burkina Faso"), ("🇧🇬", "Bulgaria"), ("🇧🇭", "Bahrain"), ("🇧🇮", "Burundi"), ("🇧🇯", "Benin"), ("🇧🇱", "St. Barthélemy"), ("🇧🇲", "Bermuda"), ("🇧🇳", "Brunei"), ("🇧🇴", "Bolivia"), ("🇧🇶", "Caribbean Netherlands"), ("🇧🇷", "Brazil"), ("🇧🇸", "Bahamas"), ("🇧🇹", "Bhutan"), ("🇧🇻", "Bouvet Island"), ("🇧🇼", "Botswana"), ("🇧🇾", "Belarus"), ("🇧🇿", "Belize"), ("🇨🇦", "Canada"), ("🇨🇨", "Cocos (Keeling) Islands"), ("🇨🇩", "Congo - Kinshasa"), ("🇨🇫", "Central African Republic"), ("🇨🇬", "Congo - Brazzaville"), ("🇨🇭", "Switzerland"), ("🇨🇮", "Côte D\’Ivoire"), ("🇨🇰", "Cook Islands"), ("🇨🇱", "Chile"), ("🇨🇲", "Cameroon"), ("🇨🇳", "China"), ("🇨🇴", "Colombia"), ("🇨🇵", "Clipperton Island"), ("🇨🇷", "Costa Rica"), ("🇨🇺", "Cuba"), ("🇨🇻", "Cape Verde"), ("🇨🇼", "Curaçao"), ("🇨🇽", "Christmas Island"), ("🇨🇾", "Cyprus"), ("🇨🇿", "Czechia"), ("🇩🇪", "Germany"), ("🇩🇬", "Diego Garcia"), ("🇩🇯", "Djibouti"), ("🇩🇰", "Denmark"), ("🇩🇲", "Dominica"), ("🇩🇴", "Dominican Republic"), ("🇩🇿", "Algeria"), ("🇪🇦", "Ceuta & Melilla"), ("🇪🇨", "Ecuador"), ("🇪🇪", "Estonia"), ("🇪🇬", "Egypt"), ("🇪🇭", "Western Sahara"), ("🇪🇷", "Eritrea"), ("🇪🇸", "Spain"), ("🇪🇹", "Ethiopia"), ("🇪🇺", "European Union"), ("🇫🇮", "Finland"), ("🇫🇯", "Fiji"), ("🇫🇰", "Falkland Islands"), ("🇫🇲", "Micronesia"), ("🇫🇴", "Faroe Islands"), ("🇫🇷", "France"), ("🇬🇦", "Gabon"), ("🇬🇧", "United Kingdom"), ("🇬🇩", "Grenada"), ("🇬🇪", "Georgia"), ("🇬🇫", "French Guiana"), ("🇬🇬", "Guernsey"), ("🇬🇭", "Ghana"), ("🇬🇮", "Gibraltar"), ("🇬🇱", "Greenland"), ("🇬🇲", "Gambia"), ("🇬🇳", "Guinea"), ("🇬🇵", "Guadeloupe"), ("🇬🇶", "Equatorial Guinea"), ("🇬🇷", "Greece"), ("🇬🇸", "South Georgia & South Sandwich Islands"), ("🇬🇹", "Guatemala"), ("🇬🇺", "Guam"), ("🇬🇼", "Guinea-Bissau"), ("🇬🇾", "Guyana"), ("🇭🇰", "Hong Kong"), ("🇭🇲", "Heard & McDonald Islands"), ("🇭🇳", "Honduras"), ("🇭🇷", "Croatia"), ("🇭🇹", "Haiti"), ("🇭🇺", "Hungary"), ("🇮🇨", "Canary Islands"), ("🇮🇩", "Indonesia"), ("🇮🇪", "Ireland"), ("🇮🇱", "Israel"), ("🇮🇲", "Isle of Man"), ("🇮🇳", "India"), ("🇮🇴", "British Indian Ocean Territory"), ("🇮🇶", "Iraq"), ("🇮🇷", "Iran"), ("🇮🇸", "Iceland"), ("🇮🇹", "Italy"), ("🇯🇪", "Jersey"), ("🇯🇲", "Jamaica"), ("🇯🇴", "Jordan"), ("🇯🇵", "Japan"), ("🇰🇪", "Kenya"), ("🇰🇬", "Kyrgyzstan"), ("🇰🇭", "Cambodia"), ("🇰🇮", "Kiribati"), ("🇰🇲", "Comoros"), ("🇰🇳", "St. Kitts & Nevis"), ("🇰🇵", "North Korea"), ("🇰🇷", "South Korea"), ("🇰🇼", "Kuwait"), ("🇰🇾", "Cayman Islands"), ("🇰🇿", "Kazakhstan"), ("🇱🇦", "Laos"), ("🇱🇧", "Lebanon"), ("🇱🇨", "St. Lucia"), ("🇱🇮", "Liechtenstein"), ("🇱🇰", "Sri Lanka"), ("🇱🇷", "Liberia"), ("🇱🇸", "Lesotho"), ("🇱🇹", "Lithuania"), ("🇱🇺", "Luxembourg"), ("🇱🇻", "Latvia"), ("🇱🇾", "Libya"), ("🇲🇦", "Morocco"), ("🇲🇨", "Monaco"), ("🇲🇩", "Moldova"), ("🇲🇪", "Montenegro"), ("🇲🇫", "St. Martin"), ("🇲🇬", "Madagascar"), ("🇲🇭", "Marshall Islands"), ("🇲🇰", "Macedonia"), ("🇲🇱", "Mali"), ("🇲🇲", "Myanmar (Burma)"), ("🇲🇳", "Mongolia"), ("🇲🇴", "Macau SAR China"), ("🇲🇵", "Northern Mariana Islands"), ("🇲🇶", "Martinique"), ("🇲🇷", "Mauritania"), ("🇲🇸", "Montserrat"), ("🇲🇹", "Malta"), ("🇲🇺", "Mauritius"), ("🇲🇻", "Maldives"), ("🇲🇼", "Malawi"), ("🇲🇽", "Mexico"), ("🇲🇾", "Malaysia"), ("🇲🇿", "Mozambique"), ("🇳🇦", "Namibia"), ("🇳🇨", "New Caledonia"), ("🇳🇪", "Niger"), ("🇳🇫", "Norfolk Island"), ("🇳🇬", "Nigeria"), ("🇳🇮", "Nicaragua"), ("🇳🇱", "Netherlands"), ("🇳🇴", "Norway"), ("🇳🇵", "Nepal"), ("🇳🇷", "Nauru"), ("🇳🇺", "Niue"), ("🇳🇿", "New Zealand"), ("🇴🇲", "Oman"), ("🇵🇦", "Panama"), ("🇵🇪", "Peru"), ("🇵🇫", "French Polynesia"), ("🇵🇬", "Papua New Guinea"), ("🇵🇭", "Philippines"), ("🇵🇰", "Pakistan"), ("🇵🇱", "Poland"), ("🇵🇲", "St. Pierre & Miquelon"), ("🇵🇳", "Pitcairn Islands"), ("🇵🇷", "Puerto Rico"), ("🇵🇸", "Palestinian Territories"), ("🇵🇹", "Portugal"), ("🇵🇼", "Palau"), ("🇵🇾", "Paraguay"), ("🇶🇦", "Qatar"), ("🇷🇪", "Réunion"), ("🇷🇴", "Romania"), ("🇷🇸", "Serbia"), ("🇷🇺", "Russia"), ("🇷🇼", "Rwanda"), ("🇸🇦", "Saudi Arabia"), ("🇸🇧", "Solomon Islands"), ("🇸🇨", "Seychelles"), ("🇸🇩", "Sudan"), ("🇸🇪", "Sweden"), ("🇸🇬", "Singapore"), ("🇸🇭", "St. Helena"), ("🇸🇮", "Slovenia"), ("🇸🇯", "Svalbard & Jan Mayen"), ("🇸🇰", "Slovakia"), ("🇸🇱", "Sierra Leone"), ("🇸🇲", "San Marino"), ("🇸🇳", "Senegal"), ("🇸🇴", "Somalia"), ("🇸🇷", "Suriname"), ("🇸🇸", "South Sudan"), ("🇸🇹", "São Tomé & Príncipe"), ("🇸🇻", "El Salvador"), ("🇸🇽", "Sint Maarten"), ("🇸🇾", "Syria"), ("🇸🇿", "Swaziland"), ("🇹🇦", "Tristan Da Cunha"), ("🇹🇨", "Turks & Caicos Islands"), ("🇹🇩", "Chad"), ("🇹🇫", "French Southern Territories"), ("🇹🇬", "Togo"), ("🇹🇭", "Thailand"), ("🇹🇯", "Tajikistan"), ("🇹🇰", "Tokelau"), ("🇹🇱", "Timor-Leste"), ("🇹🇲", "Turkmenistan"), ("🇹🇳", "Tunisia"), ("🇹🇴", "Tonga"), ("🇹🇷", "Turkey"), ("🇹🇹", "Trinidad & Tobago"), ("🇹🇻", "Tuvalu"), ("🇹🇼", "Taiwan"), ("🇹🇿", "Tanzania"), ("🇺🇦", "Ukraine"), ("🇺🇬", "Uganda"), ("🇺🇲", "United States"), ("🇺🇳", "United Nations"), ("🇺🇾", "Uruguay"), ("🇺🇿", "Uzbekistan"), ("🇻🇦", "Vatican City"), ("🇻🇨", "St. Vincent & Grenadines"), ("🇻🇪", "Venezuela"), ("🇻🇬", "British Virgin Islands"), ("🇻🇮", "U.S. Virgin Islands"), ("🇻🇳", "Vietnam"), ("🇻🇺", "Vanuatu"), ("🇼🇫", "Wallis & Futuna"), ("🇼🇸", "Samoa"), ("🇽🇰", "Kosovo"), ("🇾🇪", "Yemen"), ("🇾🇹", "Mayotte"), ("🇿🇦", "South Africa"), ("🇿🇲", "Zambia"), ("🇿🇼", "Zimbabwe"), ("🏴󠁧󠁢󠁥󠁮󠁧󠁿", "England"), ("🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Scotland"), ("🏴󠁧󠁢󠁷󠁬󠁳󠁿," "Wales")]
print("Flag Emojis up to date as of October 25, 2022")

@bot.event
async def on_ready():
    print(f'Bot connected, logged in as {bot.user}, ID {bot.user.id}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadLiteralArgument):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        return
    else:
        raise error

def getbuttons(index):
    name4 = random.choice(flagpairs)
    names = [random.choice(flagpairs)[index], random.choice(flagpairs)[index], random.choice(flagpairs)[index], name4[index]] # name4 will be the answer one, we chose this one special because it has both index 1 and 2 saved
    while len(names) != len(set(names)): # Re-roll if there are duplicates
        name4 = random.choice(flagpairs)
        names = [random.choice(flagpairs)[index], random.choice(flagpairs)[index], random.choice(flagpairs)[index], name4[index]]
        print("\n\n\nRerolled because of duplicates")
    if index == 1: # crude statement to check whether we're looking for flags or for flag names
        answer = name4[0]
        match = name4[1]
    else:
        answer = name4[1]
        match = name4[0]
    
    random.shuffle(names) # shuffle it so that it's not always answer 4
    return(names, answer, match)

@bot.hybrid_command(name = "guessplace", with_app_command=True, description="Guess the name of a place from its flag!")
@app_commands.describe(
    guesstype="Choose whether to guess the flag or the place!"
)
async def guessplace(ctx: commands.Context, guesstype: Literal["flag", "place"]):
    if guesstype.lower() == "flag":
        flagorplace = "place"
        sendorguess = "Guess"
        guesstype = 0
    elif guesstype.lower() == "place":
        flagorplace = "flag"
        sendorguess = "Send"
        guesstype = 1
    input = getbuttons(guesstype)
    await ctx.reply(f"{sendorguess} the {flagorplace}: {input[2]}", mention_author=False)
    channel = ctx.channel
    def check(m):
            return m.content.lower() == input[1].lower() and m.channel == channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=20)
    except asyncio.TimeoutError:
        await channel.send(f"Nobody got it... the {flagorplace} was {input[1]}!")
        print(f"Nobody got the word, word was {input[1]}")
    else:
        await msg.reply(f"{msg.author.mention} got it!")
        print(f"{msg.author}({msg.author.id}) won in {msg.guild.name}({msg.guild.id}), word was {input[1]}")

@bot.hybrid_command(name="resync", with_app_command=True, description="Resync the commands!")
async def resync(ctx: commands.Context):
    if ctx.message.author.guild_permissions.administrator:
        await bot.tree.sync()
        await ctx.reply(content="Resynced slash commands!", mention_author=False, ephemeral=True)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

def raptvfunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        overlay = Image.open("raptvnotext.png")
        bg = Image.open(BytesIO(img))
        font = ImageFont.truetype(font='steelfisheb.otf', size=400)

        bg = bg.resize((overlay.size[0], overlay.size[1]))
        bg = bg.convert("RGBA")
        final = Image.alpha_composite(bg, overlay)
        draw = ImageDraw.Draw(im=final)
        text=msg.upper()

        def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
                lines = ['']
                for word in text.split():
                    line = f'{lines[-1]} {word}'.strip()
                    if font.getlength(line) <= line_length:
                        lines[-1] = line
                    else:
                        lines.append(word)
                return '\n'.join(lines)
        draw.text(xy=(final.size[0]/2, final.size[1]/2 + 300), text=get_wrapped_text(text, font, line_length=2950), font=font, fill='#FF6508', anchor='ma')
        output_buffer = BytesIO()
        final.save(output_buffer, "png")  # or whatever format
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="raptv", with_app_command=True, description="Create a post akin to the RapTV Instagram account!")
async def raptv(ctx: commands.Context, img: discord.Attachment, *, msg: str):
    img = await img.read()
    async with ctx.typing():
        await ctx.reply(mention_author=False, file=discord.File(raptvfunc(img,msg), filename="output.png"))

def quotefunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        overlay = Image.open("quote.png")
        bg = Image.open(BytesIO(img))
        font = ImageFont.truetype(font='avenirnext.otf', size=50)

        bg = bg.resize((overlay.size[1], overlay.size[1]))
        bg = ImageOps.grayscale(bg)
        bg = bg.convert("RGBA")
        bgfinal = Image.new(mode="RGBA", size=(overlay.size[0], overlay.size[1]))
        bgfinal.paste(bg, (-100, 0))
        final = Image.alpha_composite(bgfinal, overlay)
        draw = ImageDraw.Draw(im=final)
        time = datetime.datetime.now
        mentions = ["dummy mention"]
        for i in msg.mentions:
            mentions.append((i.id, i.name))
            print("mention found")
        for i in mentions:
            if str(i[0]) in str(msg.content):
                withtags = "<@" + str(i[0]) + ">"
                newname = "@" + str(i[1])
                newmsg = str(msg.content).replace(withtags, newname)
            else:
                newmsg = str(msg.content)
        text="\"" + newmsg + "\""
        def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
                lines = ['']
                for word in text.split():
                    line = f'{lines[-1]} {word}'.strip()
                    if font.getlength(line) <= line_length:
                        lines[-1] = line
                    else:
                        lines.append(word)
                return '\n'.join(lines)
        text = get_wrapped_text(text,font, line_length=700)
        if msg.author.nick != None:
            text=text + "\n\n-" + get_wrapped_text(str(msg.author.nick), font, line_length=700) + ", " + str(time().year)
        else:
            text=text + "\n\n-" + get_wrapped_text(str(msg.author.name), font, line_length=700) + ", " + str(time().year)
        draw.text(xy=(final.size[0]/2 + 200, final.size[1]/2), text=text, font=font, fill='#FFFFFF', anchor='mm')
        output_buffer = BytesIO()
        final = final.resize((overlay.size[0], overlay.size[1]))
        final.save(output_buffer, "png", optimize=True, quality=10)  # or whatever format
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="quote", with_app_command=True, description="Create a quote from the most recent message of a member!")
async def quote(ctx: commands.Context, user: discord.Member):
    channel = ctx.channel
    msg = ""
    async for i in channel.history(limit=50):
        if i.author == user:
            if not i.content.lower().startswith("havitron") and not "quote" in i.content.lower():
                msg = i.id
                break
    img = user.display_avatar
    img = await img.read()
    if msg == "":
        await ctx.reply(content="Message not found! Here are some things to check:\n\n**- Does the user's most recent message include text?**\n**- Has the user sent a message within the last 50 messages?**", mention_author=False, ephemeral=True)
        return
    msg = await ctx.fetch_message(msg)
    if msg.content == "":
        await ctx.reply(content="Message not found! Here are some things to check:\n\n**- Does the user's most recent message include text?**\n**- Has the user sent a message within the last 50 messages?**", mention_author=False, ephemeral=True)
        return
    async with ctx.typing():
        await ctx.reply(mention_author=False, file=discord.File(quotefunc(img, msg), filename="output.png"))

@bot.hybrid_command(name="echo", with_app_command=True, description="Send a message to another channel through the bot!")
async def resync(ctx: commands.Context, channels: discord.TextChannel, *, msg: str):
    if ctx.message.author.guild_permissions.administrator:
        await channels.send(msg)
        channeltag = "<#" + str(channels.id) + ">"
        await ctx.reply(content=f"Sent \"{msg}\" to {channeltag}!", mention_author=False, ephemeral=True)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="dice", description="Roll a dice")
async def dice(ctx: commands.Context, maxroll: typing.Optional[int] = 6):
    await ctx.reply(f"The dice landed on {random.randint(1, maxroll)}!", mention_author=False, ephemeral=True)


@bot.hybrid_command(name="ping", description="Get the bot's ping")
async def gifture(ctx: commands.Context):
    await ctx.reply(f"My ping is {round(bot.latency * 1000)}ms.", mention_author=False)

@bot.hybrid_command(name="wheel", description="Spin a wheel between multiple options!")
@app_commands.describe(choices="Options; Comma separate each choice.")
async def wheel(ctx: commands.Context, *, choices: str):
    list = choices.split(",")
    newlist = []
    for i in list:
        i = i.replace(",", "")
        if not i == "":
            i = i.rstrip()
            newlist.append(i)
    if len(list) > 1:
        final = random.choice(newlist)
        await ctx.reply(final, mention_author=False)
        print(f"Selected \"{final}\" from {newlist} for {ctx.message.author}")
    else:
        await ctx.reply("Not enough arguments detected! Did you comma separate them?", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="coinflip", description="Flip a coin!")
async def coinflip(ctx: commands.Context):
    sides = ["Heads", "Tails"]
    side = random.choice(sides)
    await ctx.reply("The coin landed on " + side + "!", mention_author=False)
    print(f"Landed on {side} for {ctx.message.author}")

@bot.event
async def on_message(message):
    if message.author != bot.user: # If the message is from a bot and not a human
        if message.content.lower().startswith('jarvis'): #if it starts with jarvis, the .lower() part makes sure it's not case sensitive
            def ingFrom(s): # Present participle function I copied from https://gist.github.com/arjun921/5f38259ea056fdc35617cb7449fb234e
                for x in s:
                    li.append(x)
                if li[len(li)-1]=='e' and li[len(li)-2]!='i':
                    del li[len(li)-1]
                    li.append("ing")
                elif li[len(li)-1]=='e' and li[len(li)-2]=='i':
                    del li[len(li)-1]
                    del li[len(li)-1]
                    li.append("ying")
                    """To Check"""
                elif li[len(li)-2] in 'aeiou' and li[len(li)-1] not in 'aeiou':
                    temp = li[len(li)-1]
                    del li[len(li)-1]
                    li.append(temp)
                    li.append(temp)
                    li.append("ing")
                elif li[len(li)-1] in 'aeiouy':
                    li.append("ing")
                else:
                    li.append("ing")
                return "".join(li)
            li=[]

            text = message.content
            firstword = []
            list = [*text] # takes the message and splits it up ['l', 'i', 'k', 'e', ' ', 't', 'h', 'i', 's']
            count = 0


            try:
                if list[6] == ",": #if the seventh character in the message is a comma, remove it  from the list(makes sure it supports messages with and without commas)
                    list.pop(6)
            except:
                return #cancels if there's nothing after jarvis
            try:
                list[7]
            except:
                return # cancels if there's nothing after the comma
            while list[6] == " ": #gets rid of all spaces leading up to the first character
                list.pop(6)

            for i in range(6): # remove the phrase "jarvis" from the beginning of the message
                list.pop(0)

            for i in list:
                if i != " ": # repeats until it finishes the first word in list(until there's a space)
                    firstword.append(i)
                    count = count+1 # counts how many characters it added to the firstword list
                else:
                    break # if there's a space, quit
            for i in range(count): # remove the first word from the list
                list.pop(0)
            firstword = "".join(map(str, firstword)) # convert ['t', 'h', 'i', 's'] into 'this'
            mentions = []
            for i in message.mentions:
                mentions.append((i.id, i.nick))
            addtick = 0
            for i in mentions:
                if str(i[0]) in firstword:
                    withtags = "<@" + str(i[0]) + ">"
                    newname = "`@" + str(i[1])
                    firstword = firstword.replace(withtags, newname)
                    addtick = 1
                    tickloc = len(firstword)
                    print(firstword)
            firstwordfinal = ingFrom(firstword) # attempts to make the first word a present participle
            if addtick == 1:
                firstwordfinal = [*firstwordfinal]
                firstwordfinal.insert(tickloc, "`")
                firstwordfinal = "".join(map(str, firstwordfinal))
            list = "".join(map(str, list)) # same as line 63
            list = list.lower()
            list = list.replace('@everyone', '`@everyone`')
            list = list.replace('@here', '`@here`')
            list = re.sub(r'\bi\b', 'you', list)
            list = re.sub(r'\bme\b', 'you', list)
            list = re.sub(r'\bmy\b', 'your', list)

            # creates the final text
            yorn = ["yes", "no"]
            for i in mentions:
                if str(i[0]) in list:
                    withtags = "<@" + str(i[0]) + ">"
                    newname = "`@" + str(i[1]) + "`"
                    list = list.replace(withtags, newname)
            if firstword.endswith("?") or list.endswith("?"):
                final = random.choice(yorn)
            else:
                if addtick == 1:
                    final = firstwordfinal + list
                else:
                    final = firstwordfinal.lower() + list
            print(f"Sent \"{final}\" to {message.guild}({message.guild.id})")
            await message.channel.send(content=final, reference=message, mention_author=False, allowed_mentions=None) # send the final message
    await bot.process_commands(message)

bot.run('TOKEN')
