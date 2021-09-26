from discord.ext import commands
import sqlite3
import discord
import random

from dotenv.main import with_warn_for_invalid_lines

#make things easier down the line
ARRList = ["ARRB", "ARRM", "ARRE", "ARRG", "ARRX", "ARRA", "ARRN"]
HWList  = ["HWDe", "HWSo", "HWDa", "HWWa", "HWRn", "HWRs", "HWWh"]
SBList  = ["SBHa", "SBEu", "SBLu", "SBAu", "SBLe", "SBRe", "SBBl"]
ShBList = ["ShBD", "ShBE", "ShBL", "ShBR", "ShBS", "ShBI", "ShBF"]

ARRRead = [" Boreas    ", "Markab     ", "Enbarr     ", "Gullfaxi   ", "Xanthos    ", "Aithon     ", " Nightmare "]
HWRead  = [" Demonic   ", " Sophic    ", " Dark      ", " Warring   ", " Round     ", " Rose      ", " White     "]
SBRead  = [" Hallowed  ", " Euphonius ", " Lunar     ", " Auspicious", " Legendary ", " Reveling  ", " Blissful  "]
ShBRead = [" Diamond   ", " Emerald   ", " Light     ", " Ruby      ", " Shadow    ", " Innocent  ", " Fae       "]

#checks to see if the string input equals anything expected
#if so, outputs database column name
#if not, outputs empty string
def checkString(string):
    #ARR Block
    mount = ""
    if   ((string.upper() == "ARRB") or (string.lower() == "boreas")):
        mount = "ARRB"
    elif ((string.upper() == "ARRM") or (string.lower() == "markab")):
        mount = "ARRM"
    elif ((string.upper() == "ARRE") or (string.lower() == "enbarr")):
        mount = "ARRE"
    elif ((string.upper() == "ARRG") or (string.lower() == "gullfaxi")):
        mount = "ARRG"
    elif ((string.upper() == "ARRX") or (string.lower() == "xanthos")):
        mount = "ARRX"
    elif ((string.upper() == "ARRA") or (string.lower() == "aithon")):
        mount = "ARRA"
    elif ((string.upper() == "ARRN") or (string.lower() == "nightmare")):
        mount = "ARRN"

    #HW Block
    elif ((string.upper() == "HWDE") or (string.lower() == "demonic")):
        mount = "HWDe"
    elif ((string.upper() == "HWSO") or (string.lower() == "sophic")):
        mount = "HWSo"
    elif ((string.upper() == "HWDA") or (string.lower() == "dark")):
        mount = "HWDa"
    elif ((string.upper() == "HWWA") or (string.lower() == "warring")):
        mount = "HWWa"
    elif ((string.upper() == "HWRN") or (string.lower() == "round")):
        mount = "HWRn"
    elif ((string.upper() == "HWRS") or (string.lower() == "rose")):
        mount = "HWRs"
    elif ((string.upper() == "HWWH") or (string.lower() == "white")):
        mount = "HWWh"

    #SB Block
    elif ((string.upper() == "SBHA") or (string.lower() == "hallowed")):
        mount = "SBHa"
    elif ((string.upper() == "SBEU") or (string.lower() == "euphonius")):
        mount = "SBEu"
    elif ((string.upper() == "SBLU") or (string.lower() == "lunar")):
        mount = "SBLu"
    elif ((string.upper() == "SBAU") or (string.lower() == "auspicious")):
        mount = "SBAu"
    elif ((string.upper() == "SBLE") or (string.lower() == "legendary")):
        mount = "SBLe"
    elif ((string.upper() == "SBRE") or (string.lower() == "reveling")):
        mount = "SBRe"
    elif ((string.upper() == "SBBL") or (string.lower() == "blissful")):
        mount = "SBBl"

    #ShB Block
    elif ((string.upper() == "SHBD") or (string.lower() == "diamond")):
        mount = "ShBD"
    elif ((string.upper() == "ShBE") or (string.lower() == "emerald")):
        mount = "ShBE"
    elif ((string.upper() == "SHBL") or (string.lower() == "light")):
        mount = "ShBL"
    elif ((string.upper() == "SHBR") or (string.lower() == "ruby")):
        mount = "ShBR"
    elif ((string.upper() == "SHBS") or (string.lower() == "shadow")):
        mount = "ShBS"
    elif ((string.upper() == "SHBI") or (string.lower() == "innocent")):
        mount = "ShBI"
    elif ((string.upper() == "SHBF") or (string.lower() == "fae")):
        mount = "ShBF"
    
    #Expac Block
    elif (string.upper() == "ARR"):
        mount = "ARR"
    elif (string.upper() == "HW"):
        mount = "HW"
    elif (string.upper() == "SB"):
        mount = "SB"
    elif (string.upper() == "SHB"):
        mount = "ShB"
    elif (string.upper() == "ALL"):
        mount = "ALL"

    return mount

#outputs a string that's 15 characters long
def checkName(string):
    output = ""
    if (len(string) <= 15):
        output = string
        for i in range(14 - len(string)):
            output += " "
    else:
        output = output[:12] + "..."

    return output

class BotCommands(commands.Cog, description="most of the commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='set', help='sets mount info, mount names in table command', usage=" <mount name> <bool>")
    async def set(self, ctx, *args):
        #sqlite3 setup
        if (len(args) == 2):
            con = sqlite3.connect('files/EXMountTracker.db')
            cur = con.cursor()

            #if there isn't a row for the user, make one
            cur.execute("select exists(select * from Users where UserID=?)", (int(ctx.author.id),))
            if (not cur.fetchone()[0]):
                cur.execute("insert into Users values (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)", (int(ctx.author.id), int(ctx.guild.id)))
            
            #defaults for now
            mount = ""
            set = 2
            reply = ""

            mount = checkString(args[0])

            if (args[1] == "0"):
                set = 0
            elif(args[1] == "1"):
                set = 1

            if ((mount == "") or (set == 2)):
                reply = "Error"
            elif (mount == "ARR"):
                for item in ARRList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                reply = mount + " " + str(set)
            elif (mount == "HW"):
                for item in HWList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                reply = mount + " " + str(set)
            elif (mount == "SB"):
                for item in SBList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                reply = mount + " " + str(set)
            elif (mount == "SHB"):
                for item in ShBList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                reply = mount + " " + str(set)
            elif (mount == "ALL"):
                for item in ARRList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                for item in HWList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                for item in SBList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                for item in ShBList:
                    cur.execute("update Users set " + item + "=? where UserID=?", (set, (ctx.author.id)))
                reply = mount + " " + str(set)

            else:
                cur.execute("update Users set " + mount + "=? where UserID=?", (set, (ctx.author.id)))
                reply = mount + " " + str(set)

            con.commit()
            con.close()
            await ctx.reply(reply, mention_author=False)
        else:
            await ctx.reply("wrong number of parameters", mention_author=False)

    @commands.command(name='mounts')
    async def mounts(self, ctx):
        con = sqlite3.connect('files/EXMountTracker.db')
        cur = con.cursor()

        for row in con.execute("select * from Users where UserID=?", (ctx.author.id, )):
            ARRB = str(row[2])
            ARRM = str(row[3])
            ARRE = str(row[4])
            ARRG = str(row[5])
            ARRX = str(row[6])
            ARRA = str(row[7])
            ARRN = str(row[8])

            HWDe = str(row[9])
            HWSo = str(row[10])
            HWDa = str(row[11])
            HWWa = str(row[12])
            HWRn = str(row[13])
            HWRs = str(row[14])
            HWWh = str(row[15])

            SBHa = str(row[16])
            SBEu = str(row[17])
            SBLu = str(row[18])
            SBAu = str(row[19])
            SBLe = str(row[20])
            SBRe = str(row[21])
            SBBl = str(row[22])

            ShBD = str(row[23])
            ShBE = str(row[24])
            ShBL = str(row[25])
            ShBR = str(row[26])
            ShBS = str(row[27])
            ShBI = str(row[28])
            ShBF = str(row[29])

        string = '''```        ARR       |        HW        |        SB         |        ShB        
__________|_______|__________|_______|___________|_______|__________|_______
Mount      | Have? |   Mount   | Have? |   Mount   | Have? |   Mount   | Have?
___________|_______|___________|_______|___________|_______|___________|_______
Boreas     | '''+ARRB+'''     | Demonic   | '''+HWDe+'''     | Hallowed  | '''+SBHa+'''     | Diamond   | '''+ShBD+'''
Markab     | '''+ARRM+'''     | Sophic    | '''+HWSo+'''     | Euphonius | '''+SBEu+'''     | Emerald   | '''+ShBE+'''
Enbarr     | '''+ARRE+'''     | Dark      | '''+HWDa+'''     | Lunar     | '''+SBLu+'''     | Light     | '''+ShBL+'''
Gullfaxi   | '''+ARRG+'''     | Warring   | '''+HWWa+'''     | Auspicious| '''+SBAu+'''     | Ruby      | '''+ShBR+'''
Xanthos    | '''+ARRX+'''     | Round     | '''+HWRn+'''     | Legendary | '''+SBLe+'''     | Shadow    | '''+ShBS+'''
Aithon     | '''+ARRA+'''     | Rose      | '''+HWRs+'''     | Reveling  | '''+SBRe+'''     | Innocent  | '''+ShBI+'''
Nightmare  | '''+ARRN+'''     | White     | '''+HWWh+'''     | Blissful  | '''+SBBl+'''     | Fae       | '''+ShBF+'''

note: 0 is no, 1 is yes```'''

        con.close()
        await ctx.reply(string, mention_author=False)

    @commands.command(name="hasMounts", help="checks who, in the server, has specific mount or an expac's mounts", usage="<mount name | expac>")
    async def has_mounts(self, ctx, *args):
        reply = "None"
        if (len(args) == 1):
            con = sqlite3.connect('files/EXMountTracker.db')
            cur = con.cursor()

            reply = ""
            mount = checkString(args[0])

            if (mount == ""):
                reply = "Not working"

            elif (mount == "ARR"):
                reply += "``` Name           |"
                for item in ARRRead:
                    reply += item
                reply += "\n"
                async for member in ctx.guild.fetch_members(limit=150):
                    for row in cur.execute("select " + mount + " from Users where userID=?", (int(member.id), )):
                        reply += " " + str(member.name)
                        for i in range(15 - len(member.name)):
                            reply += " "
                        reply +=  "| " + str(row[0]) + "\n"
                reply += "```"

            elif (mount == "HW"):
                print(2)

            elif (mount == "SB"):
                print(3)
            
            elif (mount == "SHB"):
                print(4)
            
            else:
                reply += "``` Name           | " + mount + "\n"
                async for member in ctx.guild.fetch_members(limit=150):
                    for row in cur.execute("select " + mount + " from Users where userID=?", (int(member.id), )):
                        reply += " " + str(member.name)
                        for i in range(15 - len(member.name)):
                            reply += " "
                        reply +=  "| " + str(row[0]) + "\n"
                reply += "```"

        
        await ctx.reply(reply, mention_author=False)

    

def setup(bot):
    bot.add_cog(BotCommands(bot))