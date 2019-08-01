import asyncio
import datetime

import discord
from discord.ext import commands
import common.channels as channels
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from pprint import pprint


# authorisation to access google sheet
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "client_secret.json", scope)
gc = gspread.authorize(creds)

# initialise current sheet
sheet = gc.open("Warnings List").sheet1
# intialise test sheet
# test = gc.open("SSPD-Test").sheet1

#-------------------------DANGER: SET TEST SHEET EQUAL TO PROD : DANGER---------------------------#
test = sheet

all = sheet.get_all_records(False, 3, "")

now = datetime.datetime.now()

e = discord.Embed()
e.set_image(
    url="https://discordapp.com/assets/e4923594e694a21542a489471ecffa50.svg")


class ReprimandDatabase(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role("Moderators™")
    async def getline(self, ctx, num):
        await ctx.send(GetRow(num))

    @commands.command(pass_context=True)
    @commands.has_role("Moderators™")
    async def strike(self, ctx, user: discord.Member, *, rule=None):

        # check if a user already has an entry
        listed = alreadyListedCheck(user, test)
        row_index = next_available_row(test)

        warning_text = fr"You have been given a disciplinary strike in the Angory Tom Discord server for:\n{rule}\nStrikes may be repealed 1 month after recieving them if you ask a moderator.\Accumulate too many of these and you'll be banned."
        await user.send(warning_text)

        # if user has no record already then make one else append to the old
        if bool(listed) == False:
            cell_list = test.range(row_index, 1, row_index, 4)
            record = make_new_record(ctx, user, rule, row_index, False)

            cell_list = apply_values(cell_list, record)

            # batch update
            test.update_cells(cell_list)
        else:
            # offset - how much to add to the indices to get the right columns
            offset = existing_warning_count(listed) * 3
            cell_list = test.range(listed, 2+offset, listed, 4+offset)
            record = make_new_record(ctx, user, rule, listed, True)

            cell_list = apply_values(cell_list, record)

            # batch update
            test.update_cells(cell_list)

            if existing_warning_count(listed) == 3:
                msg = f"{user} is on penultimate warning. Take aditional action."
                await channels.modChannel.send(msg)
            if existing_warning_count(listed) >= 4:
                msg = f"{user} used their final warning. Banning user..."
                await channels.modChannel.send(msg)

    # -----------------------------


def apply_values(cell_list, values_list):
    for i, cell in enumerate(cell_list):
        cell_list[i].value = values_list[i]
    return cell_list


def existing_warning_count(row_num):
    cols_used = len(GetRow(row_num))

    count = (cols_used-1)/3
    return count


def make_new_record(ctx, user, rule, row_index, record_exists):
    new_record = []

    if record_exists == False:
        new_record.append(str(user))
        new_record.append(str(rule))
        new_record.append(str(now.strftime("%Y-%m-%d")))
        new_record.append(str(ctx.message.author))
    else:
        new_record.append(str("Rule " + rule))
        new_record.append(str(now.strftime("%Y-%m-%d")))
        new_record.append(str(ctx.message.author))
    return new_record


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
    # str_list gets a list of all enries in column 1
    str_list = list(filter(None, worksheet.col_values(1)))
    found = None
    for item in str_list:
        if str(user.discriminator) in item:
            found = str_list.index(item)+2
            break
    return found


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


def setup(bot):
    bot.add_cog(ReprimandDatabase(bot))
    print("Cog Loaded: Reprimand Database")
