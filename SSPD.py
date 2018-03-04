
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio

bot = commands.Bot(command_prefix='&')
token_file = open("dToken.txt", "r")
d_token = token_file.readline()

# authorisation to access google sheet
scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
gc = gspread.authorize(creds)
client = gspread.authorize(creds)

# initialise the sheet
sheet = gc.open("Warnings List").sheet1
warnings = sheet.row_values(4)

# remove empty cells
warnings = list(filter(lambda x: x != '', warnings))


@bot.event
async def on_ready():
    print(bot.user.name + " Ready...")
    print("ID: " + bot.user.id)


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("pong!")


@bot.command(pass_context=True)
async def Bertodog(ctx):
    await bot.say(warnings)


bot.run(d_token)
