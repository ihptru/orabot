# Copyright 2011 orabot Developers
#
# This file is part of orabot, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3

def parse_event(self, recv):
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    irc_join_nick = recv.split( '!' ) [ 0 ].split( ':' ) [ 1 ]
    if ( len(irc_join_nick.split()) == 1 ):
        supy_host = recv.split()[0].split('!')[1]
        chan = recv.split()[2].strip()
        ###logs
        self.logs(irc_join_nick, chan, 'join', supy_host, '')
        ###

        ### for pingme
        sql = """SELECT who,users_back FROM pingme
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) != 0 ):
            for i in range(len(records)):
                who = records[i][0]
                users_back = records[i][1].split(',')
                if ( irc_join_nick in users_back ):
                    self.send_reply( (irc_join_nick +' has joined IRC!'), who, who )
                    records_index = users_back.index(irc_join_nick)
                    del users_back[records_index]
                    users_back = ",".join(users_back)
                    if ( len(users_back) == 0 ):
                        sql = """DELETE FROM pingme
                                WHERE who = '"""+who+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
                    else:
                        sql = """UPDATE pingme
                                SET users_back = '"""+users_back+"""'
                                WHERE who = '"""+who+"""'
                        """
                        cur.execute(sql)
                        conn.commit()
        ###
        sql = """SELECT * FROM users
                WHERE user = '"""+irc_join_nick+"'"+"""
        """
        cur.execute(sql)
        conn.commit()
        row = []
        for row in cur:
            pass
        if irc_join_nick not in row:     #user NOT found, add him (if user is not in db, he could not have ]later message)
            sql = """INSERT INTO users
                    (user,state,channels)
                    VALUES
                    (
                    '"""+irc_join_nick+"""',1,'"""+chan+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
        else:   #user is in `users` table; he can have ]later messages
            #for ]last and for logs (add channel in list)
            sql = """SELECT channels FROM users
                    WHERE user = '"""+irc_join_nick+"""'
            """
            cur.execute(sql)
            records = cur.fetchall()
            conn.commit()
            if ( records[0][0] == '' ) or ( str(records[0][0]) == 'None' ):
                channel_to_db = chan
            else:
                channel_to_db = records[0][0]+','+chan
            sql = """UPDATE users
                    SET state = 1, channels = '"""+channel_to_db+"""'
                    WHERE user = '"""+irc_join_nick+"""'
            """
            cur.execute(sql)
            conn.commit()
            sql = """SELECT reciever FROM later
                    WHERE reciever = '"""+irc_join_nick+"'"+"""
            """
            cur.execute(sql)
            conn.commit()

            row = []
            for row in cur:
                pass
            if irc_join_nick in row:    #he has messages in database, read it
                sql = """SELECT * FROM later
                        WHERE reciever = '"""+irc_join_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
                row = []
                msgs = []
                for row in cur:
                    msgs.append(row)
                msgs_length = len(msgs) #number of messages for player
                self.send_message_to_channel( ("You have "+str(msgs_length)+" offline messages:"), irc_join_nick )
                for i in range(int(msgs_length)):
                    who_sent = msgs[i][1]
                    on_channel = msgs[i][3]
                    message_date = msgs[i][4]
                    offline_message = msgs[i][5]
                    self.send_message_to_channel( ("### From: "+who_sent+";  channel: "+on_channel+";  date: "+message_date), irc_join_nick )
                    self.send_message_to_channel( (offline_message), irc_join_nick )
                time.sleep(0.1)
                sql = """DELETE FROM later
                        WHERE reciever = '"""+irc_join_nick+"'"+"""
                """
                cur.execute(sql)
                conn.commit()
    cur.close()
