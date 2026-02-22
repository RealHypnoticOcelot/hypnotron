# -*- coding: utf8 -*-
import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction
from discord.app_commands import Choice
import difflib
import time as t
import asyncio
import datetime
import random
import re
import io
import aiohttp
import math
from math import log10, floor
from typing import Literal
import typing
from PIL import Image, ImageFont, ImageDraw, ImageOps
from urllib.request import urlopen
from urllib import parse
from urllib.parse import urlsplit
import json
import os
from io import BytesIO
import atexit
import logging
import pytz
import unicodedata
import openai
from openai import AsyncOpenAI
from pathlib import Path
import comics
from comics.exceptions import InvalidEndpointError, InvalidDateError

# Old code! It's no good, just here for parts
# Made with Python version 3.12.3

newrules = """
## 1. Harassment
 - Harassment is not tolerated at all in this server. Joking around is fine of course, but if someone asks you to stop, you must do so
  - if you feel as if someone is crossing the line you should tell them directly or contact a moderator
 - Racism, transphobia, homophobia, ableism, and any and all slurs - claimable or not - are strictly prohibited
  - A list of automatically moderated slurs can be found [here](<https://haviture.ch/slurs.txt>)
  - Intentionally bypassing the slur filter will result in being punished at a moderator's discretion
  - Referencing slurs, like using the term "bundle of sticks" to reference the f-slur, is also not allowed

## 2. Prohibited content
 - Pornographic content is not allowed, a majority of the server members are underage
  - If you are posting something suggestive that is something the average person would not want to be seen looking at in public, spoiler it or it will be deleted
  - Repeatedly violating this rule will result in punishment
 - Posting any gore or shock content will result in a ban

## 3. Server etiquette
 - Spamming images, text, or emotes are not allowed
  - ASCII/Text art and copypastas will be deleted; repeatedly violating this rule may result in punishment
 - Please try to use channels for the intended purposes (i.e. gaming goes in <#912965437694803968>, memes go in <#912965043312803840>, etc.)
  - Please no constant meme posting in general even if you have image perms
 - Please do not be annoying in voice chats
  - if someone is being annoying in voice chats feel free to mute them on your end
 - Do not DM moderators about punishments besides bans

## Image and embed perms in <#912964431552610335> 
To prevent image spamming in <#912964431552610335>, image perms are only given to <@&953496931739512873> or <@&916096225445564497>
 - All users can use images in <#993202397163827221> and most other channels besides <#912964431552610335>
 - If you are a subscriber, you can learn how to connect your Twitch account to your Discord account [here](<https://support.discord.com/hc/en-us/articles/212112068>)

"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("havitron, ", "havitron ", "Havitron ", "Havitron, ", "h!"), case_insensitive=True, intents=intents, activity=discord.Streaming(name="Haviture", url="https://twitch.tv/haviture_ch"))

time = datetime.datetime.now(tz=datetime.timezone.utc)
flagpairshard = [("🇦🇨", "Ascension Island"), ("🇦🇩", "Andorra"), ("🇦🇪", "United Arab Emirates"), ("🇦🇫", "Afghanistan"), ("🇦🇬", "Antigua & Barbuda"), ("🇦🇮", "Anguilla"), ("🇦🇱", "Albania"), ("🇦🇲", "Armenia"), ("🇦🇴", "Angola"), ("🇦🇶", "Antarctica"), ("🇦🇷", "Argentina"), ("🇦🇸", "American Samoa"), ("🇦🇹", "Austria"), ("🇦🇺", "Australia"), ("🇦🇼", "Aruba"), ("🇦🇽", "Åland Islands"), ("🇦🇿", "Azerbaijan"), ("🇧🇦", "Bosnia & Herzegovina"), ("🇧🇧", "Barbados"), ("🇧🇩", "Bangladesh"), ("🇧🇪", "Belgium"), ("🇧🇫", "Burkina Faso"), ("🇧🇬", "Bulgaria"), ("🇧🇭", "Bahrain"), ("🇧🇮", "Burundi"), ("🇧🇯", "Benin"), ("🇧🇱", "St. Barthélemy"), ("🇧🇲", "Bermuda"), ("🇧🇳", "Brunei"), ("🇧🇴", "Bolivia"), ("🇧🇶", "Caribbean Netherlands"), ("🇧🇷", "Brazil"), ("🇧🇸", "Bahamas"), ("🇧🇹", "Bhutan"), ("🇧🇻", "Bouvet Island"), ("🇧🇼", "Botswana"), ("🇧🇾", "Belarus"), ("🇧🇿", "Belize"), ("🇨🇦", "Canada"), ("🇨🇨", "Cocos (Keeling) Islands"), ("🇨🇩", "Congo - Kinshasa"), ("🇨🇫", "Central African Republic"), ("🇨🇬", "Congo - Brazzaville"), ("🇨🇭", "Switzerland"), ("🇨🇮", "Côte D\’Ivoire"), ("🇨🇰", "Cook Islands"), ("🇨🇱", "Chile"), ("🇨🇲", "Cameroon"), ("🇨🇳", "China"), ("🇨🇴", "Colombia"), ("🇨🇵", "Clipperton Island"), ("🇨🇷", "Costa Rica"), ("🇨🇺", "Cuba"), ("🇨🇻", "Cape Verde"), ("🇨🇼", "Curaçao"), ("🇨🇽", "Christmas Island"), ("🇨🇾", "Cyprus"), ("🇨🇿", "Czechia"), ("🇩🇪", "Germany"), ("🇩🇬", "Diego Garcia"), ("🇩🇯", "Djibouti"), ("🇩🇰", "Denmark"), ("🇩🇲", "Dominica"), ("🇩🇴", "Dominican Republic"), ("🇩🇿", "Algeria"), ("🇪🇦", "Ceuta & Melilla"), ("🇪🇨", "Ecuador"), ("🇪🇪", "Estonia"), ("🇪🇬", "Egypt"), ("🇪🇭", "Western Sahara"), ("🇪🇷", "Eritrea"), ("🇪🇸", "Spain"), ("🇪🇹", "Ethiopia"), ("🇪🇺", "European Union"), ("🇫🇮", "Finland"), ("🇫🇯", "Fiji"), ("🇫🇰", "Falkland Islands"), ("🇫🇲", "Micronesia"), ("🇫🇴", "Faroe Islands"), ("🇫🇷", "France"), ("🇬🇦", "Gabon"), ("🇬🇧", "United Kingdom"), ("🇬🇩", "Grenada"), ("🇬🇪", "Georgia"), ("🇬🇫", "French Guiana"), ("🇬🇬", "Guernsey"), ("🇬🇭", "Ghana"), ("🇬🇮", "Gibraltar"), ("🇬🇱", "Greenland"), ("🇬🇲", "Gambia"), ("🇬🇳", "Guinea"), ("🇬🇵", "Guadeloupe"), ("🇬🇶", "Equatorial Guinea"), ("🇬🇷", "Greece"), ("🇬🇸", "South Georgia & South Sandwich Islands"), ("🇬🇹", "Guatemala"), ("🇬🇺", "Guam"), ("🇬🇼", "Guinea-Bissau"), ("🇬🇾", "Guyana"), ("🇭🇰", "Hong Kong"), ("🇭🇲", "Heard & McDonald Islands"), ("🇭🇳", "Honduras"), ("🇭🇷", "Croatia"), ("🇭🇹", "Haiti"), ("🇭🇺", "Hungary"), ("🇮🇨", "Canary Islands"), ("🇮🇩", "Indonesia"), ("🇮🇪", "Ireland"), ("🇮🇱", "Israel"), ("🇮🇲", "Isle of Man"), ("🇮🇳", "India"), ("🇮🇴", "British Indian Ocean Territory"), ("🇮🇶", "Iraq"), ("🇮🇷", "Iran"), ("🇮🇸", "Iceland"), ("🇮🇹", "Italy"), ("🇯🇪", "Jersey"), ("🇯🇲", "Jamaica"), ("🇯🇴", "Jordan"), ("🇯🇵", "Japan"), ("🇰🇪", "Kenya"), ("🇰🇬", "Kyrgyzstan"), ("🇰🇭", "Cambodia"), ("🇰🇮", "Kiribati"), ("🇰🇲", "Comoros"), ("🇰🇳", "St. Kitts & Nevis"), ("🇰🇵", "North Korea"), ("🇰🇷", "South Korea"), ("🇰🇼", "Kuwait"), ("🇰🇾", "Cayman Islands"), ("🇰🇿", "Kazakhstan"), ("🇱🇦", "Laos"), ("🇱🇧", "Lebanon"), ("🇱🇨", "St. Lucia"), ("🇱🇮", "Liechtenstein"), ("🇱🇰", "Sri Lanka"), ("🇱🇷", "Liberia"), ("🇱🇸", "Lesotho"), ("🇱🇹", "Lithuania"), ("🇱🇺", "Luxembourg"), ("🇱🇻", "Latvia"), ("🇱🇾", "Libya"), ("🇲🇦", "Morocco"), ("🇲🇨", "Monaco"), ("🇲🇩", "Moldova"), ("🇲🇪", "Montenegro"), ("🇲🇫", "St. Martin"), ("🇲🇬", "Madagascar"), ("🇲🇭", "Marshall Islands"), ("🇲🇰", "Macedonia"), ("🇲🇱", "Mali"), ("🇲🇲", "Myanmar (Burma)"), ("🇲🇳", "Mongolia"), ("🇲🇴", "Macau SAR China"), ("🇲🇵", "Northern Mariana Islands"), ("🇲🇶", "Martinique"), ("🇲🇷", "Mauritania"), ("🇲🇸", "Montserrat"), ("🇲🇹", "Malta"), ("🇲🇺", "Mauritius"), ("🇲🇻", "Maldives"), ("🇲🇼", "Malawi"), ("🇲🇽", "Mexico"), ("🇲🇾", "Malaysia"), ("🇲🇿", "Mozambique"), ("🇳🇦", "Namibia"), ("🇳🇨", "New Caledonia"), ("🇳🇪", "Niger"), ("🇳🇫", "Norfolk Island"), ("🇳🇬", "Nigeria"), ("🇳🇮", "Nicaragua"), ("🇳🇱", "Netherlands"), ("🇳🇴", "Norway"), ("🇳🇵", "Nepal"), ("🇳🇷", "Nauru"), ("🇳🇺", "Niue"), ("🇳🇿", "New Zealand"), ("🇴🇲", "Oman"), ("🇵🇦", "Panama"), ("🇵🇪", "Peru"), ("🇵🇫", "French Polynesia"), ("🇵🇬", "Papua New Guinea"), ("🇵🇭", "Philippines"), ("🇵🇰", "Pakistan"), ("🇵🇱", "Poland"), ("🇵🇲", "St. Pierre & Miquelon"), ("🇵🇳", "Pitcairn Islands"), ("🇵🇷", "Puerto Rico"), ("🇵🇸", "Palestinian Territories"), ("🇵🇹", "Portugal"), ("🇵🇼", "Palau"), ("🇵🇾", "Paraguay"), ("🇶🇦", "Qatar"), ("🇷🇪", "Réunion"), ("🇷🇴", "Romania"), ("🇷🇸", "Serbia"), ("🇷🇺", "Russia"), ("🇷🇼", "Rwanda"), ("🇸🇦", "Saudi Arabia"), ("🇸🇧", "Solomon Islands"), ("🇸🇨", "Seychelles"), ("🇸🇩", "Sudan"), ("🇸🇪", "Sweden"), ("🇸🇬", "Singapore"), ("🇸🇭", "St. Helena"), ("🇸🇮", "Slovenia"), ("🇸🇯", "Svalbard & Jan Mayen"), ("🇸🇰", "Slovakia"), ("🇸🇱", "Sierra Leone"), ("🇸🇲", "San Marino"), ("🇸🇳", "Senegal"), ("🇸🇴", "Somalia"), ("🇸🇷", "Suriname"), ("🇸🇸", "South Sudan"), ("🇸🇹", "São Tomé & Príncipe"), ("🇸🇻", "El Salvador"), ("🇸🇽", "Sint Maarten"), ("🇸🇾", "Syria"), ("🇸🇿", "Swaziland"), ("🇹🇦", "Tristan Da Cunha"), ("🇹🇨", "Turks & Caicos Islands"), ("🇹🇩", "Chad"), ("🇹🇫", "French Southern Territories"), ("🇹🇬", "Togo"), ("🇹🇭", "Thailand"), ("🇹🇯", "Tajikistan"), ("🇹🇰", "Tokelau"), ("🇹🇱", "Timor-Leste"), ("🇹🇲", "Turkmenistan"), ("🇹🇳", "Tunisia"), ("🇹🇴", "Tonga"), ("🇹🇷", "Turkey"), ("🇹🇹", "Trinidad & Tobago"), ("🇹🇻", "Tuvalu"), ("🇹🇼", "Taiwan"), ("🇹🇿", "Tanzania"), ("🇺🇦", "Ukraine"), ("🇺🇬", "Uganda"), ("🇺🇲", "United States"), ("🇺🇳", "United Nations"), ("🇺🇾", "Uruguay"), ("🇺🇿", "Uzbekistan"), ("🇻🇦", "Vatican City"), ("🇻🇨", "St. Vincent and Grenadines"), ("🇻🇪", "Venezuela"), ("🇻🇬", "British Virgin Islands"), ("🇻🇮", "U.S. Virgin Islands"), ("🇻🇳", "Vietnam"), ("🇻🇺", "Vanuatu"), ("🇼🇫", "Wallis and Futuna"), ("🇼🇸", "Samoa"), ("🇽🇰", "Kosovo"), ("🇾🇪", "Yemen"), ("🇾🇹", "Mayotte"), ("🇿🇦", "South Africa"), ("🇿🇲", "Zambia"), ("🇿🇼", "Zimbabwe"), ("🏴󠁧󠁢󠁥󠁮󠁧󠁿", "England"), ("🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Scotland"), ("🏴󠁧󠁢󠁷󠁬󠁳󠁿," "Wales")]
flagpairs = [("🇦🇩", "Andorra"), ("🇦🇪", "United Arab Emirates"), ("🇦🇫", "Afghanistan"), ("🇦🇬", "Antigua"), ("🇦🇲", "Armenia"), ("🇦🇴", "Angola"), ("🇦🇷", "Argentina"), ("🇦🇹", "Austria"), ("🇦🇺", "Australia"), ("🇦🇿", "Azerbaijan"), ("🇧🇦", "Bosnia"), ("🇧🇧", "Barbados"), ("🇧🇩", "Bangladesh"), ("🇧🇪", "Belgium"), ("🇧🇫", "Burkina Faso"), ("🇧🇬", "Bulgaria"), ("🇧🇭", "Bahrain"), ("🇧🇮", "Burundi"), ("🇧🇯", "Benin"), ("🇧🇲", "Bermuda"), ("🇧🇳", "Brunei"), ("🇧🇴", "Bolivia"), ("🇧🇷", "Brazil"), ("🇧🇸", "Bahamas"), ("🇧🇹", "Bhutan"), ("🇧🇼", "Botswana"), ("🇧🇾", "Belarus"), ("🇧🇿", "Belize"), ("🇨🇦", "Canada"), ("🇨🇩", "Democratic Republic of the Congo"), ("🇨🇫", "Central African Republic"), ("🇨🇬", "Republic of the Congo"), ("🇨🇭", "Switzerland"), ("🇨🇱", "Chile"), ("🇨🇲", "Cameroon"), ("🇨🇳", "China"), ("🇨🇴", "Colombia"), ("🇨🇷", "Costa Rica"), ("🇨🇺", "Cuba"), ("🇨🇻", "Cape Verde"), ("🇨🇾", "Cyprus"), ("🇨🇿", "Czech Republic"), ("🇩🇪", "Germany"), ("🇩🇯", "Djibouti"), ("🇩🇰", "Denmark"), ("🇩🇲", "Dominica"), ("🇩🇴", "Dominican Republic"), ("🇩🇿", "Algeria"), ("🇪🇨", "Ecuador"), ("🇪🇪", "Estonia"), ("🇪🇬", "Egypt"), ("🇪🇷", "Eritrea"), ("🇪🇸", "Spain"), ("🇪🇹", "Ethiopia"), ("🇫🇮", "Finland"), ("🇫🇯", "Fiji"), ("🇫🇰", "Falkland Islands"), ("🇫🇲", "Micronesia"), ("🇫🇴", "Faroe Islands"), ("🇫🇷", "France"), ("🇬🇦", "Gabon"), ("🇬🇧", "United Kingdom"), ("🇬🇩", "Grenada"), ("🇬🇪", "Georgia"), ("🇬🇫", "French Guiana"), ("🇬🇬", "Guernsey"), ("🇬🇭", "Ghana"), ("🇬🇮", "Gibraltar"), ("🇬🇱", "Greenland"), ("🇬🇲", "Gambia"), ("🇬🇳", "Guinea"), ("🇬🇵", "Guadeloupe"), ("🇬🇶", "Equatorial Guinea"), ("🇬🇷", "Greece"), ("🇬🇹", "Guatemala"), ("🇬🇺", "Guam"), ("🇬🇼", "Guinea-Bissau"), ("🇬🇾", "Guyana"), ("🇭🇰", "Hong Kong"), ("🇭🇳", "Honduras"), ("🇭🇷", "Croatia"), ("🇭🇹", "Haiti"), ("🇭🇺", "Hungary"), ("🇮🇨", "Canary Islands"), ("🇮🇩", "Indonesia"), ("🇮🇪", "Ireland"), ("🇮🇱", "Israel"), ("🇮🇲", "Isle of Man"), ("🇮🇳", "India"), ("🇮🇶", "Iraq"), ("🇮🇷", "Iran"), ("🇮🇸", "Iceland"), ("🇮🇹", "Italy"), ("🇯🇪", "Jersey"), ("🇯🇲", "Jamaica"), ("🇯🇴", "Jordan"), ("🇯🇵", "Japan"), ("🇰🇪", "Kenya"), ("🇰🇬", "Kyrgyzstan"), ("🇰🇭", "Cambodia"), ("🇰🇮", "Kiribati"), ("🇰🇲", "Comoros"), ("🇰🇵", "North Korea"), ("🇰🇷", "South Korea"), ("🇰🇼", "Kuwait"), ("🇰🇾", "Cayman Islands"), ("🇰🇿", "Kazakhstan"), ("🇱🇦", "Laos"), ("🇱🇧", "Lebanon"), ("🇱🇨", "St. Lucia"), ("🇱🇮", "Liechtenstein"), ("🇱🇰", "Sri Lanka"), ("🇱🇷", "Liberia"), ("🇱🇸", "Lesotho"), ("🇱🇹", "Lithuania"), ("🇱🇺", "Luxembourg"), ("🇱🇻", "Latvia"), ("🇱🇾", "Libya"), ("🇲🇦", "Morocco"), ("🇲🇨", "Monaco"), ("🇲🇩", "Moldova"), ("🇲🇪", "Montenegro"), ("🇲🇬", "Madagascar"), ("🇲🇭", "Marshall Islands"), ("🇲🇰", "Macedonia"), ("🇲🇱", "Mali"), ("🇲🇲", "Myanmar"), ("🇲🇳", "Mongolia"), ("🇲🇶", "Martinique"), ("🇲🇷", "Mauritania"), ("🇲🇸", "Montserrat"), ("🇲🇹", "Malta"), ("🇲🇺", "Mauritius"), ("🇲🇻", "Maldives"), ("🇲🇼", "Malawi"), ("🇲🇽", "Mexico"), ("🇲🇾", "Malaysia"), ("🇲🇿", "Mozambique"), ("🇳🇦", "Namibia"), ("🇳🇨", "New Caledonia"), ("🇳🇬", "Nigeria"), ("🇳🇮", "Nicaragua"), ("🇳🇱", "Netherlands"), ("🇳🇴", "Norway"), ("🇳🇵", "Nepal"), ("🇳🇷", "Nauru"), ("🇳🇺", "Niue"), ("🇳🇿", "New Zealand"), ("🇴🇲", "Oman"), ("🇵🇦", "Panama"), ("🇵🇪", "Peru"), ("🇵🇫", "French Polynesia"), ("🇵🇬", "Papua New Guinea"), ("🇵🇭", "Philippines"), ("🇵🇰", "Pakistan"), ("🇵🇱", "Poland"), ("🇵🇲", "St. Pierre & Miquelon"), ("🇵🇳", "Pitcairn Islands"), ("🇵🇷", "Puerto Rico"), ("🇵🇸", "Palestinian Territories"), ("🇵🇹", "Portugal"), ("🇵🇼", "Palau"), ("🇵🇾", "Paraguay"), ("🇶🇦", "Qatar"), ("🇷🇴", "Romania"),("🇷🇸", "Serbia"), ("🇷🇺", "Russia"), ("🇷🇼", "Rwanda"), ("🇸🇦", "Saudi Arabia"), ("🇸🇧", "Solomon Islands"), ("🇸🇨", "Seychelles"), ("🇸🇩", "Sudan"), ("🇸🇪", "Sweden"), ("🇸🇬", "Singapore"), ("🇸🇮", "Slovenia"), ("🇸🇰", "Slovakia"), ("🇸🇱", "Sierra Leone"), ("🇸🇲", "San Marino"), ("🇸🇳", "Senegal"), ("🇸🇴", "Somalia"), ("🇸🇷", "Suriname"), ("🇸🇸", "South Sudan"), ("🇸🇻", "El Salvador"), ("🇸🇽", "Sint Maarten"), ("🇸🇾", "Syria"), ("🇸🇿", "Eswatini"), ("🇹🇩", "Chad"), ("🇹🇬", "Togo"), ("🇹🇭", "Thailand"), ("🇹🇯", "Tajikistan"), ("🇹🇰", "Tokelau"), ("🇹🇲", "Turkmenistan"), ("🇹🇳", "Tunisia"), ("🇹🇴", "Tonga"), ("🇹🇷", "Turkey"), ("🇹🇹", "Trinidad & Tobago"), ("🇹🇻", "Tuvalu"), ("🇹🇼", "Taiwan"), ("🇹🇿", "Tanzania"), ("🇺🇦", "Ukraine"), ("🇺🇬", "Uganda"), ("🇺🇳", "United Nations"), ("🇺🇸","United States"), ("🇺🇾", "Uruguay"), ("🇺🇿", "Uzbekistan"), ("🇻🇦", "Vatican City"), ("🇻🇪", "Venezuela"), ("🇻🇬", "British Virgin Islands"), ("🇻🇮", "US Virgin Islands"), ("🇻🇳", "Vietnam"), ("🇻🇺", "Vanuatu"), ("🇼🇫", "Wallis and Futuna"), ("🇼🇸", "Samoa"), ("🇽🇰", "Kosovo"), ("🇾🇪", "Yemen"), ("🇾🇹", "Mayotte"), ("🇿🇦", "South Africa"), ("🇿🇲", "Zambia"), ("🇿🇼", "Zimbabwe")]
flagfacts = [("has the world's oldest oil paintings painted by Buddhists", "has no public christian churches ", "the world's largest producer of opium", "has its official sport as goat catching", "celebrates new year on March 21st ", "Afghanistan"), ("has had a mass protest started due to a tax on traffic lights", "has an average of 5.7 bunkers for every square kilometer", "was declared to be the first atheist country in the world, banning religious practices in its constitution", "has the largest percentage of Muslims in Europe", "Gained independence from the Ottoman empire in 1912", "Albania"), ("has over 200,000 elephants living in its national parks", "has an estimated population of over 77 million people", "is home to the world's highest mountain peak", "has the world's largest artificial lake", "Nepal"), ("has a population of over 11 million people", "has the world's longest coastline of over 25,000km", "was first inhabited by indigenous people, the Arawaks ", "has a history of slavery and colonialism in the Caribbeans", "The Bahamas"), ("is the world's second-largest country by land area", "has the world's longest undefended border", "was the first country to criminalize possession of child pornography", "has the most number of lakes in the world", "Canada"), ("has the largest population of any African country", "is the second-largest producer of cocoa in the world", "is home to the world's most ancient rainforest,", "has the second-highest number of linguistic groups in Africa", "The Democratic Republic of the Congo"), ("has been inhabited by humans since at least 4,000 BC", "has a population of over 85 million people", "is home to one of the oldest civilizations in the world in North Africa", "has the start of world's longest river", "Egypt"), ("has the world's largest population of any Spanish-speaking country", "has the world's largest rainforest", "is the world's fifth-largest country by both area and population", "is home to the world's highest uninterrupted waterfall", "Venezuela"), ("has the world's fourth-largest population", "has the world's busiest port", "has the largest rail infrastructure in Asia", "has the world's oldest surviving wood structure, the Horyu-ji Temple", "China"), ("has the world's highest per capita income", "has the world's oldest surviving republic", "has the world's oldest surviving constitution, dating back to 1600 AD", "San Marino"), ("has the world's highest mountain peak, Mt. Kilimanjaro", "has the world's longest river", "is home to the world's largest desert, the Sahara Desert", "Tanzania"), ("has over 1,200 islands and islets", "has the world's most ancient olive trees, some of which are over 2,000 years old", "is the world's largest producer of olive oil", "Greece"), ("is the world's largest archipelago, with over 17,000 islands", "has the world's most active volcano, Mount Merapi", "is home to the world's highest level of biodiversity", "Indonesia"), ("has the world's largest coral reef system, the Great Barrier Reef", "has the world's largest living organism, the Great Barrier Reef", "has the world's largest sand island, Fraser Island", "Australia"), ("has the world's largest waterfall, Angel Falls", "has the world's highest uninterrupted waterfall", "has the world's highest rate of lightning strikes", "Venezuela"), ("has the world's largest desert, the Sahara Desert", "has the world's longest coastline on the Mediterranean Sea", "has the world's most ancient city", "Tunisia"), ("has the world's largest island", "has the world's longest fjord, Scoresby Sund", "has the world's largest national park", "Denmark"), ("has the world's largest rainforest", "has the world's largest river by volume", "has the world's most diverse wildlife", "Brazil"), ("has the world's largest mangrove forest", "has the world's largest delta", "has the world's largest Royal Bengal Tiger population", "Bangladesh"), ("has the world's largest hot desert, the Sahara Desert", "has the world's largest sand desert", "has the world's largest oil reserves", "Saudi Arabia"), ("has the world's largest lake", "has the world's largest salt lake,", "has the world's largest natural gas reserves", "Iran"), ("has the world's largest island, Borneo", "has the world's largest cave chamber,", "has the world's largest flower, the Rafflesia", "Malaysia"), ("has the world's largest river island", "has the world's 4th largest railway infrastructure", "has the world's largest freshwater river island", "India"), ("has the world's largest mountain range, the Himalayas", "has the world's highest mountain, Mount Everest", "has the world's largest glaciers", "Nepal"), ("has the world's largest lake", "has the most military bases in the world", "has the world's largest military budget", "United States"), ("is the largest island nation in Africa", "has the world's largest lemur, the Indri", "has the world's largest baobab tree, the Grandidier's baobab", "Madagascar"), ("has the world's largest coral reef, the Great Barrier Reef", "has the world's largest collection of coral species, the Great Barrier Reef", "has the world's largest turtle species, the Leatherback turtle", "Australia"), ("has the world's coldest desert", "has the world's largest ice sheet", "has no time zone", "Antarctica")]
flagsilhouettes = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cape Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czechia", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Eswatini", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]
lockdown_allowed_categories = []  # ID
lockdown_blacklisted_channels = [] # IDs
allowed_users = [] # IDs
api_keys = {
    "bot_token": "TOKEN",
    "rapidapi": "TOKEN",
    "serpapi": "TOKEN",
    "zukijourney": "TOKEN"
}

print("Flag Emojis up to date as of October 25, 2022")

async def printwrite(msg):
    print(msg)

async def has_permissions(ctx, requireGuild):
    if ctx.guild:
        modrole = ctx.guild.get_role() # moderator role
        if ctx.message.author.guild_permissions.administrator or ctx.message.author.id in allowed_users or modrole in ctx.message.author.roles:
            return True
        else:
            return False
    elif requireGuild == False and not ctx.guild:
        return True

def round_sig(n: int, sig: int) -> int: # from 442244135840382978
    """Returns the amount of decimal places to display in order to display `n` as `sig` sf."""
    return -(int(floor(log10(abs(n))))-1)

def format_number(num: float) -> str:
    if isinstance(num, int):  # no formatting
        return f"{num}"
    if num.is_integer():
        return f"{int(num)}"  # remove trailing ".0..."
    if num >= 0.01:
        num_dp = 2
        return f"{num:.{num_dp}f}" # format to 2dp, change both 2's to change how many it rounds to
    num_sf = 2
    num_decimals = round_sig(num, num_sf)
    return f"{num:.{num_decimals}f}"  # format to 2 sf

def get_mentions(message):
    message_string = message.content

    for i in message.mentions:
        newname = "@" + i.display_name
        message_string = message_string.replace(i.mention, newname)

    for i in message.channel_mentions:
        newname = "#" + i.name
        message_string = message_string.replace(i.mention, newname)
    
    for i in message.role_mentions:
        newname = "@" + i.name
        message_string = message_string.replace(i.mention, newname)
    
    return message_string

async def mentionstrip(guild, list): # {message} has to be a discord.py message object and list has to be the content of the message
    def clear_pings(result):
        if result.group(0) == "@everyone":
            return "`@everyone`"
        return "`@here`"
    mentions = []
    matchedmentions = re.findall(r'<@(\d+)>', list)
    for i in matchedmentions:
        member = await guild.fetch_member(i)
        if member != None:
            mentions.append((f"<@{i}>", member.display_name))
    matchedroles = re.findall(r'<@&(\d+)>', list)
    for i in matchedroles:
        for x in guild.roles:
            if x.id == int(i):
                rolename = x.name
                mentions.append((f"<@&{i}>", rolename))
    for i in mentions: # replace mentions with sanitized versions
        if str(i[0]) in list:
            newname = "`@" + str(i[1]) + "`"
            list = list.replace(str(i[0]), newname)
    list = re.sub(r'@everyone|@here', clear_pings, list) # sanitize @everyone and @here
    return list

async def isdeleteslur(message):
    deleteslurs = [] # This is where you would put slurs that would get deleted
    deleteslur_check = re.findall( '|'.join(deleteslurs), message, re.A)
    # r"(?!maggot)[^e]{2}[gq]{2,}[oо0][tτтr]|" + <--- Add this after the opening parentheses
    # on the previous line in order to add the f-slur filter.
    if deleteslur_check != []:
        return True, deleteslur_check
    return False, deleteslur_check

async def isbanslur(message):
    banslurs = [] # This is where you would put slurs that would ban people
    banslur_check = re.findall(f"({'|'.join(banslurs)})", message)
    if banslur_check != []:
        return True, banslur_check
    return False, banslur_check

async def sluraction(message):
    bot_channel = await message.guild.fetch_channel() # action logs

    deleteslur_check = await isdeleteslur(message.content.lower())
    if deleteslur_check[0]:
        await message.delete()

        embed = discord.Embed(
            color=discord.Color.from_str("#FF0000"), 
            title=f"Slur automatically deleted by {message.author.display_name} in {message.channel.mention}", 
            description=f"{message.content}\n\nMatched String: `{', '.join(deleteslur_check[1])}`").set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id}").set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
        await bot_channel.send(embed=embed)
        
        try:
            await message.author.timeout(datetime.timedelta(minutes=1), reason=f"Sent a slur (Matched String: `{', '.join(deleteslur_check[1])}`)")
        except: # if no permissions
            pass

        watchmouth = await message.channel.send(f"<@{message.author.id}> Watch your mouth!!")
        await asyncio.sleep(3)
        await watchmouth.delete()
        
    banslur_check = await isbanslur(message.content.lower())
    if banslur_check[0]:
        try:
            await message.author.send(f"You were automatically banned for the following message:\n\n{message.content}\n\nIf this message did not contain anything offensive, please contact [HypnoticOcelot](<https://discord.com/users/404053132910395393>)")
        except:
            pass
        await message.delete()
        await message.author.ban(delete_message_days=0, reason=f"Matched user's message({message.content}) with `{', '.join(banslur_check[1])}`")

@bot.event
async def on_ready():
    print(f'Bot connected, logged in as {bot.user}, ID {bot.user.id}')

@bot.event
async def setup_hook():
    await bot.load_extension("catposts")
    # await bot.load_extension("mindfulness")

# @bot.event # presence test
# async def on_presence_update(before, after):
#     modcave = await after.guild.fetch_channel(1047952331603456010)
#     if after.activity != None:
#         # if after.activity.type == discord.ActivityType.playing and after.bot == False:
#             # await modcave.send(f"{after.name} is now playing {after.activity.name}")
#         if after.activity.type != discord.ActivityType.custom and after.id == 473882944407207936: # HAVITURE!!!
#             if after.activity.type == "Spotify":
                

sniped_messages = {}

@bot.event # delete logger and message sniper
async def on_message_delete(message):
    deleteslur_check = await isdeleteslur(message.content.lower())
    msglogs = await message.guild.fetch_channel( ) # message logs
    files = []
    attachedfiles = ""


    if message.author != bot.user and not deleteslur_check[0]:
        if (message.attachments != [] or message.stickers != []):
            if message.attachments != []:
                for i in message.attachments:
                    files.append(i)
            if message.stickers != []:
                for i in message.stickers:
                    if isinstance(await i.fetch(), discord.GuildSticker): # can't reupload discord's lottie format stickers
                        files.append(i)
            attachedfiles = "| Attached Files Above"
        logattachments = [await i.to_file() for i in files]
        embed = discord.Embed(
            color=discord.Color.from_str("#FF0000"), 
            title=f"Message deleted by {message.author.display_name} in {message.channel.mention}", 
            description=message.content).set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id} {attachedfiles}").set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
        await msglogs.send(embed=embed, files=logattachments)

        naughtylistattachments = [await i.to_file() for i in files]
        naughtylist = [] # user ids
        isreplying = ""
        if message.reference != None:
            isreplying = f" ([Reply](<{message.reference.jump_url}>))"
        if message.author.id in naughtylist:
            sanitizedmessage = await mentionstrip(message.guild, message.content)
            def replace_links(result):
                return f"<{result.group(0)}>"
            if not message.channel.permissions_for(message.author).embed_links:
                sanitizedmessage = re.sub(r'https?:\/\/(www\.)?.+\.\S+', replace_links, sanitizedmessage)
            await message.channel.send(content=f"{message.author.mention}{isreplying}:\n{sanitizedmessage}\n", files=naughtylistattachments)

    # snipes   
    if message.author != bot.user:
      global sniped_messages
      sniped_messages[message.channel.id] = message # log most recent message in channel to sniped messages dictionary
      await asyncio.sleep(30)
      # i don't know what i'm doing with the code below
      try:
          del sniped_messages[message.channel.id] # after 30 seconds, remove most recent message in channel from sniped messages
      except KeyError:
          pass

@bot.hybrid_command(name="snipe", with_app_command=True, description="Snipe the most recent message in a channel, if one is found")
async def snipe(ctx: commands.Context):
    if await has_permissions(ctx, True):
        try: #This piece of code is run if the bot finds anything in the dictionary
            files = []
            message = sniped_messages[ctx.channel.id]
            if (message.attachments != [] or message.stickers != []):
                if message.attachments != []:
                    for i in message.attachments:
                        files.append(await i.to_file())
                if message.stickers != []:
                    for i in message.stickers:
                        if isinstance(await i.fetch(), discord.GuildSticker): # can't reupload discord's lottie format stickers
                            files.append(await i.to_file())
            if ctx.prefix == "/":
                await ctx.reply(f"Successfully sniped {message.author.mention}'s message!", mention_author=False, ephemeral=True)
            await ctx.channel.send(content=f"{message.author.mention}:\n{message.content}\n", files=files)
        except KeyError: #This piece of code is run if the bot doesn't find anything in the dictionary
            if ctx.prefix == "/":
                await ctx.reply(f"Could not find a message from the last 30 seconds to snipe!", mention_author=False, ephemeral=True)
            else:
                await ctx.channel.send(f"Could not find a message from the last 30 seconds to snipe!")

@bot.event # edit logger
async def on_message_edit(before, after):
    if before.author != bot.user and before.content != after.content: # embedded gifs count as edits
        await sluraction(after)
        msglogs = await after.guild.fetch_channel() # message logs channel

        embed = discord.Embed(
            color=discord.Color.from_str("#0a919e"), 
            title=f"Message edited by {before.author.display_name} in {before.channel.mention}", 
            url=after.jump_url,
            description=f"**Before**:\n{before.content}\n**After:**\n{after.content}").set_footer(text=f"User ID: {before.author.id} | Message ID: {after.id}").set_author(name=before.author.name, icon_url=before.author.display_avatar.url)
        await msglogs.send(embed=embed)

@bot.event # roles timeouts, and nickname updates logger
async def on_member_update(before, after):
    userlogs = await after.guild.fetch_channel() # userlogs channel

    #roles
    if before.roles != after.roles:
        rolechanged = list(set(before.roles).symmetric_difference(set(after.roles)))[0]
        if rolechanged in before.roles: # if it was removed
            changetype = "removed from"
            hex = "#FF0000"
        else: # if it was added
            changetype = "given"
            hex = "#00FF00"
        embed = discord.Embed(
            color=discord.Color.from_str(hex), 
            title=f"{after.display_name} {changetype} role", 
            description=f"{after.mention} was {changetype} the {rolechanged.mention} role").set_author(name=before.name, icon_url=before.display_avatar.url)
        await userlogs.send(embed=embed)
        
    #nickname updates
    if before.display_name != after.display_name:
        embed = discord.Embed(
            color=discord.Color.from_str("#0a919e"),
            title=f"{after.display_name} Nickname Changed",
            description=f"**Before**:\n{before.display_name}\n**After:**\n{after.display_name}"
        ).set_author(name=before.name, icon_url=before.display_avatar.url)
        await userlogs.send(embed=embed)
    
    actionlogs = await after.guild.fetch_channel() # action logs channel
    #timeouts 
    if before.timed_out_until != after.timed_out_until:
        async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
            initiator = entry.user
            reason = entry.reason
        if after.timed_out_until == None: # if timeout was removed, won't log natural untimeouts because it doesn't get set to None that way
            change = "Un-Timed Out"
            hex = "#00FF00"
            until = ""
            reason = ""
        elif before.timed_out_until != after.timed_out_until: # specifically checks because of other member updates
            change = "Timed Out"
            hex = "#FF0000"
            until = f"until <t:{int(t.mktime(after.timed_out_until.timetuple()))}:R>" # convert to discord unix timestamp in relative time
            reason = f"\n**Reason:**\n{reason}"
        embed = discord.Embed(
            color=discord.Color.from_str(hex), 
            title=f"{before.display_name} {change}", 
            description=f"{before.mention} was {change.lower()} by {initiator.mention} {until}{reason}").set_author(name=before.name, icon_url=before.display_avatar.url)
        await actionlogs.send(embed=embed)

@bot.event # server mutes and deafens, vc joins/leaves/mutes
async def on_voice_state_update(member, before, after):
    actionlogs = await member.guild.fetch_channel() # actio nlogs
    async for entry in member.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
        initiator = entry.user

    # mutes/deafens
    change = None # in case the modification wasn't a mute or deafen, cancel the action
    if after.mute == False and before.mute == True:
        change = "Unmuted"
        hex = "#00FF00"
    if after.deaf == False and before.deaf == True:
        change = "Undeafened"
        hex = "#00FF00"
    if after.mute == True and before.mute == False:
        change = "Muted"
        hex = "#FF0000"
    if after.deaf == True and before.deaf == False:
        change = "Deafened"
        hex = "#FF0000"

    if change != None:
        embed = discord.Embed(
            color=discord.Color.from_str(hex), 
            title=f"{member.display_name} Server {change}", 
            description=f"{member.mention} was server {change.lower()} by {initiator.mention}").set_author(name=member.name, icon_url=member.display_avatar.url)
        await actionlogs.send(embed=embed)
    
    voicelogs = await member.guild.fetch_channel( ) # voice logs
    changetype = None 
    #vc joins/leaves/moves
    if before.channel == None and after.channel != None:
        changetype = "Joined"
        changename = after.channel.mention
        hex = "#00FF00"    
    if before.channel != None and after.channel == None:
        changetype = "Left"
        changename = before.channel.mention
        hex = "#FF0000"
    if (before.channel != None and after.channel != None) and before.channel != after.channel: # sometimes it just shows the same channel i guess
        changetype = "Switched"
        changename = f"from {before.channel.mention} to {after.channel.mention}"
        hex = "#0a919e"
        if after.channel == member.guild.afk_channel:
            mindfulnessvc = await member.guild.fetch_channel() # mindfulness vc
            await member.move_to(mindfulnessvc, reason="AFK Movement")

        

    if changetype != None:
        embed = discord.Embed(
            color=discord.Color.from_str(hex), 
            title=f"{member.display_name} {changetype} Voice Channel", 
            description=f"{member.mention} {changetype.lower()} {changename}").set_author(name=member.name, icon_url=member.display_avatar.url)
        await voicelogs.send(embed=embed)

@bot.event # server bans
async def on_member_ban(guild, user):
    actionlogs = await guild.fetch_channel() # action logs
    async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
        initiator = entry.user
        reason = entry.reason
    embed = discord.Embed(
        color=discord.Color.from_str("#FF0000"), 
        title=f"{user.display_name} Banned", 
        description=f"{user.name} was banned by {initiator.mention}\n**Reason:**\n{reason}").set_author(name=user.name, icon_url=user.display_avatar.url).set_footer(text=f"User ID: {user.id}")
    await actionlogs.send(embed=embed)

@bot.event # server unbans
async def on_member_unban(guild, user):
    actionlogs = await guild.fetch_channel() # action logs
    async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1):
        initiator = entry.user
    embed = discord.Embed(
        color=discord.Color.from_str("#00FF00"), 
        title=f"{user.display_name} Unbanned", 
        description=f"{user.name} was unbanned by {initiator.mention}").set_author(name=user.name, icon_url=user.display_avatar.url).set_footer(text=f"User ID: {user.id}")
    await actionlogs.send(embed=embed)

@bot.event # server joins
async def on_member_join(member):
    userlogs = await member.guild.fetch_channel() # user logs
    embed = discord.Embed(
        color=discord.Color.from_str("#00FF00"), 
        title=f"{member.display_name} Joined", 
        description=f"{member.name} joined the server!").set_author(name=member.name, icon_url=member.display_avatar.url)
    await userlogs.send(embed=embed)


@bot.event # server leaves/kicks
async def on_member_remove(member):
    userlogs = await member.guild.fetch_channel() # user logs
    actionlogs = await member.guild.fetch_channel() # action logs
    async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
        initiator = entry.user
        reason = entry.reason
        if entry.target == member and entry.created_at.replace(microsecond=0, second=0) == datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0, second=0): # if the target is the member and the audit log entry was created within the past minute (minute-accurate, accounting for time offset in discord.py)
            embed = discord.Embed(
                color=discord.Color.from_str("#FF0000"), 
                title=f"{member.display_name} was kicked", 
                description=f"{member.name} was kicked by {initiator.mention}\n**Reason:**\n{reason}").set_author(name=member.name, icon_url=member.display_avatar.url)
            await actionlogs.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.from_str("#FF0000"), 
                title=f"{member.display_name} left", 
                description=f"{member.name} left the server").set_author(name=member.name, icon_url=member.display_avatar.url)
            await userlogs.send(embed=embed)

ignored = (commands.CommandNotFound, commands.BadLiteralArgument, commands.MissingRequiredArgument)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, ignored):
        return
    else:
        raise error

class customDate(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            argument = datetime.datetime.strptime(argument, '%Y-%m-%d')
            return True, argument
        except:
            return False, argument

async def getbuttons(index, hard):
    if hard == False:
        name4 = random.choice(flagpairs)
        names = [random.choice(flagpairs)[index], random.choice(flagpairs)[index], random.choice(flagpairs)[index], name4[index]] # name4 will be the answer one, we chose this one special because it has both index 1 and 2 saved
        while len(names) != len(set(names)): # Re-roll if there are duplicates
            name4 = random.choice(flagpairs)
            names = [random.choice(flagpairs)[index], random.choice(flagpairs)[index], random.choice(flagpairs)[index], name4[index]]
            await printwrite("Rerolled flagpairs because of duplicates")
    elif hard == True:
        name4 = random.choice(flagpairshard)
        names = [random.choice(flagpairshard)[index], random.choice(flagpairshard)[index], random.choice(flagpairshard)[index], name4[index]] # name4 will be the answer one, we chose this one special because it has both index 1 and 2 saved
        while len(names) != len(set(names)): # Re-roll if there are duplicates
            name4 = random.choice(flagpairshard)
            names = [random.choice(flagpairshard)[index], random.choice(flagpairshard)[index], random.choice(flagpairshard)[index], name4[index]]
            await printwrite("Rerolled flagpairs because of duplicates")
    if index == 1: # crude statement to check whether we're looking for flags or for flag names
        answer = name4[0]
        match = name4[1]
    else:
        answer = name4[1]
        match = name4[0]
    
    random.shuffle(names) # shuffle it so that it's not always answer 4
    return(names, answer, match)

async def getfacts():
    factslist = list(random.choice(flagfacts))
    answer = factslist[-1]
    facts = []
    for i in range(len(factslist) - 1):
        facts.append(factslist[i])
    return (facts, answer)
    
async def getsilhouette(hard):
    silhouette = random.choice(flagsilhouettes)
    path = "/opt/discordbots/silhouettes/" + silhouette + ".png"
    with open(path, 'rb') as fp:
        fp = Image.open(path)
        if hard == True:
            fp = fp.rotate(random.randint(1,360), resample=Image.Resampling.BICUBIC, expand=True)
        bg = Image.new(mode="RGBA", size=(500, 500))
        
        old_width, old_height = fp.size
        x1 = int(math.floor((bg.size[0] - old_width) / 2))
        y1 = int(math.floor((bg.size[1] - old_height) / 2))
        bg.paste(fp, (x1, y1, x1 + old_width, y1 + old_height))

        output_buffer = BytesIO()
        bg.save(output_buffer, "png")  # or whatever format
        output_buffer.seek(0)
        return (output_buffer, silhouette)


@bot.hybrid_command(name = "guessplace", with_app_command=True, description="Guess the name of a place from its flag!")
@app_commands.describe(
    guesstype="Choose your guess!",
    hardmode="Whether to include territories - only works on Flag and Place mode"
)
async def guessplace(ctx: commands.Context, guesstype: Literal["flag", "place", "fact", "silhouette"], hardmode: typing.Optional[bool] = False):
    if guesstype.lower() == "flag":
        flagorplace = "place"
        sendorguess = "Guess"
        guesstype = 0
    elif guesstype.lower() == "place":
        flagorplace = "flag"
        sendorguess = "Send"
        guesstype = 1
    elif guesstype.lower() == "fact":
        flagorplace = "place"
        sendorguess = "Send"
        guesstype = 2
    elif guesstype.lower() == "silhouette":
        flagorplace = "place"
        sendorguess = "Send"
        guesstype = 3
    if guesstype == 0 or guesstype == 1:
        input = await getbuttons(guesstype, hardmode)
        await ctx.reply(f"{sendorguess} the {flagorplace}: {input[2]}", mention_author=False)
        channel = ctx.channel
        def check(m):
                return m.content.lower() == input[1].lower() and m.channel == channel
        try:
            msg = await bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            await channel.send(f"Nobody got it... the {flagorplace} was {input[1]}!")
            await printwrite(f"Nobody got the word, {flagorplace} was {input[1]}")
        else:
            await msg.reply(f"{msg.author.mention} got it!")
            await printwrite(f"{msg.author}({msg.author.id}) won in {msg.guild.name}({msg.guild.id}), word was {input[1]}")
    elif guesstype == 2:
        input = await getfacts()
        fact1 = random.choice(input[0])
        input[0].remove(fact1)
        await ctx.reply(f"1. This country {fact1}", mention_author=False)
        def check(m):
                return m.content.lower() == input[1].lower() and m.channel == ctx.channel
        try:
            msg = await bot.wait_for('message', check=check, timeout=15)
        except asyncio.TimeoutError:
            fact2 = random.choice(input[0])
            input[0].remove(fact2)
            await ctx.channel.send(f"2. This country {fact2}", mention_author=False)
            try:
                msg = await bot.wait_for('message', check=check, timeout=15)
            except asyncio.TimeoutError:
                await ctx.channel.send(f"Nobody got it... the {flagorplace} was {input[1]}!")
                await printwrite(f"Nobody got the word, {flagorplace} was {input[1]}")
            else:
                await msg.reply(f"{msg.author.mention} got it!")
                await printwrite(f"{msg.author}({msg.author.id}) won in {msg.guild.name}({msg.guild.id}), word was {input[1]}")
        else:
            await msg.reply(f"{msg.author.mention} got it!")
            await printwrite(f"{msg.author}({msg.author.id}) won in {msg.guild.name}({msg.guild.id}), word was {input[1]}")
    elif guesstype == 3:
        input = await getsilhouette(hardmode)
        if hardmode == False:
            async with ctx.typing():
                await ctx.reply("Guess the country based off of the silhouette!", file=discord.File(input[0], filename="country.png"), mention_author=False)
        else:
            async with ctx.typing():
                await ctx.reply("Guess the country based off of the silhouette! `[HARD MODE]`", file=discord.File(input[0], filename="country.png"), mention_author=False)
        channel = ctx.channel
        def check(m):
                return m.content.lower() == input[1].lower() and m.channel == channel
        try:
            msg = await bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            await channel.send(f"Nobody got it... the {flagorplace} was {input[1]}!")
            await printwrite(f"Nobody got the word, {flagorplace} was {input[1]}")
        else:
            await msg.reply(f"{msg.author.mention} got it!")
            await printwrite(f"{msg.author}({msg.author.id}) won in {msg.guild.name}({msg.guild.id}), word was {input[1]}")

@bot.hybrid_command(name="resync", with_app_command=True, description="Resync the commands!")
async def resync(ctx: commands.Context):
    if await has_permissions(ctx, True):
        await bot.tree.sync()
        await ctx.reply(content="Resynced slash commands!", mention_author=False, ephemeral=True)
        await printwrite(f"Resynced commands in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}")
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)
        await printwrite(f"{ctx.message.author} attempted to use resync command in {ctx.message.guild}({ctx.message.guild.id})")

async def raptvfunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        overlay = Image.open("images/raptvnotext.png")
        bg = Image.open(BytesIO(img))
        font = ImageFont.truetype(font='fonts/steelfisheb.otf', size=400)

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
        await ctx.reply(mention_author=False, file=discord.File(await raptvfunc(img,msg), filename="output.png"))
        await printwrite(f"raptv command used in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}")

async def quotefunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        overlay = Image.open("/images/quote.png")
        bg = Image.open(BytesIO(img))
        font = ImageFont.truetype(font='/fonts/avenirnext.ttf', size=50)

        bg = bg.resize((overlay.size[1], overlay.size[1]))
        bg = ImageOps.grayscale(bg)
        bg = bg.convert("RGBA")
        bgfinal = Image.new(mode="RGBA", size=(overlay.size[0], overlay.size[1]))
        bgfinal.paste(bg, (-100, 0))
        final = Image.alpha_composite(bgfinal, overlay)
        draw = ImageDraw.Draw(im=final)
        time = datetime.datetime.now(tz=datetime.timezone.utc)
        newmsg = get_mentions(msg)
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
        text = text + "\n\n-" + get_wrapped_text(str(msg.author.display_name), font, line_length=700) + ", " + str(msg.created_at.year)
        draw.text(xy=(final.size[0]/2 + 200, final.size[1]/2), text=text, font=font, fill='#FFFFFF', anchor='mm')
        output_buffer = BytesIO()
        final = final.resize((overlay.size[0], overlay.size[1]))
        final.save(output_buffer, "png", optimize=True, quality=10)  # or whatever format
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="quote", with_app_command=True, description="Create a quote from the most recent message of a member!")
async def quote(ctx: commands.Context, msgid: str):
    msg = await ctx.channel.fetch_message(int(msgid))
    img = msg.author.display_avatar
    img = await img.read()
    if msg.content == "":
        await ctx.reply(content="Message not found! Here are some things to check:\n\n**- Does the user's most recent message include text?**\n**- Has the user sent a message within the last 50 messages?**", mention_author=False, ephemeral=True)
        return
    async with ctx.typing():
        await ctx.reply(mention_author=False, file=discord.File(await quotefunc(img, msg), filename="output.png"))
    await printwrite(f"quote command used in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}; user quoted: {msg.author.name}#{msg.author.discriminator}")

async def spotifyfunc(img, msg):
    with Image.open(BytesIO(img)) as final:
        topImage = Image.open("/images/thisis.png")
        bottomImage = Image.open(BytesIO(img))

        wpercent = (topImage.size[0]/float(bottomImage.size[0]))
        hsize = int((float(bottomImage.size[1])*float(wpercent)))
        bottomImage = bottomImage.resize((topImage.size[0], hsize), Image.Resampling.LANCZOS) # resize to width of topimage

        font = ImageFont.truetype(font='/fonts/gothambold.otf', size=45)
        text = msg.title()
        final = Image.new('RGBA', (topImage.width, topImage.height + bottomImage.height))
        final.paste(topImage, (0, 0))
        final.paste(bottomImage, (0, topImage.height))
        draw = ImageDraw.Draw(im=final)

        def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
                lines = ['']
                for word in text.split():
                    line = f'{lines[-1]} {word}'.strip()
                    if font.getlength(line) <= line_length:
                        lines[-1] = line
                    else:
                        lines.append(word)
                return '\n'.join(lines)

        draw.text(xy=(final.width/2, 110), text=get_wrapped_text(text, font, line_length=500), font=font, fill='#010101', anchor='ma')

        output_buffer = BytesIO()
        final.save(output_buffer, "png")  # or whatever format
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="thisis", with_app_command=True, description="Create a \"This is\" post similar to the spotify layout!")
async def thisis(ctx: commands.Context, img: discord.Attachment, *, msg: str):
    img = await img.read()
    async with ctx.typing():
        await ctx.reply(mention_author=False, file=discord.File(await spotifyfunc(img,msg), filename="output.png"))
        await printwrite(f"thisis command used in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}")

async def hexfunc(msg):
    final = Image.new(mode="RGB", size=(128, 128), color=msg)
    output_buffer = BytesIO()
    final.save(output_buffer, "png")  # or whatever format
    output_buffer.seek(0)
    return output_buffer

@bot.hybrid_command(name="hex", with_app_command=True, description="Get the color of a specific hex code!")
@app_commands.rename(msg="hex")
async def raptv(ctx: commands.Context, msg: str):
    print(type(msg))
    if len(msg) == 6:
        msg = "#" + msg
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', msg)
    if not match:
        await ctx.reply(content="Not a valid hex code!", mention_author=False, ephemeral=True)
    else:
        async with ctx.typing():
            await ctx.reply(mention_author=False, file=discord.File(await hexfunc(msg), filename="output.png"))
    await printwrite(f"hex command used in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}; hex code {msg}")

async def addstickerfunc(img):
    with Image.open(BytesIO(img)) as final:
        await printwrite(final.format)
        final = final.resize((320, 320))
        output_buffer = BytesIO()
        final.save(output_buffer, "png")
        output_buffer.seek(0)
        return output_buffer

@bot.hybrid_command(name="addsticker", with_app_command=True, description="Add a sticker to the server!")
async def raptv(ctx: commands.Context, img: discord.Attachment, emoji: str, *, stickername: str):
    if await has_permissions(ctx, True):
        img = await img.read()
        async with ctx.typing():
            try:
                await ctx.guild.create_sticker(name=stickername, emoji=emoji, file=discord.File(await addstickerfunc(img), filename="sticker.png"), description="")
                remainingSlots = str(ctx.guild.sticker_limit - len(await ctx.guild.fetch_stickers()))
                await ctx.reply(f"Created \"**{stickername}**\"! `{remainingSlots}` slot(s) remaining!", mention_author=False, ephemeral=True)
                await printwrite(f"addsticker command used in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}")
            except Exception as e:
                await ctx.reply(f"Error: `{e}`")


@bot.hybrid_command(name="echo", with_app_command=True, description="Send a message to another channel through the bot!")
async def echo(ctx: commands.Context, channel: discord.TextChannel, *, msg: str, attachment: typing.Optional[discord.Attachment] = None):
    if await has_permissions(ctx, True):
        deleteslur_check = await isdeleteslur(msg)
        banslur_check = await isbanslur(msg)
        if not deleteslur_check[0] and not banslur_check[0]:
            if attachment != None:
                attachment = await attachment.to_file()
            await ctx.reply(content=f"Sent message to {channel.mention}!", mention_author=False, ephemeral=True)
            await channel.send(msg, file=attachment)
        else:
            await ctx.reply(content="Message contains moderated content!", mention_author=False, ephemeral=True)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="banbot", with_app_command=True, description="DANGEROUS: Bans a random server member")
async def banbot(ctx: commands.Context):
    if await has_permissions(ctx, True):
        memberlist = []
        fulldata = []
        async for i in ctx.guild.fetch_members(limit=None):
            if i.bot == False:
                memberlist.append(i.name + "#" + i.discriminator)
                fulldata.append(i)
        rannum = random.randint(0, len(memberlist) - 1)
        ranmember = memberlist[rannum]
        ranmemdata = fulldata[rannum]
        await printwrite(f"Banning random member! Bye, {ranmember}")
        await ctx.send(f"Banning random member! Bye, {ranmember}", mention_author=False)
        await ranmemdata.send(content=f"You were randomly banned from `{ctx.guild.name}`!")
        await ranmemdata.ban(reason="Banned by BanBot")
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="randommember", description="")
async def randommember(ctx: commands.Context):
    if await has_permissions(ctx, True):
        members = []
        async for i in ctx.guild.fetch_members(limit=None):
            if i.bot == False:
                members.append(i)
        ranmem = random.choice(members)
        await ctx.reply(ranmem.mention, mention_author=False, ephemeral=True)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="merch", description="Link to the merch shop!")
async def merch(ctx: commands.Context):
    await ctx.reply(content="<https://shop.example.com>", mention_author=False )
    await printwrite(f"merch command used in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}")

@bot.hybrid_command(name="hieroglyphify", description="For fun, not super accurate; for best results remove silent letters")
async def hgify(ctx: commands.Context, undo: typing.Optional[bool] = False, *, text: str):
    char_map = [
        ("q", "𓎡"),
        ("w", "𓅃"),
        ("e", "𓅂"),
        ("r", "𓂋"),
        ("t", "𓏏"),
        ("y", "𓇌"),
        ("u", "𓅲"),
        ("i", "𓇋"),
        ("o", "𓅱"),
        ("p", "𓊪"),
        ("a", "𓄿"),
        ("s", "𓋴"),
        ("d", "𓂧"),
        ("f", "𓆑"),
        ("g", "𓎼"),
        ("h", "𓉔"),
        ("j", "𓆓"),
        ("k", "𓈎"),
        ("l", "𓃭"),
        ("z", "𓊃"),
        ("x", "𓇨"),
        ("c", "𓎢"),
        ("v", "𓆯"),
        ("b", "𓃀"),
        ("n", "𓈖"),
        ("m", "𓅓")
    ]

    # Replace multiple occurrences of a character with one instance, i.e. "teeest" becomes "test"
    # also makes it lowercase
    text = re.sub(r'(.)\1+', r'\1', text.lower())

    # Replace instances of a character with its hieroglyph equivalent
    if undo == False:
        for i in char_map:
            text = text.replace(i[0], i[1])
    else:
        for i in char_map:
            text = text.replace(i[1], i[0])
    
    await ctx.reply(f"{text}\n-# Adapted from [r74n](<https://c.r74n.com/converter/hieroglyphs>)", mention_author=False)

@bot.hybrid_command(name="dice", description="Roll a dice")
async def dice(ctx: commands.Context, maxroll: typing.Optional[int] = 6, ephemeral: typing.Optional[bool] = False):
    side = random.randint(1, maxroll)
    await ctx.reply(f"The dice landed on {side}!", mention_author=False, ephemeral=ephemeral)
    await printwrite(f"Landed on {side} for {ctx.message.author} in {ctx.message.guild}({ctx.message.guild.id})")

@bot.hybrid_command(name="tomato", description="BOOOOO!!! 🍅")
async def tomato(ctx: commands.Context):
    text = ""
    for i in range(0, random.randint(1, 5)):
        text += f" BOO" + ("O" * random.randint(0, 5)) + ("!" * random.randint(2, 6)) + " " + ("🍅" * random.randint (1, 6))
    await ctx.reply(text, mention_author=False)

@bot.hybrid_command(name="ping", description="Get the bot's ping")
async def ping(ctx: commands.Context):
    ping = round(bot.latency * 1000)
    await ctx.reply(f"My ping is {ping}ms.", mention_author=False, ephemeral=True)
    await printwrite(f"Got ping({ping}ms) for {ctx.message.author} in {ctx.message.guild}({ctx.message.guild.id})")

@bot.hybrid_command(name="savevoice", description="Download a voice message!")
@app_commands.rename(msgid="id")
async def savevoice(ctx:commands.Context, msgid: str):
    try:
        msg = await ctx.channel.fetch_message(int(msgid))
        if msg.flags.voice == True:
            ogg = await msg.attachments[0].to_file(filename=f"{msg.author.name}_{msg.created_at.strftime('%Y-%m-%d')}.ogg")
            await ctx.reply(file=ogg)
        else:
            await ctx.reply("Not a voice message!", mention_author=False, ephemeral=True)
    except ValueError:
        await ctx.reply("Not a valid message ID!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="transcribe", description="Transcribe a voice message!")
@app_commands.rename(msgid="id")
async def transcribe(ctx:commands.Context, msgid: str):
    try:
        msg = await ctx.channel.fetch_message(int(msgid))
        if msg.flags.voice == True:
            ogg = io.BytesIO(await msg.attachments[0].read())
            client = AsyncOpenAI(
                api_key = api_keys['zukijourney'],
                base_url = "https://api.zukijourney.com/v1"
            )
            try:
                response = await ctx.reply("`Transcribing, please wait...`", mention_author=False)
                transcription = await client.audio.transcriptions.create(
                    model="whisper",
                    file=ogg
                )
                await response.edit(content=f"[@{msg.author.display_name} said](<{msg.jump_url}>): \"{await mentionstrip(ctx.guild, transcription.text)}\"")
            except openai.RateLimitError:
                oneminute = datetime.datetime.now().replace(second=0) + datetime.timedelta(minutes=1)
                await ctx.reply(f"Rate limit reached! Try again <t:{int(t.mktime(oneminute.timetuple()))}:R>", mention_author=False, ephemeral=True)
        else:
            await ctx.reply("Not a voice message!", mention_author=False, ephemeral=True)
    except ValueError:
        await ctx.reply("Not a valid message ID!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="smackcam", description="Smack Cam")
@app_commands.rename(timeint="time")
@app_commands.describe(
    timeint="Length of time in seconds"
)
async def smackcam(ctx:commands.Context, user: discord.Member, timeint: typing.Optional[int] = 5):
    if await has_permissions(ctx, True) or user == ctx.message.author:
        try:
            await user.timeout(datetime.timedelta(days=28), reason=f"Smackcammed by {ctx.message.author.display_name}")
            await ctx.reply(f"Smackcammed {user.mention}!", mention_author=False, ephemeral=True)
            async with aiohttp.ClientSession() as session:
                async with session.get("https://media.tenor.com/B3vsZok1kSkAAAAC/smack-cam-cat.gif") as resp:
                    if resp.status != 200:
                        return await channel.send('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    try:
                        await user.send(content="SMACK CAM", file=discord.File(data, 'smackcam.gif'))
                    except:
                        await ctx.channel.send(content=f"{user.mention} SMACK CAM", file=discord.File(data, 'smackcam.gif'))
            await asyncio.sleep(timeint)
            await user.timeout(None)
        except Exception as e:
            await ctx.reply(f"Error: `{e}`", mention_author=False, ephemeral=True)
    else:
        await ctx.reply("No permissions!", mention_author=False, ephemeral=True)
    

@bot.hybrid_command(name="wheel", description="Spin a wheel between multiple options!")
@app_commands.describe(choices="Options; Comma separate each choice.")
async def wheel(ctx: commands.Context, *, choices: str):
    list = choices.split(",")
    newlist = []
    for i in list:
        i = i.replace(",", "")
        if not i == "":
            i = i.strip()
            newlist.append(i)
    if len(list) > 1:
        final = random.choice(newlist)
        await ctx.reply(await mentionstrip(ctx.guild, final), mention_author=False)
        await printwrite(f"Selected \"{final}\" from {newlist} for {ctx.message.author} in {ctx.message.guild}({ctx.message.guild.id})")
    else:
        await ctx.reply("Not enough arguments detected! Did you comma separate them?", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="8ball", description="Shake the Magic 8-Ball!")
async def ball(ctx: commands.Context, question: str):
    answers = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy, try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "My reply is no",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful"
    ]
    await ctx.reply(random.choice(answers), mention_author=False)

@bot.hybrid_command(name="coinflip", description="Flip a coin!")
async def coinflip(ctx: commands.Context):
    sides = ["Heads", "Tails"]
    side = random.choice(sides)
    await ctx.reply("The coin landed on " + side + "!", mention_author=False)
    await printwrite(f"Landed on {side} for {ctx.message.author} in {ctx.message.guild}({ctx.message.guild.id})")

@bot.hybrid_command(name="slowmode", description="Set the slowmode of a channel!")
async def slowmode(ctx: commands.Context, seconds: int):
    if not seconds > 21600:
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.reply(content=f"Successfully set <#{ctx.channel.id}>'s slowmode to {seconds} seconds!", mention_author=False, ephemeral=True)
        await printwrite(f"Successfully set #{ctx.channel}'s slowmode to {seconds} seconds for {ctx.message.author} in {ctx.message.guild}({ctx.message.guild.id})")
    else:
        await ctx.reply(content=f"Integer too high! Maximum: 21600 seconds", mention_author=False, ephemeral=True)
        await printwrite(f"Failed to set #{ctx.channel}'s slowmode to {seconds} seconds for {ctx.message.author} in {ctx.message.guild}({ctx.message.guild.id})")

@bot.hybrid_command(name="pin", description="Pin a message from its ID!")
@app_commands.rename(msgid="id")
async def pin(ctx: commands.Context, msgid: str):
    if await has_permissions(ctx, False):
        msg = await ctx.channel.fetch_message(int(msgid))
        await msg.pin()
        await ctx.reply(content=f"Pinned message in <#{ctx.channel.id}>!", mention_author=False, ephemeral=True)
        await printwrite(f"Pinned \"{msg.content}\" in {ctx.message.guild}({ctx.message.guild.id}) for {ctx.message.author}")
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)
        await printwrite(f"{ctx.message.author} attempted to use pin command in {ctx.message.guild}({ctx.message.guild.id})")

@bot.hybrid_command(name="delete", description="Delete Havitron's messages")
async def delete(ctx: commands.Context, count: int):
    messages = []
    await ctx.reply(f"Deleting {count} messages!", mention_author=False, ephemeral=True)
    if ctx.prefix != "/":
        count += 1
    async for i in ctx.channel.history():
        if i.author == bot.user:
            messages.append(i)
    if await has_permissions(ctx, False):
        for i in range(count):
            if messages != []:
                await messages[0].delete()
                await asyncio.sleep(1)
                messages.pop(0)

# @bot.app_command(name="time", description="Get info about a timezone!")
# async def time(ctx: commands.Context, timezone: str):

@bot.hybrid_command(name="rulesupdate", description="Update the rules!")
async def rulesupdate(ctx:commands.Context):
    if await has_permissions(ctx, True):
        channel = await ctx.guild.fetch_channel("RULESCHANNEL")
        message = await channel.fetch_message("RULES MESSAGE")
        embed = discord.Embed(
            color = discord.Color.from_str("#0a919e"),
            title = "Server Rules",
            description = newrules
        )
        await message.edit(content="||@everyone||", embed=embed)
        await ctx.reply("Updated Rules Embed!", ephemeral=True, mention_author=False)

# @bot.hybrid_command(name"encode", description="Encode a string with various algorithms!")
# async def encode(ctx: commands.Context, : Literal["flag", "place", "fact", "silhouette"])

@bot.hybrid_command(name="inspire", description="Inspirational!")
async def inspire(ctx: commands.Context):
    async with ctx.typing():
        url = "https://inspirobot.me/api?generate=true"
        if datetime.datetime.now(tz=datetime.timezone.utc).month == 12:
            url += "&season=xmas"
            # christmas code!! so jolly
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                quotes = str(await resp.read()).lstrip('b').strip("'")
                await ctx.reply(quotes, mention_author=False)

@bot.hybrid_command(name="funfact", description="Get a fun fact!")
async def funfact(ctx: commands.Context):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/api/v2/facts/random") as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                url = await resp.json()
                randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                embed = discord.Embed(
                    color=randomrgb, 
                    title="Did you know?",
                    description=url['text'],
                    url=url['source_url']).set_footer(text=f"Source: {url['source']}")
                await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="cat", description="Get a random cat picture!")
async def cat(ctx: commands.Context):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                url = await resp.json()
                url = url[0]['url']
                randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                embed = discord.Embed(color=randomrgb, title="Here's your cat image!").set_footer(text="From https://thecatapi.com").set_image(url=url)
                await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="dog", description="Get a random dog picture!")
async def dog(ctx: commands.Context):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://dog.ceo/api/breeds/image/random") as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                url = await resp.json()
                url = url['message']
                randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                embed = discord.Embed(color=randomrgb, title="Here's your dog image!").set_footer(text="From https://dog.ceo/dog-api").set_image(url=url)
                await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="azuframe", description="Get a random frame from Azumanga Daioh")
@app_commands.rename(episodeindex="episode", frameindex="frame")
async def azuframe(ctx: commands.Context, episodeindex: typing.Optional[int] = None, frameindex: typing.Optional[int] = None):
    folder = Path("opt/discordbots/daiohframes")

    episodelist = list(folder.iterdir())
    episodelist.sort()
    if episodeindex == None: # If the user didn't select an episode
        episodeindex = random.randint(1, len(episodelist))
    try:
        episode = episodelist[episodeindex - 1]
    except IndexError: # If the user selected an invalid episode
        episodeindex = random.randint(1, len(episodelist))
        episode = episodelist[episodeindex - 1]

    framelist = list(episode.iterdir())
    framelist.sort()
    if frameindex == None: # If the user didn't select a frame
        frameindex = random.randint(1, len(framelist))
    try: # If the user selected an invalid frame, pick a random valid one
        frame = framelist[frameindex - 1]
    except IndexError:
        frameindex = random.randint(1, len(framelist))
        frame = framelist[frameindex - 1]
    
    percent = round((frameindex / len(framelist)) * 10)
    
    async with ctx.typing():
        embed = discord.Embed(
            color=discord.Color.from_str("#d33682"), 
            description=f"""```ansi
\u001b[0;35mAzumanga Daioh
\u001b[0;37mEpisode \u001b[0;40;31m{episodeindex}
\u001b[0;37mFrame \u001b[0;40;32m{frameindex}\u001b[0;37m of \u001b[0;40;32m{len(framelist)}
\u001b[0;37m[\u001b[0;35m{"█" * percent}\u001b[0;31m{"░" * (10 - percent)}\u001b[0;37m]
```""")
        file = discord.File(frame, filename=f"frame_{frameindex}.png")
        embed.set_image(url=f"attachment://frame_{frameindex}.png")
        await ctx.reply(file=file, embed=embed, mention_author=False)

async def comic_autocomplete(interaction: discord.Interaction, current: str,) -> list[app_commands.Choice[str]]:
    try:
        comics_list = comics.directory.search(current)
        comics_list = [
            app_commands.Choice(name=i, value=i)
            for i in comics_list if current.lower() in i.lower()
        ]
        return comics_list[0 : 25]
    except InvalidEndpointError:
        return []

@bot.hybrid_command(name="comic", description="Get a comic from GoComics!")
@app_commands.autocomplete(comic=comic_autocomplete)
async def gocomic(ctx: commands.Context, comic: str, date: typing.Optional[customDate] = None):
    try:
        if date == None:
            randomcomic = comics.search(comic).random_date()
        elif date[0]:
            try:
                randomcomic = comics.search(comic).date(date[1])
            except InvalidDateError:
                await ctx.reply("Invalid Date!", mention_author=False, ephemeral=True)
        else:
            if date[1].lower() == "latest":
                randomcomic = comics.search(comic).date(datetime.datetime.now(pytz.timezone('America/Chicago')).strftime('%Y-%m-%d')) # Uses Chicago timezone I'm pretty sure, since the company is based in Missouri
            else:
                await ctx.reply("Invalid Date!", mention_author=False, ephemeral=True)
        randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        embed = discord.Embed(
            color=randomrgb,
            title=randomcomic.title,
            url=randomcomic.url,
            description=randomcomic.date).set_image(url=randomcomic.image_url)
        await ctx.reply(embed=embed, mention_author=False)
    except InvalidEndpointError:
        await ctx.reply("Invalid Comic!", mention_author=False, ephemeral=True)

async def timezone_autocomplete(interaction: discord.Interaction, current: str,) -> list[app_commands.Choice[str]]:
    timezone_list = [
        app_commands.Choice(name=i, value=i)
        for i in pytz.all_timezones if current.lower() in i.lower()
    ]
    return timezone_list[0 : 25]

@bot.hybrid_command(name="tzdifference", description="Get the difference between two timezones!")
@app_commands.autocomplete(timezone1=timezone_autocomplete, timezone2=timezone_autocomplete)
async def timezone(ctx: commands.Context, timezone1: str, timezone2: typing.Optional[str] = str(pytz.timezone("UTC"))):
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

@bot.hybrid_command(name="time", descriptione="Get the time in a timezone!")
@app_commands.autocomplete(timezone=timezone_autocomplete)
async def time(ctx: commands.Context, timezone: str, ephemeral: typing.Optional[bool] = False):
    try:
        tz = datetime.datetime.now(tz=pytz.timezone(timezone))
        await ctx.reply(f"It's currently **{tz.strftime('%-I:%M %p')}** for {timezone}(`{tz.strftime('%Z')}`).", ephemeral=ephemeral)
    except pytz.exceptions.UnknownTimeZoneError:
        await ctx.reply("Invalid Timezone(s)!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="bible", description="Get a random bible verse!")
async def bible(ctx: commands.Context):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://bible-api.com/?random=verse") as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                url = await resp.json()
                randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                embed = discord.Embed(
                    color=randomrgb, 
                    title=url['reference'],
                    description=url['text']).set_footer(text=f"{url['translation_name']}")
                await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="xkcd", description="Get the current or a custom XKCD comic!")
async def xkcd(ctx: commands.Context, issue: typing.Optional[int] = None) :
    async with ctx.typing():
        if issue != None:
            issue = f"{issue}/"
        else:
            issue = ""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://xkcd.com/{issue}info.0.json") as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                url = await resp.json()
                randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                embed = discord.Embed(
                    color=randomrgb, 
                    title=f"XKCD #{url['num']}: {url['safe_title']}",
                    description=url['alt']).set_image(url=url['img'])
                await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="wikipedia", description="Search Wikipedia!")
async def wikipedia(ctx: commands.Context, *, search: typing.Optional[str]):
    if search != None:
        search = search.replace(" ", "_")
        search = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search}"
    else:
        search = "https://en.wikipedia.org/api/rest_v1/page/random/summary/"
    headers = {"User-Agent": "ocelot@ocelot.lol"}
    async with aiohttp.ClientSession() as session:
        async with session.get(search, headers=headers) as resp:
            if resp.status != 200:
                return await ctx.reply('Invalid Search!(Hint: The search string is case sensitive)', mention_author=False, ephemeral=True)
            url = await resp.json()
            article_title = url['title']
            article_description = url['extract']
            randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            embed = discord.Embed(
                color=randomrgb, 
                title=article_title, 
                description=article_description, 
                url=url['content_urls']['desktop']['page'])
            try:
                embed = embed.set_thumbnail(url=url['thumbnail']['source'])
            except:
                pass
            await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="tiktok", description="Embed a TikTok!")
async def tiktok(ctx: commands.Context, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.quickvids.win/v1/shorturl/create", json={'input_text': f'{url}'}) as resp:
            url = await resp.json()
            try:
                await ctx.reply(content=f"{url['quickvids_url']}", mention_author=False)
            except:
                await ctx.reply("Invalid URL!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="discordstatus", description="Check Discord's status!")
async def discordstatus(ctx: commands.Context):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://discordstatus.com/api/v2/summary.json") as resp:
            if resp.status != 200:
                return await ctx.reply('Error!', mention_author=False, ephemeral=True)
            data = await resp.json()
            randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))

            status_status = data['status']['description']
            if data['incidents'] == []:
                status_description = "No Unresolved Incidents"
            else:
                status_description = []
                for i in data['incidents']:
                    status_description.append(f"**{i['name']}**\n{i['incident_updates'][0]['body']}")
                status_description = "\n\n".join(status_description)
            
            embed = discord.Embed(
                color=randomrgb, 
                title=f"Discord Status: {status_status}",
                description=status_description, 
                url="https://discordstatus.com/")
            await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="tosdr", description="Search Terms of Service; Didn't read")
async def tosdr(ctx: commands.Context, *, search: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.tosdr.org/search/v4/?query={search}") as resp:
            if resp.status != 200:
                return await ctx.reply('Error!', mention_author=False, ephemeral=True)
            data = await resp.json()
            data = data['parameters']['services'][0]
            randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            try:
                tosdr_rating_image = data['links']['crisp']['badge']['png']
                tosdr_service_name = data['name']
                tosdr_service_url = data['links']['crisp']['service']
                tosdr_points_url = data['links']['crisp']['api']

                async with session.get(tosdr_points_url) as resp:
                    if resp.status != 200:
                        return await ctx.reply('Error!', mention_author=False, ephemeral=True)
                        pass
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
            except Exception as e:
                await ctx.reply(f"No service found! Error: `{e}`", ephemeral=True, mention_author=False)

@bot.hybrid_command(name="google", description="Google anything!")
async def google(ctx: commands.Context, *, query: str):
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://serpapi.com/search.json?q={query}&hl=en&gl=us&safe=active&api_key={api_keys['serpapi']}") as resp:
                if resp.status != 200:
                    return await ctx.reply('Error!')
                data = await resp.json()
                randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                if "answer_box" in data:        
                    answer_box = data['answer_box']            
                    # calculator
                    if answer_box['type'] == "calculator_result":
                        calculator_result = data['answer_box']['result']

                        embed = discord.Embed(
                            color=randomrgb, 
                            title=f"Calculator Result", 
                            description=calculator_result)
                        await ctx.reply(embed=embed, mention_author=False)
                    # weather
                    elif answer_box['type'] == "weather_result":
                        weather_thumbnail = answer_box['thumbnail']
                        weather_location = answer_box['location']
                        weather_temperature = f"{answer_box['temperature']}°"
                        weather_temperature_unit = answer_box['unit']
                        weather_outside = answer_box['weather'] # i.e. Partly Cloudy
                        weather_humidity = answer_box['humidity']
                        weather_wind = answer_box['wind']
                        weather_precipitation = answer_box['precipitation']

                        embed = discord.Embed(
                            color=randomrgb, 
                            title=weather_location, 
                            description=f"{weather_temperature} {weather_temperature_unit}").set_footer(text=f"Weather: {weather_outside} | Humidity {weather_humidity} | Wind {weather_wind} | Precipitation {weather_precipitation}").set_thumbnail(url=weather_thumbnail)
                        await ctx.reply(embed=embed, mention_author=False)
                    # stocks
                    elif answer_box['type'] == "finance_results":
                        finance_thumbnail = answer_box['thumbnail']
                        finance_company_name = answer_box['title']

                        finance_stock_name = answer_box['stock']
                        finance_stock_price = answer_box['price']
                        finance_stock_currency = answer_box['currency']

                        price_movement = answer_box['price_movement']
                        finance_stock_movement = price_movement['movement'] # up or down
                        finance_stock_movement_amount = price_movement['price']
                        finance_stock_movement_percent = f"{price_movement['percentage']}%"
                        finance_stock_movement_date = price_movement['date']
                        
                        embed = discord.Embed(
                            color=randomrgb, 
                            title=f"{finance_company_name} -{finance_stock_name}", 
                            description=f"{finance_stock_price} {finance_stock_currency}").set_footer(text=f"{finance_stock_movement} {finance_stock_movement_amount}({finance_stock_movement_percent}) {finance_stock_movement_date}").set_thumbnail(url=finance_thumbnail)
                        await ctx.reply(embed=embed, mention_author=False)
                    # population
                    elif answer_box['type'] == "population_result":
                        population_area = answer_box['place']
                        population_amount = answer_box['population']
                        population_last_update = answer_box['year']

                        embed = discord.Embed(
                            color=randomrgb, 
                            title=f"{population_area} Population", 
                            description=population_amount).set_footer(text=f"As of {population_last_update}")
                        await ctx.reply(embed=embed, mention_author=False)
                    # currency
                    elif answer_box['type'] == "currency_converter":
                        currency_converter = answer_box['currency_converter']
                        
                        currency_from_value = currency_converter['from']['price']
                        currency_formatted_from_value = format_number(currency_from_value)
                        currency_from_type = currency_converter['from']['currency']

                        currency_to_value = currency_converter['to']['price']
                        currency_formatted_to_value = format_number(currency_to_value)
                        currency_to_type = currency_converter['to']['currency']

                        symbol = "=" if currency_from_value == float(currency_formatted_from_value) and currency_to_value == float(currency_formatted_to_value) else "≈"
                        embed = discord.Embed(
                            color=randomrgb, 
                            title=f"Currency Converter", 
                            description=f"{currency_formatted_from_value} {currency_from_type} {symbol} {currency_formatted_to_value} {currency_to_type}")
                        await ctx.reply(embed=embed, mention_author=False)
                    # translation
                    elif answer_box['type'] == "translation_result":
                        translation_original_text = f"\"{data['answer_box']['translation']['source']['text']}\""
                        translation_target_language = data['answer_box']['translation']['target']['language']
                        translation_target_text = data['answer_box']['translation']['target']['text']
                        embed = discord.Embed(
                            color=randomrgb, 
                            title=f"{translation_original_text} in {translation_target_language}", 
                            description=f"{translation_target_text}")
                        await ctx.reply(embed=embed, mention_author=False)
                    # unit conversion
                    elif answer_box['type'] == "unit_converter":
                        unit_conversion_type = answer_box['unit_type']
                        
                        unit_from_value = answer_box['from']['value']
                        unit_formatted_from_value = format_number(unit_from_value)
                        unit_from_unit = answer_box['from']['unit']

                        unit_to_value = answer_box['to']['value']
                        unit_formatted_to_value = format_number(unit_to_value)
                        unit_to_unit = answer_box['to']['unit']

                        symbol = "=" if unit_from_value == float(unit_formatted_from_value) and unit_to_value == float(unit_formatted_to_value) else "≈"
                        embed = discord.Embed(
                            color=randomrgb, 
                            title=unit_conversion_type,
                            description=f"{unit_formatted_from_value} {unit_from_unit} {symbol} {unit_formatted_to_value} {unit_to_unit}")
                        await ctx.reply(embed=embed, mention_author=False)
                    elif answer_box['type'] == "dictionary_results":
                        dictionary_name = answer_box['syllables'].replace("·", "")
                        dictionary_syllables = answer_box['syllables']
                        title = dictionary_name if dictionary_syllables == dictionary_name else f"{dictionary_name} - {dictionary_syllables}"
                        dictionary_pronunciation = answer_box['pronunciation_audio']
                        dictionary_word_type = answer_box['word_type']
                        dictionary_descriptions = []
                        for i in range(len(answer_box['definitions'])):
                            definition = answer_box['definitions'][i]
                            try:
                                example = answer_box['examples'][i]
                                dictionary_descriptions.append(f"{i + 1}. `{definition}`\n*{example}*\n")
                            except:
                                dictionary_descriptions.append(f"{i + 1}. `{definition}`\n")
                        dictionary_descriptions = ''.join(dictionary_descriptions)
                        
                        embed = discord.Embed(
                            color=randomrgb,
                            title=title,
                            url=dictionary_pronunciation,
                            description = dictionary_descriptions
                        ).set_footer(text=dictionary_word_type)
                        await ctx.reply(embed=embed, mention_author=False)
                    else:
                        organic_results = data['organic_results'][0]

                        result_title = organic_results['title']
                        result_url = organic_results['link']
                        result_snippet = organic_results['snippet']
                        result_source = organic_results['source']
                        try:
                            result_thumbnail = organic_results['thumbnail']
                        except:
                            basedomain = urlsplit(organic_results['link']).netloc
                            result_thumbnail = f"https://icon.horse/icon/{basedomain}"

                        embed = discord.Embed(
                            color=randomrgb, 
                            title=result_title, 
                            url=result_url, 
                            description=result_snippet).set_footer(text=f"Source: {result_source}")
                        embed.set_thumbnail(url=result_thumbnail)
                        await ctx.reply(embed=embed, mention_author=False)                     
                else:
                    organic_results = data['organic_results'][0]

                    result_title = organic_results['title']
                    result_url = organic_results['link']
                    result_snippet = organic_results['snippet']
                    result_source = organic_results['source']
                    try:
                        result_thumbnail = organic_results['thumbnail']
                    except:
                        basedomain = urlsplit(organic_results['link']).netloc
                        result_thumbnail = f"https://icon.horse/icon/{basedomain}"
                    
                    embed = discord.Embed(
                        color=randomrgb, 
                        title=result_title, 
                        url=result_url, 
                        description=result_snippet).set_footer(text=f"Source: {result_source}")
                    embed.set_thumbnail(url=result_thumbnail)
                    await ctx.reply(embed=embed, mention_author=False)      

@bot.hybrid_command(name="boostorsub", description="Boost or subscribe for image perms")
async def boostorsub(ctx: commands.Context):
    await ctx.reply("https://media.discordapp.net/attachments/816119274183458867/1051733128777052240/caption.gif", mention_author=False)


@bot.hybrid_command(name="wordify", description="Convert unicode strings to words!")
async def wordify(ctx: commands.Context, message:str):
    messagelist = [*message]
    chars = []
    for i in messagelist:
        if i != " ":
            chars.append(unicodedata.name(i).lower())
            chars.append(" ")
    final = "".join(map(str, chars)) 
    if len(final) <= 2000:
        await ctx.reply(final, mention_author=False)
    else:
        await ctx.reply("Output too long! Outputted >2000 characters.")

@bot.hybrid_command(name="itemshop", description="Get today's Fortnite item shop!")
async def itemshop(ctx: commands.Context):
    today = datetime.datetime.now(tz=datetime.timezone.utc)
    url = f"https://bot.fnbr.co/shop-image/fnbr-shop-{today.day}-{today.month}-{today.year}.png"
    randomrgb = discord.Color.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    embed = discord.Embed(color=randomrgb, title=f"Item Shop for {today.strftime('%A, %B %d')}").set_footer(text="From https://fnbr.co/").set_image(url=url)
    await ctx.reply(embed=embed, mention_author=False)
            
@bot.hybrid_command(name="createpoll", description="Add vote reactions for a message!")
async def vote(ctx: commands.Context, msgid:str):
    message = await ctx.channel.fetch_message(int(msgid))
    if await has_permissions(ctx, False):
        emojis = ['<:voteyes:1007343090769592320>', '<:voteno:1007343102392008834>']
        for emoji in emojis:
            await message.add_reaction(emoji)
        await ctx.reply(content=f"Added reactions to {message.author.mention}'s message!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="lockdown", description="Lockdown a channel! If a channel isn't specified, will lock every channel")
async def lockdown(ctx: commands.Context, channel: typing.Optional[discord.abc.GuildChannel]):
    if await has_permissions(ctx, True):
        if channel != None:
            description = "`This channel has been locked!`"
        else:
            description = "`All channels have been locked!`"
        lock_embed = discord.Embed(
            color = discord.Color.from_rgb(255, 0, 0),
            title = "🔒 Channel Locked!",
            description = description
        ).set_thumbnail(url=ctx.bot.user.display_avatar.url)

        await ctx.reply(content="Lockdown initiated!", mention_author=False, ephemeral=True)
        if channel == None:
            for i in lockdown_allowed_categories:
                category = ctx.guild.get_channel(i) #getting channel because categories count as channels
                for x in category.channels:
                    if x.id not in lockdown_blacklisted_channels:
                        overwrite = x.overwrites_for(ctx.guild.default_role)
                        if x.type is discord.ChannelType.voice:
                            overwrite.connect = False
                        else:
                            overwrite.send_messages = False
                        await x.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            announcements_channel = ctx.guild.get_channel("ANNOUNCEMENTS_CHANNEL")
            await announcements_channel.send(embed=lock_embed)
        else:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            if channel.type is discord.ChannelType.voice:
                overwrite.connect = False
            else:
                overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await channel.send(embed=lock_embed)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

@bot.hybrid_command(name="unlockdown", description="Unlockdown a channel! If a channel isn't specified, will lock every channel")
async def unlockdown(ctx: commands.Context, channel: typing.Optional[discord.abc.GuildChannel]):
    if await has_permissions(ctx, True):
        if channel != None:
            description = "`This channel has been unlocked!`"
        else:
            description = "`All channels have been unlocked!`"
        unlock_embed = discord.Embed(
            color = discord.Color.from_rgb(0, 255, 0),
            title = "🔓 Channel Unlocked!",
            description = description
        ).set_thumbnail(url=ctx.bot.user.display_avatar.url)
        overwrite = discord.PermissionOverwrite()

        await ctx.reply(content="Unlockdown initiated!", mention_author=False, ephemeral=True)
        if channel == None:
            for i in lockdown_allowed_categories:
                category = ctx.guild.get_channel(i) #getting channel because categories count as channels
                for x in category.channels:
                    if x.id not in lockdown_blacklisted_channels:
                        overwrite = x.overwrites_for(ctx.guild.default_role)
                        if x.type is discord.ChannelType.voice:
                            overwrite.connect = None
                        else:
                            overwrite.send_messages = None
                        await x.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            announcements_channel = ctx.guild.get_channel("ANNOUNCEMENTS_CHANNEL")
            await announcements_channel.send(embed=unlock_embed)
        else:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            if channel.type is discord.ChannelType.voice:
                overwrite.connect = None
            else:
                overwrite.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await channel.send(embed=unlock_embed)
    else:
        await ctx.reply(content="No permissions!", mention_author=False, ephemeral=True)

# @bot.hybrid_command(name="time", description="Convert times from one timezone to another!")
# async def tempcmd(
#     ctx: commands.Context,
#     from: Literal["UTC", "ECT", "EET", "ART", "EAT", "MET", "NET", "PLT", "IST", "BST", "VST", "CTT", "JST", "ACT", "AET", "SST", "NST", "MIT", "HST", "AST", "PST", "PNT", "MST", "CST", "EST", "IET", "PRT", "CNT", "AGT", "BET", "CAT"],
#     to: Literal["UTC", "ECT", "EET", "ART", "EAT", "MET", "NET", "PLT", "IST", "BST", "VST", "CTT", "JST", "ACT", "AET", "SST", "NST", "MIT", "HST", "AST", "PST", "PNT", "MST", "CST", "EST", "IET", "PRT", "CNT", "AGT", "BET", "CAT"],
#     hour: app_commands.Range[int, 1, 12],
#     minute: app_commands.Range[int, 0, 59],
#     ampm: Literal["AM", "PM"]
# ):
#     print("Works!")


@bot.hybrid_group(name="e")
async def e(ctx: commands.Context):
    pass

@e.command(name="free", description="/e free")
async def efree(ctx: commands.Context):
    await ctx.reply("/e free", mention_author=False)

@bot.event
async def on_message(message):
    if message.channel.id == 00000000 and message.author.id == 00000000: # announcements and birthday bot
        await message.add_reaction("🎂")
    if not message.author.bot: # If the message is not from a bot
        notenorids = [00000000, 0000000] # channels where gifs aren't allowed

        if message.channel.id in notenorids:
            matches = re.search(r"^https?:\/\/(www\.)?tenor\.com\/view\/.*$|^https:\/\/(cdn|media)\.discordapp\.(com|net)\/attachments\/[0-9]+\/[0-9]+\/.*\.gif$|^https?:\/\/[^ ]*\.gif$", message.content)
            # looks for any tenor link, cdn/media.discordapp.com/net links and any link ending in .gif
            if matches:
                await message.delete()
                await printwrite(f"Gif deleted in #{message.channel} by {message.author}:\n({matches.group(0)})")
        if not message.author.bot:
            if not message.channel.permissions_for(message.author).embed_links:
                matches = re.search(r"^https?:\/\/(www\.)?tenor\.com\/view\/.*$|^https:\/\/(cdn|media)\.discordapp\.(com|net)\/attachments\/[0-9]+\/[0-9]+\/.*\.gif$|^https?:\/\/[^ ]*\.gif$", message.content)
                # looks for any tenor link, cdn/media.discordapp.com/net links and any link ending in .gif
                if matches:
                    try:
                        await message.delete()
                        await printwrite(f"Gif deleted in #{message.channel} by {message.author}:\n({matches.group(0)})")
                    except:
                        pass
        if message.channel.id == 000000000000000: # intros
            await message.add_reaction("<:ratio:1019962452428980254>")
        if message.channel.id == 000000000000000: # polls channel
            emojis = ['<:voteyes:1007343090769592320>', '<:voteno:1007343102392008834>']
            for emoji in emojis:
                await message.add_reaction(emoji)
                await printwrite(f"Reacted in polls channel")
        if message.channel.id == 000000000000000 or message.channel.id == 000000000000000: # art sharing and haviture fanart
            if message.attachments != [] or re.search(r'https?:\/\/[\S]*', message.content):
                await message.add_reaction("⭐")
        if "uglyasscat" in message.content:
            await message.add_reaction("<:uglyasscat:990349767521472512>")
            await printwrite(f":uglyasscat:")
        if "freaky" in message.content.lower() and random.randint(1,10) == 1:
            await message.channel.send(f"freaky mode activated {'👅'*random.randint(1,5) }", reference=message, mention_author=False, allowed_mentions=None)
        # if "femboy" in message.content.lower():
        #     await asyncio.sleep(0.2)
        #     await message.delete()
        #     if "femboys" in message.content.lower():
        #         nofem = await message.channel.send(f"{message.author.mention} say \"feminine boys\" instead")
        #     else:
        #         nofem = await message.channel.send(f"{message.author.mention} say \"feminine boy\" instead")
        #     await asyncio.sleep(3)
        #     await nofem.delete()

        if message.guild:
            await sluraction(message)

        gptchannel_whitelist = [] # Channels where GPT is alloewd
        if message.channel.id in gptchannel_whitelist and (random.randint(1, 200) == 1 or bot.user in message.mentions):
            async with message.channel.typing():
                initialmessage = message
                chathistory = [message async for message in message.channel.history(limit=10)]
                chathistory_formatted = []
                for message in chathistory:
                    if (message.author != bot.user):
                        url_pattern = r'https?:\/\/(?:[\w-]+[.]?)+[\w\/.-]+'
                        user_message = {
                            "role": "user",
                            "name": f"{message.author.name.replace('.', '_')}",
                            "content": []
                        }
                        if message.content != "":
                            user_message['content'].append({
                                "type": "text",
                                "text": f"{message.clean_content}"
                            })
                        else:
                            user_message['content'].append({
                                "type": "text",
                                "text": f"(No Message)"
                            })
                        if (message.attachments != [] or message.stickers != [] or re.search(url_pattern, message.content)) and chathistory.index(message) == 0: # only reads attachments from the most recent message for stability and token reasons
                            for i in message.attachments:
                                if i.content_type.startswith("image/"): # if it has the image media type
                                    user_message['content'].append({
                                        "type": "image_url",
                                        "image_url": {
                                            "url": i.url,
                                            "detail": "low"
                                        }
                                    })
                            for i in message.stickers:
                                if i.format != discord.StickerFormatType.lottie: # if it's not a lottie sticker
                                    user_message['content'].append({
                                        "type": "image_url",
                                        "image_url": {
                                            "url": i.url,
                                            "detail": "low"
                                        }
                                    })
                            for i in re.findall(url_pattern, message.clean_content):
                                async with aiohttp.ClientSession() as session: # make sure an image is being sent
                                    try: 
                                        async with session.get(i) as resp:
                                            if resp.content_type.startswith("image/"): # if image MIME type
                                                user_message['content'].append({
                                                    "type": "image_url",
                                                    "image_url": {
                                                        "url": i.url,
                                                        "detail": "low"
                                                    }
                                                })
                                    except aiohttp.client_exceptions.ClientConnectorError: # if it's not a valid url
                                        pass

                        chathistory_formatted.append(user_message)
                        try:
                            bot_message = chathistory[chathistory.index(message) + 1].content.lower()
                            limited_words = ["moderation", "guidelines"]
                            if chathistory[chathistory.index(message) + 1].author == bot.user and all(word not in bot_message for word in limited_words): # to prevent content moderation loops
                                chathistory_formatted.append({
                                    "role": "assistant",
                                    "content": bot_message
                                    # "content": ""
                                    }) # Required because consecutive entries of the same role type are not allowed
                            else:
                                # chathistory_formatted.append({
                                #     "role": "assistant",
                                #     "content": ""
                                #     }) # Required because consecutive entries of the same role type are not allowed
                                #above code no longer necessary
                                pass
                        except IndexError:
                            pass
                # Make sure that a user is the most recent input
                while chathistory_formatted[-1]["role"] == "assistant":
                    chathistory_formatted.pop(-1)
                    # else:
                    #     chathistory_formatted.append({
                    #         "role": "assistant",
                    #         "content": f"{message.content} {attachments}\n"
                    #         })
                botuser = await message.guild.fetch_member(bot.user.id)
                chathistory_formatted.append({
                    "role": "system",
                    "content": f"""You are {botuser.display_name}, also known as {botuser.name}. Your goal is to respond to the MOST RECENT message in the conversation supplied to you. If the other messages aren't relevant to the most recent one, discard them entirely. You should aim for 2-3 sentences, and if a situation calls for a longer response(i.e. \"tell me a story\"), limit to three or less paragraphs.
"""
                })
                chathistory_formatted.reverse()
                
                # slop = [str(chathistory_formatted)[i:i + 4096] for i in range(0, len(str(chathistory_formatted)), 4096)]
                # hypno = await initialmessage.guild.fetch_member(404053132910395393)
                # for i in slop:
                #     newembed = discord.Embed(
                #         description=i
                #     )
                #     await hypno.send(embed=newembed)

                client = AsyncOpenAI(
                    api_key = api_keys['zukijourney'],
                    base_url = "https://api.zukijourney.com/v1"
                )
                
                try:
                    chat_completion = await client.chat.completions.create(
                        model="gpt-5-mini",
                        messages=chathistory_formatted,
                        max_tokens=750,
                        user=initialmessage.author.name
                    )
                except openai.RateLimitError as e:
                    oneminute = datetime.datetime.now().replace(second=0) + datetime.timedelta(minutes=1)
                    await message.channel.send(f"Rate limit reached! Try again <t:{int(t.mktime(oneminute.timetuple()))}:R>", reference=initialmessage, mention_author=False, allowed_mentions=None)
                except openai.BadRequestError as e:
                    await message.channel.send(f"Out of credits! Try again later. {e}", reference=initialmessage, mention_author=False, allowed_mentions=None)


                final = await mentionstrip(initialmessage.guild, chat_completion.choices[0].message.content)
                if "The response was filtered due to the prompt triggering Azure OpenAI's content management policy. Please modify your prompt and retry." in final:
                    await message.channel.send(f"`Error: Response filtered by OpenAI content moderation`", reference=initialmessage, mention_author=False, allowed_mentions=None)
                elif "Request validation failed." in final:
                    await message.channel.send(f"`Error: Failed to access image`", reference=initialmessage, mention_author=False, allowed_mentions=None)
                elif len(final) > 2000 or len(final) == 0:
                    await message.channel.send(f"`Error: Invalid response length!`", reference=initialmessage, mention_author=False, allowed_mentions=None)
                else:
                    await message.channel.send(f"{final}", reference=initialmessage, mention_author=False, allowed_mentions=None)


        tiktokChannels = [] # Channels where the TikTok function is allowed
        if message.channel.id in tiktokChannels:
            if "tiktok.com" in message.content.lower():
                for i in message.content.split():
                    if "tiktok.com" in i:
                        async with aiohttp.ClientSession() as session:
                            async with session.post("https://api.quickvids.win/v1/shorturl/create", json={'input_text': f'{i}'}) as resp:
                                url = await resp.json()
                                try:
                                    await message.channel.send(content=f"{url['quickvids_url']}", reference=message, mention_author=False, allowed_mentions=None)
                                    await message.edit(suppress=True)
                                except Exception as e:
                                    print(e)

        if message.content.lower().startswith('jarvis'):
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

            final = message.content.lower().split() # converts the string into a ["list", "of", "words"]
            final.pop(0) # removes "jarvis" from the string
            if len(final) != 0:
                final[0] = ingFrom(final[0]) # converts the first word into the present participle

                final = " ".join(final) # convert ['this', 'list'] into 'this list'

                # now our message is a string ready to be manipulated

                final = await mentionstrip(message.guild, final) # sanitize mentions

                def swap_words(result): # replaces first person with second person and vice versa
                    match result.group(0).lower():
                        case "i" | "me":
                            return "you"
                        case "you":
                            return "me"
                        case "my":
                            return "your"
                        case "your":
                            return "my"
                        case "myself":
                            return "yourself"
                        case "yourself":
                            return "myself"
                        case "am":
                            return "are"
                        case "are":
                            return "am"
                            
                final = re.sub(r'\b(i|me|you|my|your|myself|yourself|am|are)\b', swap_words, final)

                def replace_links(result):
                    return f"<{result.group(0)}>"
                
                if not message.channel.permissions_for(message.author).embed_links:
                    final = re.sub(r'https?:\/\/(www\.)?.+\.\S+', replace_links, final)

                if final.endswith("?"):
                    final = random.choice(["yes", "no"])

                try:
                    await message.channel.send(content=final, reference=message, mention_author=False, allowed_mentions=None) # send the final message
                except discord.HTTPException:
                    await message.channel.send("`Cannot send message! Response is >2000 characters!`", reference=message, mention_author=False, allowed_mentions=None)

        elif message.content.lower().startswith("i'm ") or message.content.lower().startswith("im ") or message.content.lower().startswith("i’m "):
            chance = random.randint(1, 150)
            if chance == 150:
                text = message.content
                list = [*text]
                if text.lower().startswith("i'm") or text.lower().startswith("i’m"):
                    for i in range(3):
                        list.pop(0)
                else:
                    for i in range(2):
                        list.pop(0)
                while list[0] == " ":
                    list.pop(0)
                mentions = []
                list = "".join(map(str, list))
                list = await mentionstrip(message.guild, list.lower())
                final = list
                await message.channel.send(content=f"hi {final}", reference=message, mention_author=False, allowed_mentions=None) # send the final message
                await printwrite(f"Sent \"hi {final}\" to {message.guild}({message.guild.id})")
        elif message.content.lower().startswith("where did my ") and (message.content.lower().endswith(" go") or message.content.lower().endswith(" go?")):
            chance = random.randint(1, 2)
            if chance == 2:
                text = message.content
                txtlist = [*text]
                for i in range(13):
                    txtlist.pop(0)
                if message.content.lower().endswith(" go"):
                    popamt = 2
                else:
                    popamt = 3
                for i in range(popamt):
                    txtlist.pop(-1)
                while txtlist[0] == " " or txtlist[-1] == " ":
                    if txtlist[0] == " ":
                        txtlist.pop(0)
                    else:
                        txtlist.pop(-1)
                mentions = []
                list = "".join(map(str, txtlist))
                list = await mentionstrip(message.guild, list.lower())
                await message.channel.send(content=f"*me, with a {list} shaped throat:* umm, i don't know!", reference=message, mention_author=False, allowed_mentions=None) # send the final message
        elif message.content.lower().startswith("say "):
            chance = random.randint(1, 10)
            if chance == 10:
                text = message.content
                txtlist = [*text]
                for i in range(4):
                    txtlist.pop(0)
                while txtlist[0] == " " or txtlist[-1] == " ":
                    if txtlist[0] == " ":
                        txtlist.pop(0)
                    else:
                        txtlist.pop(-1)
                mentions = []
                list = "".join(map(str, txtlist))
                list = await mentionstrip(message.guild, list.lower())
                await message.channel.send(content=f"{list}", reference=message, mention_author=False, allowed_mentions=None) # send the final message
    await bot.process_commands(message)

bot.run(api_keys['bot_token'])