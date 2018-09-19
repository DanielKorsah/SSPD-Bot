
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from pprint import pprint
import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime
import logging

logging.basicConfig(level=logging.INFO)

now = datetime.datetime.now()
bot = commands.Bot(command_prefix='&')
client = discord.Client()

# credential file for discord token
token_file = open("dToken.txt", "r")
d_token = token_file.readline()

# authorisation to access google sheet
scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
gc = gspread.authorize(creds)
dc = gspread.authorize(creds)

# initialise current sheet
sheet = gc.open("Warnings List").sheet1
# intialise test sheet
# test = gc.open("SSPD-Test").sheet1

#-------------------------DANGER: SET TEST SHEET EQUAL TO PROD : DANGER---------------------------#
test = sheet

all = sheet.get_all_records(False, 3, "")


#-----Hardcode-----

#------------------


@bot.event
#@commands.has_role("Moderators™")
async def on_ready():
    print("ID: " + str(bot.user.id))
    print(bot.user.name + " Ready...")

#----------------------


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def ping(ctx):
    await ctx.send("pong!")


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def getline(ctx, num):
    await ctx.send(GetRow(num))


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def strike(ctx, user: discord.Member, rule):
    print(bool(alreadyListedCheck(user, test)))
    if bool(alreadyListedCheck(user, test)) == False:
        row_index = next_available_row(test)
        if test.cell(row_index, 1).value == "":
            cell_list = test.range(
                letters[0]+str(row_index)+":" + letters[4]+str(row_index))
            cell_list[0].value = str(user)
            cell_list[1].value = str("Rule " + rule)
            cell_list[2].value = str(now.strftime("%Y-%m-%d"))
            cell_list[3].value = str(ctx.message.author)
            test.update_cells(cell_list)
    else:

        alreadyListedCheck(user, test)
    await notification(ctx, user, rule)


@bot.command(pass_context=True)
@commands.has_role("Moderators™")
async def channelTest(ctx, flag: int):
    if flag == 3:
        general = bot.get_channel(266593626501545984)
        await general.send("test" + str(flag))
    elif flag == 2:
        modChannel = bot.get_channel(300045476554735618)
        await modChannel.send("test" + str(flag))
    elif flag == 1:
        logChannel = bot.get_channel(373156271056224256)
        await logChannel.send("test" + str(flag))
    else:
        ctx.send("Incrrect usage. \n channeltest [x] where 0<x<4")
#-----------------------------


def GetRow(num):
    warnings = sheet.row_values(num)
    # remove empty cells
    warnings = list(filter(lambda x: x != '', warnings))
    # warnings.insert(5, "|")
    return warnings


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+2


def alreadyListedCheck(user: discord.Member, worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    found = list()
    for item in str_list:
        if user.id in item:
            found = str_list.index(item)
            break
    return found


def firstEmptyColum():
    return True


async def notification(ctx, user: discord.Member, rule):
    embed = discord.Embed(title="POO LAGOONER DETECTED: Disciplinary Action Taken", description="Strike dealt to @" +
                          str(user) + " for rule" + str(rule) + ".", color=0xFF0000)
    embed.set_footer(
        text="Further misbehaviour may result in deportation to Poo Island.")
    embed.set_image(url="https://i.imgur.com/eYTcdNe.jpg")
    # await client.send_message(discord.Object(id='general'), embed=embed)
    noti_string = str(str(user) + " striked for rule " +
                      rule + " on " + now.strftime("%Y-%m-%d") + ".")
    await ctx.send(embed=embed)
    print(noti_string)


a = ""
# print(bool(a))
a = "a"
# print(bool(a))
letters = ["A", "B", "C", "D", "E", "F", "G",
           "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]
row_index = next_available_row(test)
# print(row_index)

a = ""
print(bool(a))
a = "a"
print(bool(a))
letters = ["A", "B", "C", "D", "E", "F", "G",
           "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"]
row_index = next_available_row(test)
print(row_index)

bot.run(d_token)
