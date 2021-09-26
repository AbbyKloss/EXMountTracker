import sqlite3

con = sqlite3.connect("files/EXMountTracker.db")
cur = con.cursor()

cur.execute(''' create table if not exists Guilds(
				GuildID integer primary key,
				Prefix text
				)''')

cur.execute(''' create table if not exists Users (
				UserID integer primary key,
				GuildID integer references Users(UserID),
                
				ARRB integer,
                ARRM integer,
                ARRE integer,
                ARRG integer,
                ARRX integer,
                ARRA integer,
                ARRN integer,

                HWDe integer,
                HWSo integer,
                HWDa integer,
                HWWa integer,
                HWRn integer,
                HWRs integer,
                HWWh integer,

                SBHa integer,
                SBEu integer,
                SBLu integer,
                SBAu integer,
                SBLe integer,
                SBRe integer,
                SBBl integer,

                ShBD integer,
                ShBE integer,
                ShBL integer,
                ShBR integer,
                ShBS integer,
                ShBI integer,
                ShBF integer
				
				)''')

con.commit()
con.close()
